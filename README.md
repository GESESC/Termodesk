# Termodesk
Simulador computacional didático para disciplinas das áreas de termofluidos

Este repositório contém o código desenvolvimento de um simulador
didático computacional para as áreas de Termofluidos, com o objetivo principal de servir como
ferramenta confiável para obtenção de propriedades termodinâmicas de substâncias puras e
de gás ideal do ar. A ideia surgiu da falta de praticidade para obter tais propriedades sem a
necessidade de uso de softwares pagos.

Pensando nisso, um software foi idealizado  para trazer uma solução automatizada para obter as principais propriedades termodinâmicas
de fluidos em uma interface simples com foco na experiência do usuário. A arquitetura do
software chamado de Termodesk consiste em uma aplicação de desktop desenvolvida com back
end em Python, responsável por todos os cálculos termodinâmicos e também pela importação
das bibliotecas consagradas Coolprop e PYroMat, fundamentais para este projeto. A interface ou
front end foi construída com ferramentas de desenvolvimento web (HTML,JavaScript e CSS),
além do framework EEL JS que estrutura toda a comunicação da interface para o back end. 

Arquitetura
<img src="https://github.com/douglas-dm9/Termodesk/blob/main/images-in-readme/arquitetura.PNG"/>

Com a tecnologia definida, cinco funcionalidades foram desenvolvidas: propriedades de substâncias
puras, propriedades do ar como gás ideal e também o cálculo e plotagem dos diagramas T-s e P-v
dos principais tipos de ciclo Rankine ideal (Simples, com Regeneração e com Reaquecimento).
Todas as funcionalidades foram exaustivamente validadas por meio das bibliografias consagradas
da Termodinâmica com seus exemplos e exercícios práticos, mostrando uma excelente confiabilidade
nos cálculos. 


Tela inicial de propriedades de substância pura
<img src="https://github.com/douglas-dm9/Termodesk/blob/main/images-in-readme/tela_1.png"/>

Resultado para 3 substâncias diferentes 

<img src="https://github.com/douglas-dm9/Termodesk/blob/main/images-in-readme/subs_result_a.png" width="300" heigth = "400"  /> <img src="https://github.com/douglas-dm9/Termodesk/blob/main/images-in-readme/subs_result_b.png" width="300" heigth = "400"  /> <img src="https://github.com/douglas-dm9/Termodesk/blob/main/images-in-readme/subs_result_c.png" width="300" heigth = "400" />

Diagrama Pressão-volume específico (P-v)

<img src="https://github.com/douglas-dm9/Termodesk/blob/main/images-in-readme/rankine_simples_result_chart_a.png" />

Link da primei versão do Termodesk. A distribuição do software por enquanto é compatível apenas  com o sistema operacional Windows 10 de 64 bits, com objetivo de migrar para uma versão web no futuro.
A pasta contém todos os arquivos necessários para o software, e dentro dela, há um arquivo com extensão .exe  e nome Termodesk para executá-lo.

[Link da pasta no Google Drive](https://drive.google.com/drive/folders/1by3G7LK-Rsh9Ap_l4RsRNwkVwk3NV3Yw?usp=sharing)
