from Classe_Substancia_pura import SubstanciaPura
from Classe_Ciclo_Rankine import Rankine_Simples_pt,Rankine_Reaquecimento_pt,Rankine_Regeneracao_pt
from Classe_Ciclo_Rankine_plots import Rankine_Simples_plots,Rankine_Reaquecimento_plots,Rankine_Regeneracao_plots
from Classe_Gas_ideal import Gases_ideais_lemmon
from bokeh.plotting import figure, output_file, show


import eel

eel.init("Interfaces")

@eel.expose
def Get_Rankine_Regeneracao_plots_ts(p1_rg,p2_rg,p4_rg,t5_rg,fluid_type_rg):
    p1_rg = float(p1_rg)*1000
    p2_rg= float(p2_rg)*1000
    p4_rg = float(p4_rg)*1000
    output_file(filename="Rankine_reg_ts.html")      
    eel.showAnswers(show(Rankine_Regeneracao_plots({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).plot_ts))

@eel.expose
def Get_Rankine_Regeneracao_plots_pv(p1_rg,p2_rg,p4_rg,t5_rg,fluid_type_rg):
    p1_rg = float(p1_rg)*1000
    p2_rg = float(p2_rg)*1000
    p4_rg = float(p4_rg)*1000
    output_file(filename="Rankine_reg_pv.html")      
    eel.showAnswers(show(Rankine_Regeneracao_plots({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).plot_pv))

@eel.expose
def Get_Rankine_Reaquecimento_plots_ts(p1_rq,p2_rq,t3_rq,p4_rq,fluid_type_rq):
    p1_rq = float(p1_rq)*1000
    p2_rq = float(p2_rq)*1000
    p4_rq = float(p4_rq)*1000
    output_file(filename="Rankine_reaq_ts.html")      
    eel.showAnswers(show(Rankine_Reaquecimento_plots({'P1':float(p1_rq),'P2':float(p2_rq),'T3':float(t3_rq),'P4':float(p4_rq)},fluid_type_rq).plot_ts))

@eel.expose
def Get_Rankine_Reaquecimento_plots_pv(p1_rq,p2_rq,t3_rq,p4_rq,fluid_type_rq):
    p1_rq = float(p1_rq)*1000
    p2_rq = float(p2_rq)*1000
    p4_rq = float(p4_rq)*1000
    output_file(filename="Rankine_reaq_pv.html")      
    eel.showAnswers(show(Rankine_Reaquecimento_plots({'P1':float(p1_rq),'P2':float(p2_rq),'T3':float(t3_rq),'P4':float(p4_rq)},fluid_type_rq).plot_pv))

@eel.expose
def Get_Rankine_Simples_plots_ts(p1_rs,p2_rs,t3_rs,fluid_type_rs):
    p1_rs = float(p1_rs)*1000
    p2_rs = float(p2_rs)*1000
    output_file(filename="Rankine_simples_ts.html")      
    eel.showAnswers(show(Rankine_Simples_plots({'P1':float(p1_rs), 'P2':float(p2_rs),'T3':float(t3_rs)},fluid_type_rs).plot_ts))

@eel.expose
def Get_Rankine_Simples_plots_pv(p1_rs,p2_rs,t3_rs,fluid_type_rs):
    p1_rs = float(p1_rs)*1000
    p2_rs = float(p2_rs)*1000
    output_file(filename="Rankine_simples_pv.html")      
    eel.showAnswers(show(Rankine_Simples_plots({'P1':float(p1_rs), 'P2':float(p2_rs),'T3':float(t3_rs)},fluid_type_rs).plot_pv))



@eel.expose
def Get_SubstanciaPura(prop1_type,prop1_value,prop2_type,prop2_value,fluid_type):
    if prop1_type == 'D':
        prop1_value = 1/prop1_value
    elif prop2_type == 'D':
        prop2_value = 1/prop2_value
    elif prop1_type == 'P':
        prop1_value = 1000*float(prop1_value)
    elif prop2_type == 'P':
        prop2_value = 1000*float(prop2_value)
    else:
        prop1_value = prop1_value
        prop2_value = prop2_value
    
    data = {}
    data.update({"Temperatura":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).temperatura})
    data.update({"Pressão":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).pressao})
    data.update({"Entalpia":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).entalpia})
    data.update({"Entropia":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).entropia})
    data.update({"Energia Interna":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).energiaInt})
    data.update({"Volume Específico":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).volume})
    data.update({"Estado":SubstanciaPura({prop1_type:float(prop1_value),prop2_type:float(prop2_value)},fluid_type).estado})
    return data




