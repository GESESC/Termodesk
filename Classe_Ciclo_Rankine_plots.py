# Função da biblioteca do Coolprop para determinar
# propriedades termodinâmicas no Sistema internacional
from CoolProp.CoolProp import PropsSI 
# biblioteca para manipular array,matrizes e escalares
import numpy as np 
# Bibliote de gráficos dinâmicos
from bokeh.io import output_notebook, reset_output
from bokeh.plotting import figure, output_file, show


class Ciclo_Rankine_pt:

  """ Esta é a classe Pai que armazena as propriedades inciais do Ciclo, que 
  pode ser Simples, com Regeneração ou com Reaquecimento. As propriedades
  inicias para execução da classe são passados em um dicionário, 'var_est', que
  variam em função das classes filhas.
  
  Além do dicionário, deve ser inserido o fluido de trabalho. 
   """
      

  def __init__(self, vars_est, fluido):

    """ Aqui no construtor da classe, as chaves e os valores do dicionário são
    armazenados em duas listas e posteriormente o método identifica pelas chaves
    as propriedades do ciclo, podendo ser inseridas em qualquer ordem.

    A lista 'propertys' contem o nome de todas as propriedades iniciais que
    podem ser utilizadas nas classes filhas.
    """
     
    self.fluido = fluido
    self.vars_est = vars_est

    var_keys = list( self.vars_est.keys())
    var_values = list( self.vars_est.values())

    propertys = ['P1','P2','P4','T3','T5']

    for i,n in zip(var_keys,range(len(var_keys))):
      if i.upper() == propertys[0]:
        self.P1 = var_values[n]
      elif i.upper() == propertys[1]:
        self.P2 = var_values[n]
      elif i.upper() == propertys[2]:
        self.P4 = var_values[n]
      elif i.upper() == propertys[3]:
        self.T3 = var_values[n]
      elif i.upper() == propertys[4]:
        self.T5 = var_values[n]
      
