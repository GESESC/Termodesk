function setupTabs (){
    document.querySelectorAll(".tabs-button").forEach( button => {
        button.addEventListener("click", () =>{
            const sideBar = button.parentElement
            const tabsContainer = sideBar.parentElement
            const tabNumber = button.dataset.forTab
            const tabToActivate = tabsContainer.querySelector(`.tabs-content[data-tab="${tabNumber}"]`)

            sideBar.querySelectorAll(".tabs-button").forEach(button => {
                button.classList.remove("tabs-button-active")
            })
            tabsContainer.querySelectorAll(".tabs-content").forEach(tab => {
                tab.classList.remove("tabs-content-active")
            })
            button.classList.add("tabs-button-active")
            tabToActivate.classList.add("tabs-content-active")
        })
    })
}

document.addEventListener("DOMContentLoaded", ()=>{
    setupTabs()
})


function Get_Rankine_Regeneracao_plots_ts() {
	var p1_rg = document.getElementById("p1_rg").value
	p2_rg = document.getElementById("p2_rg").value
	p4_rg= document.getElementById("p4_rg").value
	t5_rg = document.getElementById("t5_rg").value
	fluid_type_rg = document.getElementById("fluid_type_rg").value
	eel.Get_Rankine_Regeneracao_plots_ts(p1_rg,p2_rg,p4_rg,t5_rg,fluid_type_rg);
	}

function Get_Rankine_Regeneracao_plots_pv() {
	var p1_rg = document.getElementById("p1_rg").value
	p2_rg = document.getElementById("p2_rg").value
	p4_rg= document.getElementById("p4_rg").value
	t5_rg = document.getElementById("t5_rg").value
	fluid_type_rg = document.getElementById("fluid_type_rg").value
	eel.Get_Rankine_Regeneracao_plots_pv(p1_rg,p2_rg,p4_rg,t5_rg,fluid_type_rg);
	}

function Get_Rankine_Reaquecimento_plots_ts() {
	var p1_rq = document.getElementById("p1_rq").value
	p2_rq = document.getElementById("p2_rq").value
	t3_rq= document.getElementById("t3_rq").value
	p4_rq = document.getElementById("p4_rq").value
	fluid_type_rq = document.getElementById("fluid_type_rq").value
	eel.Get_Rankine_Reaquecimento_plots_ts(p1_rq,p2_rq,t3_rq,p4_rq,fluid_type_rq);
	}

function Get_Rankine_Reaquecimento_plots_pv() {
	var p1_rq = document.getElementById("p1_rq").value
	p2_rq = document.getElementById("p2_rq").value
	t3_rq= document.getElementById("t3_rq").value
	p4_rq = document.getElementById("p4_rq").value
	fluid_type_rq = document.getElementById("fluid_type_rq").value
	eel.Get_Rankine_Reaquecimento_plots_pv(p1_rq,p2_rq,t3_rq,p4_rq,fluid_type_rq);
	}


function Get_Rankine_Simples_plots_ts() {
	var p1_rs = document.getElementById("p1_rs").value
	p2_rs = document.getElementById("p2_rs").value
	t3_rs= document.getElementById("t3_rs").value
	fluid_type_rs = document.getElementById("fluid_type_rs").value
	eel.Get_Rankine_Simples_plots_ts(p1_rs,p2_rs,t3_rs,fluid_type_rs);
	}

function Get_Rankine_Simples_plots_pv() {
		var p1_rs = document.getElementById("p1_rs").value
		p2_rs = document.getElementById("p2_rs").value
		t3_rs= document.getElementById("t3_rs").value
		fluid_type_rs = document.getElementById("fluid_type_rs").value
		eel.Get_Rankine_Simples_plots_pv(p1_rs,p2_rs,t3_rs,fluid_type_rs);
	}

eel.expose(showAnswers);
	function showAnswers(answer) {
		var outputDiv = document.getElementById("result");
		outputDiv.innerHTML =  answer;
	}