@eel.expose
def Get_Rankine_Simples(p1_rs,p2_rs,t3_rs,fluid_type_rs):

    p1_rs = float(p1_rs)*1000
    p2_rs = float(p2_rs)*1000
    data = {}
    data.update({"Trabalho específico":Rankine_Simples_pt({'P1':float(p1_rs), 'P2':float(p2_rs),'T3':float(t3_rs)},fluid_type_rs).trabalho})
    data.update({"Eficiência":Rankine_Simples_pt({'P1':float(p1_rs), 'P2':float(p2_rs),'T3':float(t3_rs)},fluid_type_rs).eficiencia})
    data.update({"Calor Fornecido":Rankine_Simples_pt({'P1':float(p1_rs), 'P2':float(p2_rs),'T3':float(t3_rs)},fluid_type_rs).calor_fornecido})
    data.update({"Calor Perdido":Rankine_Simples_pt({'P1':float(p1_rs), 'P2':float(p2_rs),'T3':float(t3_rs)},fluid_type_rs).calor_perdido})
    return data


@eel.expose
def Get_Rankine_Reaq(p1_rq,p2_rq,t3_rq,p4_rq,fluid_type_rq):

    p1_rq = float(p1_rq)*1000
    p2_rq = float(p2_rq)*1000
    p4_rq = float(p4_rq)*1000
    data = {}
    data.update({"Trabalho específico":Rankine_Reaquecimento_pt({'P1':float(p1_rq), 'P2':float(p2_rq),'T3':float(t3_rq),'P4':float(p4_rq)},fluid_type_rq).trabalho})
    data.update({"Eficiência":Rankine_Reaquecimento_pt({'P1':float(p1_rq),'P2':float(p2_rq),'T3':float(t3_rq),'P4':float(p4_rq)},fluid_type_rq).eficiencia})
    data.update({"Calor Fornecido":Rankine_Reaquecimento_pt({'P1':float(p1_rq), 'P2':float(p2_rq),'T3':float(t3_rq),'P4':float(p4_rq)},fluid_type_rq).calor_fornecido})
    data.update({"Calor Perdido":Rankine_Reaquecimento_pt({'P1':float(p1_rq), 'P2':float(p2_rq),'T3':float(t3_rq),'P4':float(p4_rq)},fluid_type_rq).calor_perdido})
    #data.update({"Gráfico":Rankine_Simples_pt({'P1':float(p1), 'P2':float(p2),'T3':float(t3)},fluid_type).plots})
    
    return data
 
@eel.expose
def Get_Rankine_Reg(p1_rg,p2_rg,p4_rg,t5_rg,fluid_type_rg):

    p1_rg = float(p1_rg)*1000
    p2_rg = float(p2_rg)*1000
    p4_rg = float(p4_rg)*1000
    data = {}
    data.update({"Trabalho específico":Rankine_Regeneracao_pt({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).trabalho})
    data.update({"Eficiência":Rankine_Regeneracao_pt({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).eficiencia})
    data.update({"Calor Fornecido":Rankine_Regeneracao_pt({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).calor_fornecido})
    data.update({"Calor Perdido":Rankine_Regeneracao_pt({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).calor_perdido})
    data.update({"Fração de vapor extraído da turbina":Rankine_Regeneracao_pt({'P1':float(p1_rg), 'P2':float(p2_rg),'P4':float(p4_rg),'T5':float(t5_rg)},fluid_type_rg).frac_vapor})
    
    return data
 
@eel.expose
def Get_Gas_Ideal(temp,press):

    press = float(press)*1000
    data = {}
    data.update({"Temperatura":Gases_ideais_lemmon(float(temp),float(press)).temperatura})
    data.update({"Pressão":Gases_ideais_lemmon(float(temp),float(press)).pressao})
    data.update({"Energia Interna":Gases_ideais_lemmon(float(temp),float(press)).energia_interna})
    data.update({"Entalpia":Gases_ideais_lemmon(float(temp),float(press)).entalpia})
    data.update({"Entropia":Gases_ideais_lemmon(float(temp),float(press)).entropia})
    data.update({"Calor Específico (volume constante)":Gases_ideais_lemmon(float(temp),float(press)).calor_especifico_cv})
    data.update({"Calor Específico (pressão constante)":Gases_ideais_lemmon(float(temp),float(press)).calor_especifico_cp})
   # data.update({"Pressão Reduzida":Gases_ideais_lemmon(float(temp),float(press)).pressao_reduzida})
   # data.update({"Volume Reduzido":Gases_ideais_lemmon(float(temp),float(press)).volume_reduzido})
    data.update({"Velocidade do som":Gases_ideais_lemmon(float(temp),float(press)).velocidade_do_som})
    
    
    return data
 

eel.start("index.html",size=(1000,1000))