class Rankine_Simples_plots(Ciclo_Rankine_pt):
  
  ''' Classe responsável por calcular a eficiência e o trabalho de um ciclo 
  Rankine Simples e ideal. As propriedades iniciais necessárias são:
  
  -P1: Pressão do vapor no condensador
  -P2: Pressão do vapor na entrada na turbina ou da saída da caldeira
  -T3: Temperatura do vapor na entrada na turbina ou da saída da caldeira
  -fluido: Fluido de trabalho do ciclo.
  
  '''

  def __init__(self, vars_est, fluido):
    super().__init__(vars_est, fluido)
    

    '''  O método construtor da classe adiciona mais uma variável, "output_var"
    que pode ser "wt", para retornar o trabalho específico da turbina, ou 
    "nt" para retornar a eficiência do ciclo. 

    A função "super()" herda os atributos da Classe Pai , "Ciclo Rankine",
    obtendo as propriedades iniciais já definidas como variáveis, nesse caso
    self.P1, self.P2  e self.T3. 

    O método output retorna o trabalho específico ou eficiência do ciclo.
    '''
    
    # Estado 1
    self.T1 =  PropsSI('T','P',self.P1,'Q',0,self.fluido )
    self.h1 =  PropsSI('H','P',self.P1,'Q',0,self.fluido )
    self.s1 =  PropsSI('S','P',self.P1,'Q',0,self.fluido )
    self.d1 =  PropsSI('D','P',self.P1,'Q',0,self.fluido )

      # Estado 2 
    self.T2 =  PropsSI('T','P',self.P2,'S',self.s1,self.fluido )
    self.h2 =  PropsSI('H','P',self.P2,'S',self.s1,self.fluido )
    self.s2 =  PropsSI('S','P',self.P2,'S',self.s1,self.fluido )
    self.d2 =  PropsSI('D','P',self.P2,'S',self.s1,self.fluido )

      #Estado 3 
    self.P3 = self.P2
    self.h3 =  PropsSI('H','P',self.P3,'T',self.T3,self.fluido )
    self.s3 =  PropsSI('S','P',self.P3,'T',self.T3,self.fluido )
    self.d3 =  PropsSI('D','P',self.P3,'T',self.T3,self.fluido )

      # Estado 4 
    self.P4 = self.P1
    self.s4 = self.s3
    self.h4 =  PropsSI('H','P',self.P4,'S',self.s4,self.fluido)
    self.d4 =  PropsSI('D','P',self.P4,'S',self.s4,self.fluido )
    self.T4 = PropsSI('T','P',self.P4,'S',self.s4,self.fluido )

    

    output_notebook()


    self.f1 = figure(plot_width=500, plot_height=500,
    title="Diagrama T-s Ciclo Rankyne",x_axis_label='Entropia, s(J/kg/K)',
     y_axis_label='Temperatura, T(K)')

    self.f2 = figure(plot_width=500, plot_height=500,  y_axis_type="log",
    x_axis_type="log", title = "Diagrama P-v Ciclo Rankyne",
    x_axis_label='Volume, v (m$^3$/kg)', y_axis_label='Pressão, p (bar)')

    
    # Para gerar o Domo 
    self.pt =PropsSI('PTRIPLE','Water')
    self.Tt = PropsSI('TTRIPLE','Water')
    self.Tc = PropsSI('TCRIT','Water')
    self.pc =PropsSI('PCRIT','Water')
    self.Tv = np.arange(self.Tt,self.Tc,0.1)
    self.pv = PropsSI('P','T',self.Tv,'Q',0,'Water')
    self.sl = PropsSI('S','T',self.Tv,'Q',0,'Water')
    self.sv = PropsSI('S','T',self.Tv,'Q',1,'Water')
    self.dl = PropsSI('D','T',self.Tv,'Q',0,'Water')
    self.dv = PropsSI('D','T',self.Tv,'Q',1,'Water')

    # Processo 1-2 
    self.p = np.array([self.P1,self.P2])
    self.T = np.array([self.T1,self.T2])
    self.d = np.array([self.d1,self.d2])
    self.s = np.array([self.s1,self.s2])


    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d, self.p/100000, line_width=2)

    # Processo 2 até linha de saturação de vapor
    self.T3v = PropsSI('T','P',self.P2,'Q',1,'Water')
    self.s3v = PropsSI('S','P',self.P2,'Q',1,'Water') 
    self.d3v = PropsSI('D','P',self.P2,'Q',1,'Water') 
    self.T = np.linspace(self.T2,self.T3v,10)
    self.p = self.P2*np.ones(self.T.shape)
    self.s =  PropsSI('S','T',self.T,'P',self.p,'Water')
    self.s[-1] = self.s3v 
    self.d = PropsSI('D','T',self.T,'P',self.p,'Water')
    self.d[-1] = PropsSI('D','P',self.P2,'Q',1,'Water')

    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d, self.p/100000, line_width=2)

    # Processo Linha de saturção vapor até estado 3
    self.f1.line([self.s3v,self.s3], [self.T3v,self.T3], line_width=2)
    self.f2.line([1./self.d3v,1./self.d3],
    [self.P3/100000,self.P3/100000], line_width=2)

    # Processo 3 até 4  (Expansão Isentrópica)
    self.p = np.array([self.P3,self.P4])
    self.T = np.array([self.T3,self.T4])
    self.s = np.array([self.s3,self.s4])
    self.d = np.array([self.d3,self.d4])
    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d ,self.p/100000, line_width=2)

    # processo 4-1 
    self.f1.line([self.s1,self.s4],[self.T1, self.T4], line_width=2)
    self.f2.line([1./self.d1, 1./self.d4],[self.P1/100000,self.P4/100000],
    line_width=2)

    self.f1.line(self.sl,self.Tv, line_width=2, color = 'red')
    self.f1.line(self.sv,self.Tv, line_width=2, color = 'red')
    self.f2.line(1./self.dl,self.pv/1000/100, line_width=2, color = 'red')
    self.f2.line(1./self.dv,self.pv/1000/100, line_width=2, color = 'red')



  @property # Torna a Funçao uma propriedade da Classe
  def plot_ts(self):
    return self.f1

  @property # Torna a Funçao uma propriedade da Classe
  def plot_pv(self):
    return self.f2
 