// RESULTADO SubstanciaPura
async function Get_SubstanciaPura(){
	var prop1_type = document.getElementById("prop1_type").value
	prop1_value = document.getElementById("prop1_value").value
	prop2_type = document.getElementById("prop2_type").value
	prop2_value = document.getElementById("prop2_value").value
	fluid_type = document.getElementById("fluid_type").value

	document.body.innerHTML="";

	let n = await eel.Get_SubstanciaPura(prop1_type,prop1_value,prop2_type,prop2_value,fluid_type)();

	var div = document.createElement("div");
	div.setAttribute("class","output");
	document.body.appendChild(div);

	var divInterna = document.createElement("div");
	divInterna.setAttribute("class","div-interna");
	div.appendChild(divInterna);

	var p = document.createElement("h2");
	p.setAttribute("style","text-align: center; padding-bottom: 20px;");
	var t = document.createTextNode("Propriedades:");
	p.appendChild(t);
	divInterna.appendChild(p);
	var table = document.createElement("table");
	
	var i=0;
	for (const[key,value] of Object.entries(n)){
		var row=table.insertRow(i)
		var cell1=row.insertCell(0)
		var cell2=row.insertCell(1)
		cell1.innerHTML=key;
		cell2.innerHTML=value;
		divInterna.appendChild(table);
		i=i+1;

	}
   var button = document.createElement("button")
   button.setAttribute("class","button-primary");
   button.innerHTML="<i class='fa fa-arrow-left'></i> Voltar"
   button.onclick=function(){
	   window.location.replace("index.html");
   }
   divInterna.appendChild(button);			   
}
// RESULTADO Substancia Pura


async function Get_Rankine_Simples(){
	var p1_rs = document.getElementById("p1_rs").value
	p2_rs = document.getElementById("p2_rs").value
	t3_rs= document.getElementById("t3_rs").value
	fluid_type_rs = document.getElementById("fluid_type_rs").value
	
	document.body.innerHTML="";

	let n =await eel.Get_Rankine_Simples(p1_rs,p2_rs,t3_rs,fluid_type_rs)();
	
	var div=document.createElement("div");
	div.setAttribute("class","output");
	document.body.appendChild(div);

	var divInterna = document.createElement("div");
	divInterna.setAttribute("class","div-interna");
	div.appendChild(divInterna);
	
	var p=document.createElement("h2");
	p.setAttribute("style","text-align: center; padding-bottom: 20px;");
	var t = document.createTextNode("Resultado:");
	p.appendChild(t);
	divInterna.appendChild(p);
	var table=document.createElement("table");

	var i=0;
	for (const[key,value] of Object.entries(n)){
		var row=table.insertRow(i)
		var cell1=row.insertCell(0)
		var cell2=row.insertCell(1)
		cell1.innerHTML=key;
		cell2.innerHTML=value;
		divInterna.appendChild(table);
		i=i+1;

	}
   var button = document.createElement("button")
   button.setAttribute("class","button-primary");
   button.innerHTML="<i class='fa fa-arrow-left'></i> Voltar"
   button.onclick=function(){
	   window.location.replace("index.html");
   }

   divInterna.appendChild(button);

}
			  

