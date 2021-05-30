// Variable global
var counter = 1;
var counter_ing = 1;

function abrir_forma() {
    document.getElementById("overlay").classList.add("active");
}

function cerrar_forma() {
    document.getElementById("overlay").classList.remove("active");
    document.getElementById("forma").reset();
    document.getElementById("unidad_ingrediente_1").innerHTML = "";
    while (counter != 1) {
        document.getElementById("ingredientes").removeChild(document.getElementById("padre"));
        counter--;
    }
}

function ocultar_ingredientes() {
    counter_ing = 1;
    document.getElementById("overlay_2").classList.remove("active");
    while (document.getElementById("tabla_ingredientes").childNodes.length != 0) {
        document.getElementById("tabla_ingredientes").removeChild(document.getElementById("tabla_ingredientes").childNodes[0]);
    }
}


function calcular_calorias() {
            var mantener_peso = document.getElementById("mantener_peso");
            var perder_peso_1 = document.getElementById("perder_peso_1");
            var perder_peso_2 = document.getElementById("perder_peso_2");
            var proteina = document.getElementById("proteinas_calculo");
            var edad = document.getElementById("edad").value;
            var estatura = document.getElementById("estatura").value;
            var peso = document.getElementById("peso").value;
            var actividad = document.getElementById("actividad").value;
            var act = 0;
            if (actividad == "Poco o nada de ejercicio") {
                act = 1.2;
            }
            else if (actividad == "Poco ejercicio (1-3 días a la semana)") {
                act = 1.375;
            }
            else if (actividad == "Promedio (3-5 días a la semana)") {
                act = 1.55;
            }
            else if (actividad == "Mucho ejercicio (6-7 días a la semana)") {
                act = 1.725;
            }
            else if (actividad == "Muy pesado (dos veces al día)") {
                act = 1.9;
            }
            var x = 0;
            // Si es hombre
            if (document.getElementById("hombre").checked == true) {
                x = (10*peso) + (6.25*estatura) - (5*edad) + 5;
                x = x*act;
                x = Math.round(x);
            }
            // Si es mujer
            else if (document.getElementById("mujer").checked == true) {
                x = (10*peso) + (6.25*estatura) - (5*edad) - 161;
                x = x*act;
                x = Math.round(x);
            }
            if (edad == "" || peso == "" || estatura == "" || x == 0 ) {
                mantener_peso.innerHTML = "&nbspFaltan Datos";
                perder_peso_1.innerHTML = "&nbspFaltan Datos";
                perder_peso_2.innerHTML = "&nbspFaltan Datos";
                proteina.innerHTML = "&nbspFaltan Datos";
                return false;
            }
            else {
                if (isNaN(x)) {
                    mantener_peso.innerHTML = "&nbspDato/s mal ingresados";
                    perder_peso_1.innerHTML = "&nbspDato/s mal ingresados";
                    perder_peso_2.innerHTML = "&nbspDato/s mal ingresados";
                    proteina.innerHTML = "&nbspDato/s mal ingresados";
                    return false;
                }
                mantener_peso.innerHTML = "&nbsp" + x + "(kcal)";
                perder_peso_1.innerHTML = "&nbsp" + (x - 500) + "(kcal)";
                perder_peso_2.innerHTML = "&nbsp" + (x - 1000) + "(kcal)";
                x = peso * 1.5;
                x = Math.round(x);
                proteina.innerHTML = "&nbsp" + x + "(gr)"
                return true;
            }
        }