class Rankine_Reaquecimento_plots(Ciclo_Rankine_pt):

  ''' Classe responsável por calcular a eficiência e o trabalho de um ciclo 
  Rankine ideal com reaquecimento . As propriedades iniciais necessárias são:
  
  -P1: Pressão do vapor no condensador
  -P2: Pressão do vapor na entrada na turbina ou da saída da caldeira
  -P4: Pressão do vapor no reaquecedor
  -T3: Temperatura do vapor na entrada na turbina ou da saída da caldeira
  -fluido: Fluido de trabalho do ciclo.
  
  '''

  def __init__(self, vars_est, fluido):

    '''  O método construtor da classe adiciona mais uma variável, "output_var"
    que pode ser "wt", para retornar o trabalho específico da turbina, ou 
    "nt" para retornar a eficiência do ciclo. 

    A função "super()" herda os atributos da Classe Pai , "Ciclo Rankine",
    obtendo as propriedades iniciais já definidas como variáveis, nesse caso
    self.P1, self.P2, self.T3 e self.P4. 

    O método output retorna o trabalho específico ou eficiência do ciclo.
    '''
    

    
    super().__init__(vars_est, fluido)
    
    
    # Estado 1
    self.T1 =  PropsSI('T','P',self.P1,'Q',0,self.fluido )
    self.h1 =  PropsSI('H','P',self.P1,'Q',0,self.fluido )
    self.s1 =  PropsSI('S','P',self.P1,'Q',0,self.fluido )
    self.d1 =  PropsSI('D','P',self.P1,'Q',0,self.fluido )

      # Estado 2 
    self.T2 =  PropsSI('T','P',self.P2,'S',self.s1,self.fluido )
    self.h2 =  PropsSI('H','P',self.P2,'S',self.s1,self.fluido )
    self.s2 =  PropsSI('S','P',self.P2,'S',self.s1,self.fluido )
    self.d2 =  PropsSI('D','P',self.P2,'S',self.s1,self.fluido )

      #Estado 3 
    self.P3 = self.P2
    self.h3 =  PropsSI('H','P',self.P3,'T',self.T3,self.fluido )
    self.s3 =  PropsSI('S','P',self.P3,'T',self.T3,self.fluido )
    self.d3 =  PropsSI('D','P',self.P3,'T',self.T3,self.fluido )

      # Estado 4 
    self.s4 = self.s3
    self.h4 =  PropsSI('H','P',self.P4,'S',self.s4,'Water')
    self.d4 =  PropsSI('D','P',self.P4,'S',self.s4,'Water')
    self.T4 = PropsSI('T','P',self.P4,'S',self.s4,'Water')

      # Estado 5 
    self.P5 = self.P4
    self.T5 = self.T3
    self.h5 =  PropsSI('H','P',self.P5,'T',self.T5,'Water')
    self.s5 =  PropsSI('S','P',self.P5,'T',self.T5,'Water')
    self.d5 =  PropsSI('D','P',self.P5,'T',self.T5,'Water')


      # Estado 6
    self.P6 = self.P1
    self.s6 = self.s5
    self.h6 =  PropsSI('H','P',self.P6,'S',self.s6,'Water')
    self.d6 =  PropsSI('D','P',self.P6,'S',self.s6,'Water')
    self.T6 = PropsSI('T','P',self.P6,'S',self.s6,'Water')

    


    output_notebook()


    self.f1 = figure(plot_width=500, plot_height=500, 
    title="Diagrama T-s Ciclo Rankyne com Reaquecimento",
    x_axis_label='Entropia, s (J/kg/K)', y_axis_label='Temperatura, T (K)')

    self.f2 = figure(plot_width=500, plot_height=500,  y_axis_type="log",
    x_axis_type="log",title = "Diagrama P-v Ciclo Rankyne com Reaquecimento",
    x_axis_label='Volume, v (m$^3$/kg)',y_axis_label='Pressão, p (bar)')

    # Para gerar o Domo 
    self.pt =PropsSI('PTRIPLE','Water')
    self.Tt = PropsSI('TTRIPLE','Water')
    self.Tc = PropsSI('TCRIT','Water')
    self.pc =PropsSI('PCRIT','Water')
    self.Tv = np.arange(self.Tt,self.Tc,0.1)
    self.Pv = PropsSI('P','T',self.Tv,'Q',0,'Water')
    self.sl = PropsSI('S','T',self.Tv,'Q',0,'Water')
    self.sv = PropsSI('S','T',self.Tv,'Q',1,'Water')
    self.dl = PropsSI('D','T',self.Tv,'Q',0,'Water')
    self.dv = PropsSI('D','T',self.Tv,'Q',1,'Water')

    
    # Processo 1-2 
    self.P = np.array([self.P1,self.P2])
    self.T = np.array([self.T1,self.T2])
    self.d = np.array([self.d1,self.d2])
    self.s = np.array([self.s1,self.s2])


    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d, self.P/100000, line_width=2)



    # Processo 2 até linha de saturação de vapor
    self.T3v = PropsSI('T','P',self.P2,'Q',1,'Water')
    self.s3v = PropsSI('S','P',self.P2,'Q',1,'Water') 
    self.d3v = PropsSI('D','P',self.P2,'Q',1,'Water') 
    self.T = np.linspace(self.T2,self.T3v,10)
    self.P = self.P2*np.ones(self.T.shape)
    self.s =  PropsSI('S','T',self.T,'P',self.P,'Water')
    self.s[-1] = self.s3v 
    self.d = PropsSI('D','T',self.T,'P',self.P,'Water')
    self.d[-1] = PropsSI('D','P',self.P2,'Q',1,'Water')

    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d, self.P/100000, line_width=2)


    # Processo Linha de saturção vapor até estado 3
    self.f1.line([self.s3v,self.s3], [self.T3v,self.T3], line_width=2)
    self.f2.line([1./self.d3v,1./self.d3],[self.P3/100000,self.P3/100000],
    line_width=2)


    # Processo 3 até 4  (Expansão Isentrópica)
    self.P = np.array([self.P3,self.P4])
    self.T = np.array([self.T3,self.T4])
    self.s = np.array([self.s3,self.s4])
    self.d = np.array([self.d3,self.d4])
    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d , self.P/100000, line_width=2)


    #processo 4 até 5 (reaquecimento)
    self.f1.line([self.s4,self.s5], [self.T4,self.T5], line_width=2)
    self.f2.line([1./self.d4,1./self.d5],[self.P4/100000,self.P5/100000],
    line_width=2)


    # Processo 5 até 6  (Expansão Isentrópica)
    self.P = np.array([self.P5,self.P6])
    self.T = np.array([self.T5,self.T6])
    self.s = np.array([self.s5,self.s6])
    self.d = np.array([self.d5,self.d6])
    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d , self.P/100000, line_width=2)


    # processo 6-1 
    self.f1.line([self.s1,self.s6],[self.T1, self.T6], line_width=2)
    self.f2.line([1./self.d1, 1./self.d6],[self.P1/100000,self.P6/100000],
    line_width=2)



    self.f1.line(self.sl,self.Tv, line_width=2, color = 'red')
    self.f1.line(self.sv,self.Tv, line_width=2, color = 'red')
    self.f2.line(1./self.dl,self.Pv/1000/100, line_width=2, color = 'red')
    self.f2.line(1./self.dv,self.Pv/1000/100, line_width=2, color = 'red')


  @property # Torna a Funçao uma propriedade da Classe
  def plot_ts(self):
    return self.f1

  @property # Torna a Funçao uma propriedade da Classe
  def plot_pv(self):
    return self.f2
 