async function Get_Rankine_Reaq(){
	var p1_rq = document.getElementById("p1_rq").value
	p2_rq = document.getElementById("p2_rq").value
	t3_rq= document.getElementById("t3_rq").value
	p4_rq = document.getElementById("p4_rq").value
	fluid_type_rq = document.getElementById("fluid_type_rq").value
	
	document.body.innerHTML="";

	let n =await eel.Get_Rankine_Reaq(p1_rq,p2_rq,t3_rq,p4_rq,fluid_type_rq)();
	
	var div=document.createElement("div");
	div.setAttribute("class","output");
	document.body.appendChild(div);

	var divInterna = document.createElement("div");
	divInterna.setAttribute("class","div-interna");
	div.appendChild(divInterna);

	var p = document.createElement("h2");
	p.setAttribute("style","text-align: center; padding-bottom: 20px;");
	var t=document.createTextNode("Resultado:");
	p.appendChild(t);
	divInterna.appendChild(p);
	var table=document.createElement("table");

	var i=0;
	for (const[key,value] of Object.entries(n)){
		var row=table.insertRow(i)
		var cell1=row.insertCell(0)
		var cell2=row.insertCell(1)
		cell1.innerHTML=key;
		cell2.innerHTML=value;
		divInterna.appendChild(table);
		i=i+1;

	}
   var button = document.createElement("button")
   button.setAttribute("class","button-primary");
   button.innerHTML="<i class='fa fa-arrow-left'></i> Voltar"
   button.onclick=function(){
	   window.location.replace("index.html");
   }

   divInterna.appendChild(button);

}



async function Get_Rankine_Reg(){
	var p1_rg = document.getElementById("p1_rg").value
	p2_rg = document.getElementById("p2_rg").value
	p4_rg= document.getElementById("p4_rg").value
	t5_rg = document.getElementById("t5_rg").value
	fluid_type_rg = document.getElementById("fluid_type_rg").value
	
	document.body.innerHTML="";
	
	let n =await eel.Get_Rankine_Reg(p1_rg,p2_rg,p4_rg,t5_rg,fluid_type_rg)();
	
	var div=document.createElement("div");
	div.setAttribute("class","output");
	document.body.appendChild(div);

	var divInterna = document.createElement("div");
	divInterna.setAttribute("class","div-interna");
	div.appendChild(divInterna);

	var p = document.createElement("h2");
	p.setAttribute("style","text-align: center; padding-bottom: 20px;");
	var t=document.createTextNode("Resultado:");
	p.appendChild(t);
	divInterna.appendChild(p);
	var table=document.createElement("table");

	var i=0;
	for (const[key,value] of Object.entries(n)){
		var row=table.insertRow(i)
		var cell1=row.insertCell(0)
		var cell2=row.insertCell(1)
		cell1.innerHTML=key;
		cell2.innerHTML=value;
		divInterna.appendChild(table);
		i=i+1;

	}
	var button = document.createElement("button")
	button.setAttribute("class","button-primary");
	button.innerHTML="<i class='fa fa-arrow-left'></i> Voltar"
   button.onclick=function(){
	   window.location.replace("index.html");
   }

   divInterna.appendChild(button);

}

/// RESULTADO GAS IDEAL
async function Get_Gas_Ideal(){
	var temp = document.getElementById("temp").value
	press = document.getElementById("press").value

	document.body.innerHTML="";

	let n =await eel.Get_Gas_Ideal(temp,press)();

	var div=document.createElement("div");
	div.setAttribute("class","output");
	document.body.appendChild(div);

	var divInterna = document.createElement("div");
	divInterna.setAttribute("class","div-interna");
	div.appendChild(divInterna);

	var p=document.createElement("h2");
	p.setAttribute("style","text-align: center; padding-bottom: 20px;");
	var t=document.createTextNode("Propriedades:");
	p.appendChild(t);
	divInterna.appendChild(p);
	var table=document.createElement("table");

	var i=0;
	for (const[key,value] of Object.entries(n)){
		var row=table.insertRow(i)
		var cell1=row.insertCell(0)
		var cell2=row.insertCell(1)
		cell1.innerHTML=key;
		cell2.innerHTML=value;
		divInterna.appendChild(table);
		i=i+1;

	}
   var button=document.createElement("button")
   button.setAttribute("class","button-primary");
   button.innerHTML="<i class='fa fa-arrow-left'></i> Voltar"
   button.onclick=function(){
	   window.location.replace("index.html");
   }

   divInterna.appendChild(button);	
			   
}

function recarrega(){
    window.location.href = "index.html"
}


/// RESULTADO GAS IDEAL