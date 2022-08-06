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
      
class Rankine_Simples_pt(Ciclo_Rankine_pt):
  
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

    # Trabalho da bomba
    self.Wb = self.h2 - self.h1

    # Trabalho da turbina        
    self.wt = (self.h3 -self.h4)

    # Calor fornecido pela caldeira        
    self.Qe = self.h3 - self.h2

    # Calor perdido      
    self.Qs = self.h4 - self.h1
            
     # Eficiência do ciclo       
    self.nt = (1 - (self.Qs/self.Qe)) * 100


  @property # Torna a Funçao uma propriedade da Classe
  def eficiencia(self):
      """Método para retorno da eficiencia"""
      return "{:.1f}%".format(self.nt)

  @property # Torna a Funçao uma propriedade da Classe
  def trabalho(self):
      """Método para retorno do trabalho"""
      return "{:.2f} kJ/kg".format(self.wt/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def calor_fornecido(self):
      """Método para retorno do Calor fornecido pela caldeira"""
      return "{:.2f} kJ/kg".format(self.Qe/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def calor_perdido(self):
      """Método para retorno do calor perdido"""
      return "{:.2f} kJ/kg".format(self.Qs/1000)

 
class Rankine_Reaquecimento_pt(Ciclo_Rankine_pt):

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

    # Trabalho da bomba
    self.Wb = self.h2 - self.h1

    # Trabalho da turbina        
    self.wt = (self.h3 - self.h4) + (self.h5 - self.h6)

    # Calor fornecido pela caldeira        
    self.Qe = (self.h3 - self.h2) + (self.h5 - self.h4)

    # Calor perdido        
    self.Qs = self.h6 - self.h1

    # Eficiência do ciclo       
    self.nt = (1 - (self.Qs/self.Qe)) * 100


    

  @property # Torna a Funçao uma propriedade da Classe
  def eficiencia(self):
    """Método para retorno da eficiencia"""
    return "{:.1f}%".format(self.nt)

  @property # Torna a Funçao uma propriedade da Classe
  def trabalho(self):
    """Método para retorno do trabalho"""
    return "{:.2f} kJ/kg".format(self.wt/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def calor_fornecido(self):
    """Método para retorno do Calor fornecido pela caldeira"""
    return "{:.2f} kJ/kg".format(self.Qe/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def calor_perdido(self):
    """Método para retorno do calor perdido"""
    return "{:.2f} kJ/kg".format(self.Qs/1000)
 

class Rankine_Regeneracao_pt(Ciclo_Rankine_pt):

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


    # Fração de vapor extraída da turbina
    self.y = (self.h3 - self.h2)/(self.h6 - self.h2)

    # Trabalho da bomba 1      
    self.Wb1 = self.h2 - self.h1

    # Trabalho da bomba 2        
    self.Wb2 = self.h4 - self.h3

    # Trabalho total das duas bombas          
    self.Wb = ((1 - self.y) * self.Wb1) + self.Wb2

    # Trabalho da turbina       
    self.wt = (self.h5 - self.h6) + ((1 - self.y) * (self.h6 - self.h7))

    # Calor fornecido para caldeira        
    self.Qe = self.h5 - self.h4

    # Calor perdido       
    self.Qs = (1 - self.y) * (self.h7 - self.h1)

    # Eficiência do ciclo        
    self.nt = (1 - (self.Qs/self.Qe)) * 100
  
  

    
  @property # Torna a Funçao uma propriedade da Classe
  def eficiencia(self):
    """Método para retorno da eficiencia"""
    return "{:.1f}%".format(self.nt)

  @property # Torna a Funçao uma propriedade da Classe
  def trabalho(self):
    """Método para retorno do trabalho"""
    return "{:.2f} kJ/kg".format(self.wt/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def calor_fornecido(self):
    """Método para retorno do Calor fornecido pela caldeira"""
    return "{:.2f} kJ/kg".format(self.Qe/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def calor_perdido(self):
    """Método para retorno do calor perdido"""
    return "{:.2f} kJ/kg".format(self.Qs/1000)

  @property # Torna a Funçao uma propriedade da Classe
  def frac_vapor(self):
    """Método para retorno da fracao de vapor"""
    return "{:.2f} %".format(self.y*100)

 