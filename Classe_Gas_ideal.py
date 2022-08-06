import numpy as np
import scipy.integrate as integrate  # pacote que faz integrais
import pyromat as pm


class Gases_ideais_lemmon:
    
    
    def __init__(self, T_input, p_input):
        self._T_input = T_input
        self._rho_input = p_input/((0.287e3)*T_input)*(1/28.97)
        self._p_input  = p_input * (1e-6)
        self._u = np.nan
        self._h = np.nan
        self._s = np.nan
        self._cv = np.nan
        self._cp  = np.nan
        self._pr = np.nan
        self._vr = np.nan
        self._speed = np.nan
        air = pm.get('ig.air')

        def entropia_calculo(T_calc, p): #função auxiliar para calcular a entropia
            T_ref = 273.15
            T = T_calc
            Ru = 8.31447 #[kJ/kmol·K]Constante universal dos gases  Cengel pagina 133, 9Ed Inglês eq 3.11
            R_air = 0.2870 #[kJ/kg·K] Contante do gas Cengel pagina 882, nona Ed Ingles tabela A-1
            N6 =  3364.011        
            u = N6/T   #formula u do Nitrogênio arquivo Lemmon pagina 345
            O6 = 2242.45
            O7 = 11580.4     
            v = O6/T #v do oxigênio para calculo do cp, formula Lemmon pagina 345, 
            w = O7/T #w do oxigênio para calculo do cp, formula Lemmon pagina 345, 
            G1  = 3.490888032
            G2  = 2.395525583*10**-6
            G3  = 7.172111248*10**-9
            G4  = -3.115413101*10**-13
            G5  = 0.223806688
            G6  = 0.719309509
            G7  = 0.212236768
            G8  = 0.197938904
            M  = 28.9645        # massa molar do ar
            entropia = lambda x: ((G1*x**0 + G2*x**1 + G3*x**2 + G4*x**3)             
                            + (G5/x**1.5) + (G6*u**2*np.exp(u))/(np.exp(u)-1)**2 
                            + (G7*v**2*np.exp(v))/((np.exp(u)-1)**2) 
                            + ((2/3)*G8*w**2*np.exp(-w))/((2/3)*np.exp(-w)+1)**2)*Ru/x
            entropia_integral, int_err = integrate.quad(entropia,T_ref, T) #integral da entropia
            vr_ref       = 785.95
            pr_ref       = 0.9999185
            entro = entropia_integral/M  #converter a entropia para kj/Kg
            pr = np.exp(entro/R_air) #calcula o pr formula Moran pagina 327
            vr = ((T*pr_ref)/(pr*T_ref))*vr_ref #calcula o vr formula Moran pagina 327
            return pr, vr

        def deriv_part_o2_mist(func, vec_xis, vec_yps, *args, dx_dy=1e-6):
            dderiv2mist = (
                func(vec_xis+dx_dy, vec_yps+dx_dy, args[0], args[1], args[2], args[3]) 
                - func(vec_xis+dx_dy, vec_yps-dx_dy, args[0], args[1], args[2], args[3]) 
                - func(vec_xis-dx_dy, vec_yps+dx_dy, args[0], args[1], args[2], args[3]) 
                - func(vec_xis-dx_dy, vec_yps-dx_dy, args[0], args[1], args[2], args[3])
            )
            return dderiv2mist
        def loc_derivada2ord(matriz, pontos):
            ind_x = np.abs(matriz[0] - pontos[0]).argmin()
            ind_y = np.abs(matriz[1] - pontos[1]).argmin()
            return matriz[2][ind_x]
        def derivada_1var(vec_fxis, vec_xis, pont_xis, n=1):
            if n == 1:
                derv = np.gradient(vec_fxis, vec_xis)
                #ind_x = np.argwhere(vec_xis == pont_xis)
                ind_x = np.abs(vec_xis-pont_xis).argmin()
            else:
                for _i in range(n):
                    derv = np.gradient(vec_fxis, vec_xis)
                    vec_fxis = derv.copy()
                #ind_x = np.argwhere(vec_xis == pont_xis)
                ind_x = np.abs(vec_xis - pont_xis).argmin()
            return derv[ind_x]
        def alpha_zero(tau, delta, N):
            def equacao(tau, delta, N,  ind_tau):
                alpha_z = np.sum(np.array(
                    [np.log(delta),
                    np.sum(np.array([N[k]*tau[ind_tau]**(k-3) for k in range(5)])),
                    N[6]*np.log(tau[ind_tau]),
                    N[7]*np.log(1-np.exp(-N[10]*tau[ind_tau])),
                    N[8]*np.log(1-np.exp(-N[11]*tau[ind_tau])),
                    N[9]*np.log(2/3 + np.exp(N[12]*tau[ind_tau]))
                ]))
                return alpha_z
            try:
                if type(tau) != np.ndarray:
                    tau = np.array([tau])
            except:
                print("Parâmetros inválidos!")
                exit()
            if tau.size > 1:
                ind_tau = tau.size
                alpha_z = np.array([])
                for i in range(ind_tau):
                    alpha_z = np.append(alpha_z, equacao(tau, delta, N, i))
            else:
                ind_tau = 0
                alpha_z = equacao(tau, delta, N, ind_tau)
            return alpha_z
        def alpha_residual(tau, delta, k_vec, j_vec, i_vec, l_vec):

            def equacao(
                tau, delta, k_vec, j_vec, i_vec, l_vec, ind_delta, ind_tau
            ):
                alpha_res = np.sum(
                    [k_vec[k]*delta[ind_delta]**i_vec[k]*tau[ind_tau]**j_vec[k] 
                    for k in range(10)]
                ) 
                + np.sum(
                    [k_vec[k]*delta[ind_delta]**i_vec[k]*tau[ind_tau]**j_vec[k]  
                    * np.exp(-delta[ind_delta]**l_vec[k]) for k in range(10, 19)]
                )
                return alpha_res
            try:
                if type(tau) != np.ndarray and type(delta) != np.ndarray:
                    delta = np.array([delta])
                    tau = np.array([tau])
                elif type(tau) != np.ndarray and type(delta) == np.ndarray:
                    tau = np.array([tau])
                elif type(delta) != np.ndarray and type(tau) == np.ndarray:
                    delta = np.array([delta])
            except:
                print("Parâmetros inválidos!")
                exit()
            else:
                if tau.size > 1:
                    ind_delta = 0
                    ind_tau = tau.size
                    alpha_res = np.array([])
                    for i in range(ind_tau):
                        alpha_res = np.append(
                            alpha_res, 
                            equacao(
                                tau, delta, k_vec, j_vec, i_vec, l_vec, ind_delta, i
                        ))
                elif delta.size > 1:
                    ind_tau = 0
                    ind_delta = delta.size
                    alpha_res = np.array([])
                    for i in range(ind_delta):
                        alpha_res = np.append(
                            alpha_res, 
                            equacao(
                                tau, delta, k_vec, j_vec, i_vec, l_vec, i, ind_tau
                        ))
                else:
                    ind_tau = 0
                    ind_delta = 0
                    alpha_res = equacao(
                        tau, delta, k_vec, j_vec, i_vec, l_vec, ind_delta, ind_tau
                    )
                return alpha_res

        N = [0.605719400e-7, -0.210274769e-4,  -0.158860716e-3,
            -13.841928076, 17.275266575, -0.195363420e-3,
            2.490888032, 0.791309509,  0.212236768,
            -0.197938904, 25.36365,  16.90741,
            87.31279]  # coeficientes tabela 12, 3 coeficientes por linha
        K = [0.118160747229, 0.713116392079,  -0.161824192067e1,
            0.714140178971e-1, -0.865421396646e-1,  0.134211176704,
            0.112626704218e-1, -0.420533228842e-1, 0.349008431982e-1,
            0.164957183186e-3, -0.101365037912, -0.173813690970,
            -0.472103183731e-1, -0.122523554253e-1,  -0.146629609713,
            -0.316055879821e-1,  0.233594806142e-3, 0.148287891978e-1,
            -0.938782884667e-2]  # coeficientes tabela 13, 3 coeficientes por linha
        i = [1, 1, 1, 2, 3, 3, 4, 4, 4, 6, 1, 3, 5, 6,
            1, 3, 11, 1, 3]  # coeficientes tabela 13
        j = [0,  0.33, 1.01, 0, 0, 0.15, 0, 0.2, 0.35,
            1.35, 1.6, 0.8, 0.95, 1.25, 3.6, 6, 3.25, 3.5, 15]  # coeficientes tabela 13
        l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,  1,  1,
            1, 2, 2, 2, 3, 3]  # coeficientes tabela 13
        T_j = 132.6312  # Maxcondentherm temperature 132.6312 K Lemmon Tabela 9 Pagina 342
        p_j = 3.78502   # Maxcondentherm pressure 3.78502 MPa Lemmon Tabela 9 Pagina 342
        rho_j = 10.4477  # rho_j Maxcondentherm density 10.4477 mol/dm3 Lemmon Tabela 9 Pagina 342
        T_c = 132.5306  # Tc Critical temperature 132.5306 K Lemmon Tabela 9 Pagina 342
        p_c = 3.7860    # pc Critical pressure 3.7860 MPa Lemmon Tabela 9 Pasgina 342
        rho_c = 11.8308  # rc Critical density 11.8308 mol/dm3 Lemmon Tabela 9 Pagina 342
        p = np.array([.101325, .2, .5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000])
        T = np.arange(self._T_input-50*0.01, self._T_input+50*0.01, 0.01)
        rho = np.arange(self._rho_input-0.00001*50, self._rho_input+0.00001*50, 0.00001)
        R_air = 0.2870
        delta = rho/rho_j  # calculo do delta
        delta_calc = self._rho_input/rho_j
        tau = T_j/T  # calculo do tau
        tau_calc = T_j/self._T_input
        z = 1 + delta_calc*(
            derivada_1var(
                alpha_residual(tau_calc, delta, K, j, i, l), delta,delta_calc
            ))
        u = (R_air*self._T_input)*(tau_calc*(
            derivada_1var(alpha_zero(tau, delta_calc, N), tau, tau_calc) +
            derivada_1var(
                alpha_residual(tau, delta_calc, K, j, i, l), tau, tau_calc
            )))  # equação 28 energia interna
        h = (R_air*self._T_input)*(tau_calc*(
            derivada_1var(
                alpha_zero(tau, delta_calc, N), tau, tau_calc
            ) 
            + derivada_1var(
                alpha_residual(tau, delta_calc, K, j, i, l), tau, tau_calc,
            )) + delta_calc*(
            derivada_1var(
                alpha_residual(tau_calc, delta, K, j, i, l), delta, delta_calc,
            )) + 1)
        s = air.s(self._T_input)-5
        cv = R_air*((-tau_calc**2*(
            derivada_1var(alpha_zero(tau, delta_calc, N), tau, tau_calc, n=2)
            ) 
            + derivada_1var(
                alpha_residual(
                    tau, delta_calc, K, j, i, l
                ), tau,  tau_calc, n=2
            )))
        vec_deriv2mista = deriv_part_o2_mist(
            alpha_residual, tau, delta, K, j, i, l
        )
        deriv2mista = loc_derivada2ord(
            matriz = [tau, delta, vec_deriv2mista], 
            pontos = [tau_calc, delta_calc]
        )

        cp = cv + R_air*((1 + delta_calc*(
            derivada_1var(
                alpha_residual(tau_calc, delta, K, j, i, l), delta, delta_calc,
            )) - delta_calc*tau_calc*(deriv2mista))**2 / (1 + 2*delta_calc*(
                derivada_1var(
                    alpha_residual(tau_calc, delta, K, j, i, l), delta, delta_calc
                )) +
                delta_calc**2*(
                    derivada_1var(
                        alpha_residual(
                            tau_calc, delta, K, j, i, l
                        ), delta, delta_calc, n=2
        ))))         
        #vr_ref       = 785.95
        #pr_ref       = 0.9999185
        #T_ref        = 273.15
        #pr = np.exp(s/R_air) #calcula o pr formula Moran pagina 327
        #vr = ((self._T_input*pr_ref)/(pr*T_ref))*vr_ref #calcula o vr formula Moran pagina 327  
        k = cp/cv #razão de calor especifico formula 4-31 Cengel 9Ed Inglês, pagina 177
        speed = np.mean(np.sqrt(k*R_air*T*1000)) #velocidade do ar Formula Irving pagina 98, Apêndice V

        pr, vr = entropia_calculo(self._T_input, self._p_input)

        atributos =  u, h, s[0], cv, cp, pr, vr, speed #resultados[indice]

        self._u,    \
        self._h,    \
        self._s,    \
        self._cv,   \
        self._cp,   \
        self._pr,   \
        self._vr,   \
        self._speed = atributos
        

    @property # Torna a Funçao uma propriedade da Classe
    def temperatura(self):
      return '{} K'.format(round(self._T_input,2)) 

    @property # Torna a Funçao uma propriedade da Classe
    def pressao(self):
      return '{} kPa'.format(round(self._p_input*1000,2)) 

    @property # Torna a Funçao uma propriedade da Classe
    def energia_interna(self):
      return '{} kJ/kg'.format(round(self._u,3)) 
  
    @property # Torna a Funçao uma propriedade da Classe
    def entalpia(self):
       return '{} kJ/kg'.format(round(self._h,3)) 
    
    @property # Torna a Funçao uma propriedade da Classe
    def entropia(self):
       return '{} kJ/kg.K'.format(round(self._s,3)) 

    @property # Torna a Funçao uma propriedade da Classe
    def calor_especifico_cv(self):
      return '{} kJ/kg.K'.format(round(self._cv,3)) 

    @property # Torna a Funçao uma propriedade da Classe
    def calor_especifico_cp(self):
      return '{} kJ/kg.K'.format(round(self._cp,3)) 

    #@property # Torna a Funçao uma propriedade da Classe
    #def pressao_reduzida(self):
     # return '{}'.format(round(self._pr,3)) 

   # @property # Torna a Funçao uma propriedade da Classe
   # def volume_reduzido(self):
   #   return '{}'.format(round(self._vr,3)) 
    
    @property # Torna a Funçao uma propriedade da Classe
    def velocidade_do_som(self):
      return '{} m/s'.format(round(self._speed,3)) 

