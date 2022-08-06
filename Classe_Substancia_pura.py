# Importando a biblioteca do Coolprop
import CoolProp.CoolProp as CP
# Função da biblioteca do Coolprop para determinar
# propriedades termodinâmicas no Sistema internacional
from CoolProp.CoolProp import PropsSI 
# Função da biblioteca do Coolprop para determinar o estado
# das propriedades termodinâmicas no Sistema internacional
from CoolProp.CoolProp import PhaseSI
# Biblioteca para manipular array, matrizes e escalares
import numpy as np 


class SubstanciaPura:

    """ Estrutura (classe) que modela o comportamento do objeto real (Substância Pura).
    Esta classe contém os métodos (funções) que operam sobre cada instância e os atributos que difericiam as instâncias. 
    Estas instâncias são capazes de retornar o valor ou estado de uma propriedade termodinâmica de uma Substância Pura,
    com base nos valores de outras duas propriedades termodinâmicas, utililzando-se a biblioteca do Coolprop.
    As propriedades inicias para execução da classe são passados em um dicionário, 'var_est'.
    
    Além do dicionário, deve ser inserido o fluido de trabalho. 
    """

    
   

      #Construtor
      # "init": Construtor (Permite criar funcionalidade inicial da classe)
      # "self" (Objeto) - identifica e acessa a instancia
    def __init__(self, vars_est, substancia):

        """ Aqui no construtor da classe, as chaves e os valores do dicionário são
        armazenados em duas listas e posteriormente o método identifica pelas chaves
        as propriedades da Substância Pura, podendo ser inseridas em qualquer ordem.

        A lista 'propertys' contem o nome de todas as propriedades que
        podem ser calculadas da Substância Pura.
    
        var_est - Deve ser um dicionário com dois elementos dentre os sete
        listados: 'T','P', 'Q', 'H', 'S', 'U', 'D'
        As chaves de cada um dicionário devem ser um dos caracteres listados
        acima, e o valor associado a cada chave, o respectivo valor da grandeza
        no SI.
        Exemplo var_est: {'T':600, 'P':2000}

        substancia - deve ser uma daquelas implementadas pelo CoolProp.
        """
        
        # Atributos da Classe que serão iniciados pelo "Construtor"
        self._temp = np.nan # Temperatura
        self._press = np.nan # Pressão
        self._titulo = np.nan # Título
        self._entalpia = np.nan # Entalpia
        self._entropia = np.nan # Entropia
        self._energiaInt = np.nan # Energia Interna
        self._volume = np.nan # Volume específico
        self._substancia = substancia # Substância 
        self._estado = np.nan # Estado da Substância Pura   

        # A função abaixo refere-se a conversão do resutados fornecidos pela biblioteca do Coolprop,
        # para o fluido refrigerante R134a.
        CP.set_reference_state('R134a','ASHRAE')

        # A lista "grandezas" possui as Chaves do Dicionário "var_est"
        grandezas = ['T','P', 'Q', 'H', 'S', 'U', 'D']
        # A função "len" permita que o número de variáveis seja alterado
        n_var = len(grandezas)

        # Lista dos atributos da Classe
        atributos = [self._temp, self._press, self._titulo, self._entalpia, 
        self._entropia, self._energiaInt, self._volume, self._substancia,
        self._estado]
        
        # Extrai as "Chaves" e armazena na lista da variável
        var_tipos = list(vars_est.keys())
        # Extrai os "Valores" e armazena na lista da variável
        var_values =  list(vars_est.values())


        # Identifica qual valor (P,T...) da lista "grandezas", está contido 
        # na variavel "var_tipos", e armazena nas variáveis "ind1 e ind2".
        ind1, ind2 = grandezas.index(var_tipos[0]), \
        grandezas.index(var_tipos[1])


        # O "for" testa se "i" é um dos "ind" estabelecidos, se for, 
        # ele armazena o atributo e o valor correspondente.
        for i in range(n_var):
            if i == ind1:
                atributos[i] = var_values[0]
            elif i == ind2:
                atributos[i] = var_values[1]

            # Quando o "else" é executado, a função "PropsSI",
            # pega os valores armazenados da grandeza correspondente ao ind, e a substância estabelecida,
            # e realiza o calcúlo das propriedades termodinâmicas no Sistema internacional.            
            else:
                atributos[i] = PropsSI(
                grandezas[i], var_tipos[0],var_values[0],
                var_tipos[1], var_values[1], self._substancia
                )
                

                # Execução da função "PhaseSI",
                # que pega os valores armazenados da grandeza correspondente ao ind, e a substância estabelecida,
                # e estabelece o "estado" das propriedades termodinâmicas no Sistema internacional.    
                atributos[-1]= PhaseSI(
                var_tipos[0],var_values[0],var_tipos[1], 
                var_values[1], self._substancia)
                
                # Conversão dos nomes das Fases (estado) fornecidas pela função "PhaseSI"
                phases ={'liquid':'Liquido Comprimido',
                'gas':'Vapor Superaquecido',
                'supercritical_gas':'Fluido Supercrítico',
                'supercritical_liquid': 'Fluido Supercrítico',
                0:'Liquido saturado',
                1:'Vapor saturado', 'twophase':'Mistura Saturada'}
                
        for x,y in phases.items():
            if atributos[-1] == x or atributos[2] == x:
                atributos[-1] = y                
                               
                
                # Adaptação da função "PropsSI" para cálculo do "volume específico"
                atributos[6]= 1/(PropsSI(
                grandezas[i], var_tipos[0],var_values[0],var_tipos[1], 
                var_values[1], self._substancia))
                

            # Atualização dos valores "atributos"      
        self._temp,         \
        self._press,        \
        self._titulo,       \
        self._entalpia,     \
        self._entropia,     \
        self._energiaInt,   \
        self._volume,       \
        self._substancia,   \
        self._estado = atributos
            
            
    #Métodos getters

    # Tem como função retornar ao usuário os valores de cada atributo que a instância possui.            

    @property # Torna a Funçao uma propriedade da Classe
    def temperatura(self):
        """Método para retorno da temperatura."""
        return '{} K'.format(round(self._temp),2)

    @property
    def pressao(self):
        """Método para retorno da pressão."""
        return '{} kPa'.format(round(self._press/1000,2))

    @property
    def titulo(self):
        """Método para retorno do título."""
        return '{}'.format(round(self._titulo,2))

    @property
    def entalpia(self):
        """Método para retorno da entalpia."""
        return '{} kJ/kg'.format(round(self._entalpia/1000,2))
    
    @property
    def entropia(self):
        """Método para retorno da entropia."""
        return '{} kJ/kg.K'.format(round(self._entropia/1000,4))
    
    @property
    def energiaInt(self):
        """Método para retorno da energia interna."""
        return '{} kJ/kg'.format(round(self._energiaInt/1000,2))
    
    @property
    def volume(self):
        """Método para retorno do volume especifico."""
        return '{} m\u00b3/kg'.format(round(self._volume,6))
    
    
    # ESTADO
    
    @property
    def estado(self):
        """Método para retorno do estado."""
        return self._estado


    #Métodos setters

    # Para cada "getter" criado, cria-se um respectivo "setter".
    # Determinador de valores. Ele modifica os valores caso necessário.

    @temperatura.setter # "@" - decorador - torna privado

    def temperatura(self, temp): # Recebe o objeto (self) e o valor (P,T,...) a ser modificado.

        """Método para definição e modificação da temperatura."""
        self._temp = temp

    @pressao.setter
    def pressao(self, press):
        """Método para definição e modificação da pressão."""
        self._press = press

    @titulo.setter
    def titulo(self, titulo):
        """Método para definição e modificação do título."""
        self._titulo = titulo

    @entalpia.setter
    def entalpia(self, entalpia):
        """Método para definição e modificação da entalpia."""
        self._entalpia = entalpia
    
    @entropia.setter
    def entropia(self, entropia):
        """Método para definição e modificação da entropia."""
        self._entropia = entropia
        
    @energiaInt.setter
    def energiaInt(self, energiaInt):
        """Método para definição e modificação da energia interna."""
        self._energiaInt = energiaInt
    
    @volume.setter
    def volume(self, volume):
        """Método para definição e modificação do volume."""
        self._volume = volume      
         
    
    # ESTADO
    @estado.setter
    def estado(self, estado):
        """Método para definição e modificação do estado."""
        self._estado = estado

    
    # Metodo público - Transformação da Substância Pura
    # Pega objeto, novo vars_est e as funções,
    # que utilizam como argumento os "setters"
    def transform(
        self, vars_est, funcoes = [temperatura, pressao, titulo, 
        entalpia, entropia, energiaInt]):
      
        """Recebe um dicionário com valores a serem modificados na função com
        as variáveis determinadas pelas strings nas chaves."""

        grandezas = ['T','P', 'Q', 'H', 'S', 'U','D']
        n_var = len(grandezas)


        var_tipos = list(vars_est.keys())
        var_values =  list(vars_est.values())


        # VALIDAÇÃO

        try:
            if (
            (len(vars_est)!=2)                      \
            and ((var_tipos[0] not in grandezas)   \
            and (var_tipos[1] not in grandezas))
            ):
                raise ValueError

        except ValueError:
            print("*****ERRO!*****\n A função não deve receber mais que duas"\
            + " grandezas. Apenas as chaves T, P, Q, H, S, U e D devem ser usadas para"\
            +" identificá-las.")

        else:
            atributos = [self._temp, self._press, self._titulo, self._entalpia, 
        self._entropia, self._energiaInt]

            for i,j in zip(grandezas, range(len(grandezas))):
                if i != var_tipos[0] and i != var_tipos[1]:
                    atributos[j]= PropsSI(
                        grandezas[j], var_tipos[0],var_values[0],
                        var_tipos[1], var_values[1], self._substancia
                        )
                  
                else:
                    atributos[j] = var_values[j]
                   
            # Atualização dos valores "atributos"  
            self._temp,         \
            self._press,        \
            self._titulo,       \
            self._entalpia,     \
            self._entropia,     \
            self._energiaInt = atributos   
            
            # Fim da Transformação  