class Rankine_Regeneracao_plots(Ciclo_Rankine_pt):

  ''' Classe responsável por calcular a eficiência e o trabalho de um ciclo 
  Rankine ideal com regeneração. As propriedades iniciais necessárias são:
  
  -P1: Pressão do vapor no condensador
  -P2: Pressão do vapor na entrada do regenerador
  -P4: Pressão do vapor na entrada da caldeira
  -T5: Temperatura do vapor na entrada na turbina ou da saída da caldeira
  -fluido: Fluido de trabalho do ciclo.
  
  '''

  
  def __init__(self, vars_est, fluido):

    '''  O método construtor da classe adiciona mais uma variável, "output_var"
    que pode ser "wt", para retornar o trabalho específico da turbina, ou 
    "nt" para retornar a eficiência do ciclo. 

    A função "super()" herda os atributos da Classe Pai , "Ciclo Rankine",
    obtendo as propriedades iniciais já definidas como variáveis, nesse caso
    self.P1, self.P2, self.P4 self.T5. 

    O método output retorna o trabalho específico ou eficiência do ciclo.
    '''

    
    
    super().__init__(vars_est, fluido)
   
    # Estado 1
    self.T1 =  PropsSI('T','P',self.P1,'Q',0,self.fluido )
    self.h1 =  PropsSI('H','P',self.P1,'Q',0,self.fluido )
    self.s1 =  PropsSI('S','P',self.P1,'Q',0,self.fluido )
    self.d1 =  PropsSI('D','P',self.P1,'Q',0,self.fluido )

    # Estado 2 
    self.w_bomba1 = (1./self.d1)*(self.P2-self.P1)
    self.h2 = self.h1 +self.w_bomba1
    self.T2 = PropsSI('T','P',self.P2,'H',self.h2,self.fluido)
    self.s2 =  self.s1
    self.d2 =  PropsSI('D','P',self.P2,'H',self.h2,self.fluido)

      #Estado 3 
    self.P3 = self.P2
    self.h3 =  PropsSI('H','P',self.P2,'Q',0,self.fluido)
    self.s3 =  PropsSI('S','P',self.P2,'Q',0,self.fluido)
    self.d3 =  PropsSI('D','P',self.P2,'Q',0,self.fluido)
    self.T3 =  PropsSI('T','P',self.P2,'Q',0,self.fluido)


      # Estado 4 
    self.w_bomba2 = (1./self.d3)*(self.P4-self.P3)
    self.s4 = self.s3
    self.h4 =  self.h3 + self.w_bomba2
    self.d4 =  PropsSI('D','P',self.P4,'H',self.h4,self.fluido)
    self.T4 = PropsSI('T','P',self.P4,'H',self.h4,self.fluido)


      # Estado 5 
    self.P5 = self.P4
    self.T5 = self.T5
    self.h5 =  PropsSI('H','P',self.P5,'T',self.T5,self.fluido)
    self.s5 =  PropsSI('S','P',self.P5,'T',self.T5,self.fluido)
    self.d5 =  PropsSI('D','P',self.P5,'T',self.T5,self.fluido)


      # Estado 6
    self.P6 = self.P2
    self.s6 = self.s5
    self.h6 =  PropsSI('H','P',self.P6,'S',self.s6,self.fluido)
    self.d6 =  PropsSI('D','P',self.P6,'S',self.s6,self.fluido)
    self.T6 = PropsSI('T','P',self.P6,'S',self.s6,self.fluido)

      # Estado 7
    self.P7 = self.P1
    self.s7 = self.s5
    self.sl =  PropsSI('S','P',self.P7,'Q',0,self.fluido)
    self.sv =  PropsSI('S','P',self.P7,'Q',1,self.fluido)
    self.x7 = (self.s7 - self.sl)/(self.sv-self.sl)
    self.hl =  PropsSI('H','P',self.P7,'Q',0,self.fluido)
    self.hv =  PropsSI('H','P',self.P7,'Q',1,self.fluido)
    self.h7 =self.hl + (self.x7*(self.hv-self.hl))
    self.dl =  PropsSI('D','P',self.P7,'Q',0,self.fluido)
    self.dv =  PropsSI('D','P',self.P7,'Q',1,self.fluido)
    self.d7 =self.dl + (self.x7*(self.dv-self.dl))
    self.T7 = PropsSI('T','P',self.P7,'H',self.h7,self.fluido)

  

    output_notebook()


    self.f1 = figure(plot_width=500, plot_height=500, 
    title="Diagrama T-s Ciclo Rankyne com Regeneração",
    x_axis_label='Entropia, s (J/kg/K)', y_axis_label='Temperatura, T (K)')

    self.f2 = figure(plot_width=500, plot_height=500,  y_axis_type="log",
    x_axis_type="log",title = "Diagrama P-v Ciclo Rankyne com Regeneração",
    x_axis_label='Volume, v (m$^3$/kg)',y_axis_label='Pressão, p (bar)')

    # Para gerar o Domo 
    self.pt =PropsSI('PTRIPLE','Water')
    self.Tt = PropsSI('TTRIPLE','Water')
    self.Tc = PropsSI('TCRIT','Water')
    self.pc =PropsSI('PCRIT','Water')
    self.Tv = np.arange(self.Tt,self.Tc,0.1)
    self.Pv = PropsSI('P','T',self.Tv,'Q',0,'Water')
    self.sl = PropsSI('S','T',self.Tv,'Q',0,'Water')
    self.sv = PropsSI('S','T',self.Tv,'Q',1,'Water')
    self.dl = PropsSI('D','T',self.Tv,'Q',0,'Water')
    self.dv = PropsSI('D','T',self.Tv,'Q',1,'Water')

     #processo 1 até 2
    self.f1.line([self.s1,self.s2], [self.T1,self.T2], line_width=2)
    self.f2.line([1./self.d1,1./self.d2],[self.P1/100000,self.P2/100000],
    line_width=2)

    #processo 2 até 3 
    self.f1.line([self.s2,self.s3], [self.T2,self.T3], line_width=2)
    self.f2.line([1./self.d2,1./self.d3],[self.P2/100000,self.P3/100000], 
    line_width=2)

    #processo 3 até 4 
    self.f1.line([self.s3,self.s4], [self.T3,self.T4], line_width=2)
    self.f2.line([1./self.d3,1./self.d4],[self.P3/100000,self.P4/100000],
    line_width=2)


    # Processo 4 até linha de saturação de vapor
    self.T4v = PropsSI('T','P',self.P4,'Q',1,'Water')
    self.s4v = PropsSI('S','P',self.P4,'Q',1,'Water') 
    self.d4v = PropsSI('D','P',self.P4,'Q',1,'Water') 
    self.T = np.linspace(self.T4,self.T4v,10)
    self.P = self.P4*np.ones(self.T.shape)
    self.s =  PropsSI('S','T',self.T,'P',self.P,'Water')
    self.s[-1] = self.s4v 
    self.d = PropsSI('D','T',self.T,'P',self.P,'Water')
    self.d[-1] = self.d4v

    self.f1.line(self.s, self.T, line_width=2)
    self.f2.line(1./self.d, self.P/100000, line_width=2)


    # Processo Linha de saturção vapor até estado 5
    self.f1.line([self.s4v,self.s5], [self.T4v,self.T5], line_width=2)
    self.f2.line([1./self.d4v,1./self.d5],[self.P4/100000,self.P4/100000],
    line_width=2)


    # Processo   5 - 6 
    self.f1.line([self.s5,self.s6], [self.T5,self.T6], line_width=2)
    self.f2.line([1./self.d5,1./self.d6],[self.P5/100000,self.P6/100000],
    line_width=2)

    # Regeneração  6 - 3 
    self.f1.line([self.s3,self.s6], [self.T3,self.T6], line_width=2)
    self.f2.line([1./self.d3,1./self.d6],[self.P3/100000,self.P6/100000],
    line_width=2)

    # Processo 6 -7 
    self.f1.line([self.s6,self.s7], [self.T6,self.T7], line_width=2)
    self.f2.line([1./self.d6,1./self.d7],[self.P6/100000,self.P7/100000], 
    line_width=2)


    # Processo 7- 1  
    self.f1.line([self.s1,self.s7], [self.T1,self.T7], line_width=2)
    self.f2.line([1./self.d1,1./self.d7],[self.P1/100000,self.P7/100000], 
    line_width=2)

    self.f1.line(self.sl,self.Tv, line_width=2, color = 'red')
    self.f1.line(self.sv,self.Tv, line_width=2, color = 'red')
    self.f2.line(1./self.dl,self.Pv/1000/100, line_width=2, color = 'red')
    self. f2.line(1./self.dv,self.Pv/1000/100, line_width=2, color = 'red')

    
  
  @property # Torna a Funçao uma propriedade da Classe
  def plot_ts(self):
    return self.f1

  @property # Torna a Funçao uma propriedade da Classe
  def plot_pv(self):
    return self.f2
 