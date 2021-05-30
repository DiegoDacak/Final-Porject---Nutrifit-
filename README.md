# Nutrifit
#### Video Demo:  https://youtu.be/zHUGAqyvBlk
#### Description:
Nutrifit is a web page that is meant to help you to have a healthy life. The web page helps you counting calories and proteins of whatever you eat during a day, so you can have a better control over what you eat.
#### Templates
**Template “layout.html”:** This template has the layout base of the entire web page. After logging, at any moment inside the page this template gives the possibility to click at the username, then a window will be to open where you can change any of your profile’s information, you also can add a calorie and protein goal. This template also provides a “loading spin” that appears when page is loading, and disappears when load is completed. We have four functions written in javascript language at this template:
1.	Function “carga completa”: Shows the spinner during the page loading and hides once load is completed.
2.	Function “mostrar_datos”: Shows the user data if the user clicks at the username.
3.	Function “ocultar_datos”: If the user clicks in “cerrar” while the window of the profile’s information is open, this function is going to close (hide) this information again.
4.	Function “habilitar_cambio”: Once the profile's information windows is open, the user may edit any of his/her profiles data, even could add a protein and calorie goal; he/she could allow this function by clicking a checkbox. This tool allows the user to make any update or reset at the profile data.

**Template “index.html”:** At this template the user can add any food to his records or reset all and start again. The user will be able to get information about total calorie and protein that he/she ate. If the user already has a calory or protein goal, he/she will be advised about how is going the goal accomplishment.  We have four functions written in javascript lenguage in this template:
1.	Function “utilizar_recetas()”: This function allows the user to change between the recipe library and the food library, with a check box.
2.	Function “funcion_unidad()”: This function is in charge of choosing the correct unit of measure when a food is selected. This unit of measure is going to be the unit that the user choses hen creates the meal.
3.	Function “restantes_calorias()”: If the user ads a calorie to his profile, this function calculates the number of calorie that user needs to consume in order to accomplish his/her objective or if he/she is already overshoot, according to the records.
4.	Function “restantes_proteinas()”: If the user ads a protein to his profile, this function calculates the number of protein that user needs to consume in order to accomplish his/her objective or if he/she is already overshoot, according to the records.

**Template “registro.html”:** At this tempplate you must create an account and add all the user information. If you try to use a username that is already used or if your confirmation password is not the same that your registered password; you are going to be advice with a “text alert”. Once the user profile is successfully created, you are going to be redirected to the “login.html” template along with a text alert that informs the success of this procedure.

**Template “login.html”:** Once the user profile is created, the user can log in. At this point the user must chose a username and its password; if there is any problem such us the password or username are not correct, even if the user mistypes the username or password, the web page will show a red text alert warning the mistake.

**Template “alimento.html”:** This is the user’s personal food library. The user can check and add any food to that library. In order to add a new food, there are some information requested by the web page: 1) The name of the food. 2) An URL of the image of the food. 3) The unit of measure (gr, kg, unit, etc.). 4) The portion. 5) Calorie. 6) Protein. The number of calories and proteins are based on the portion quantities.

**Template “recetas.html”:** This is the user’s personal recipe library. The user can check and create any recipe combination within the foods already added to the food library. In order to create a new recipe, there are some information requested by the web page: 1) The name of the recipe. 2) An URL of the image of the recipe. 3) How many portions is going to have the recipe. 4) The meals that composes the recipe. We can add how many meals or ingredients we want. The user needs to specify the meal and the portion of this meal, the portion is going have a particular unit of measure depending on the food choose, and the unit of measure used at the moment of creation. Once you add a recipe you can view each ingredient and the portion of each one if you click at the image of the recipe. We have four functions written in javascript lenguage in this template:
1.	Function “mostrar_ingredientes (receta_buscada)”: The function gives the user the possibility to click at any recipe and check a window with the ingredients of the recipe. The function's argument is the id of the recipe from we want to know the ingredients.
2.	Function “agregar_ingrediente()”: When the user creates a new recipe, this function gives the possibility to add any ingredient the user wants.
3.	Function “unidad_medida(ingrediente_id)”: When the user creates a new recipe, and ads new ingredients, the user may choose what ingredient he wants to add, and this function is in charge of select the correct unit of measured for that ingredient. The function’s argument is the id of the ingredient.
4.	Function “unidad(alimento)”: This function is used by the function in 1), the function's argument is an ingredient and the return is the unit of measure of that ingredient.

**Template “calculate.html”:** In this template the user may calculate the number of protein and calorie that must consume in base of his age, sex, height, weight and activity. At this template, the user can obtain the number of protein and calory goal in order to add this information at his/her profile data.

#### Static

**background-image:** This is the image that use all the templates like background image.

**java.js:** We have four functions written in javascript lenguage:
1.	Function “abrir_forma()”: This function is in charge to show the adding food or recipe form to the “alimento.html” or “recipe.html” template.
2.	Function “cerrar_forma()”: This function is in charge to hide the adding food or recipe form to the “alimento.html”  or “recipe.html” template.
3.	Function “ocultar_ingredientes()”: This function is in charge to hide the ingredients window.
4.	Function “calcular_calorias()”: This is the function in charge to make the calculation that template “calculate.html” needs in order to show the number of protein and calory that the user must consume.

**style.css:** This file gives style to the web page. Here we have the css code that most templates uses, and here we also may create the loading spinner.
