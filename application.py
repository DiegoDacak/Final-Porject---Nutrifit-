from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functions import login_required
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash


# Configuramos la aplicacion
app = Flask(__name__)


# Nos aseguramos que las plantillas se auto-recarguen
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configuramos la sesion para usar el filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configuramos la libreria CS50 para usar SQLite database
db = SQL("sqlite:///database.db")


@app.context_processor
def context_processor():
    user = {}
    if session:
        row = db.execute("SELECT * FROM users WHERE id = ?", session["id"])
        user = row[0]
    return user


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':

        # Si se introdujeron los datos de un alimento
        if request.form.get("porcion_comida") and request.form.get("comida"):
            portion = float(request.form.get("porcion_comida"))
            # Cantidad de calorias
            calorie = db.execute("SELECT calorie FROM foods WHERE user_id = ? AND food = ?",
                                 session['id'], request.form.get("comida"))
            calorie = float(calorie[0]['calorie'])
            calorie = calorie*portion
            calorie = "{:.2f}".format(calorie)

            # Cantidad de proteinas
            protein = db.execute("SELECT protein FROM foods WHERE user_id = ? AND food = ?",
                                 session['id'], request.form.get("comida"))
            protein = float(protein[0]['protein'])
            protein = protein*portion
            protein = "{:.2f}".format(protein)

            db.execute("INSERT INTO register (user_id, food, protein, calorie) VALUES (?, ?, ?, ?)",
                       session['id'], request.form.get("comida"), protein, calorie)

            return redirect('/')

        # Si se introdujeron los datos de alguna receta
        if request.form.get("porcion_receta") and request.form.get("receta"):
            portion = float(request.form.get("porcion_receta"))

            # Cantidad de calorias
            calorie = db.execute("SELECT calorie FROM recipes WHERE user_id = ? AND recipe = ?",
                                 session['id'], request.form.get("receta"))
            calorie = float(calorie[0]['calorie'])
            calorie = calorie*portion
            calorie = "{:.2f}".format(calorie)

            # Cantidad de proteinas
            protein = db.execute("SELECT protein FROM recipes WHERE user_id = ? AND recipe = ?",
                                 session['id'], request.form.get("receta"))
            protein = float(protein[0]['protein'])
            protein = protein*portion
            protein = "{:.2f}".format(protein)

            db.execute("INSERT INTO register (user_id, food, protein, calorie) VALUES (?, ?, ?, ?)",
                       session['id'], request.form.get("receta"), protein, calorie)

            return redirect('/')

        else:
            comidas = db.execute("SELECT * FROM foods WHERE user_id = ?", session['id'])
            registros = db.execute("SELECT * FROM register WHERE user_id = ?", session['id'])
            recetas = db.execute("SELECT * FROM recipes WHERE user_id = ?", session['id'])
            aviso = "Favor introducir los datos del alimento"

            total_calorie = 0
            total_protein = 0
            for registro in registros:
                total_calorie = total_calorie + float(registro['calorie'])
                total_protein = total_protein + float(registro['protein'])

            user_nutrition = db.execute("SELECT * FROM users WHERE id = ?", session['id'])
            user_nutrition = user_nutrition[0]
            user_calorie = None
            user_protein = None
            if user_nutrition['calorie'] != None:
                user_calorie = total_calorie - float(user_nutrition['calorie'])
                user_calorie = "{:.2f}".format(user_calorie)
            if user_nutrition['protein'] != None:
                user_protein = total_protein - float(user_nutrition['protein'])
                user_protein = "{:.2f}".format(user_protein)

            total_calorie = "{:.2f}".format(total_calorie)
            total_protein = "{:.2f}".format(total_protein)
            return render_template("index.html", aviso=aviso, total_calorie=total_calorie, total_protein=total_protein, comidas=comidas, registros=registros, recetas=recetas, user_calorie=user_calorie, user_protein=user_protein)

    else:
        # Obtenemos las recetas que hemos agregado
        comidas = db.execute("SELECT * FROM foods WHERE user_id = ?", session['id'])
        # Obtenemos la comida diaria
        registros = db.execute("SELECT * FROM register WHERE user_id = ?", session['id'])
        # Obtenemos las recetas que hemos agregado
        recetas = db.execute("SELECT * FROM recipes WHERE user_id = ?", session['id'])

        total_calorie = 0
        total_protein = 0
        for registro in registros:
            total_calorie = total_calorie + float(registro['calorie'])
            total_protein = total_protein + float(registro['protein'])

        user_nutrition = db.execute("SELECT * FROM users WHERE id = ?", session['id'])
        user_nutrition = user_nutrition[0]
        user_calorie = None
        user_protein = None
        if user_nutrition['calorie'] != None:
            user_calorie = total_calorie - float(user_nutrition['calorie'])
            user_calorie = "{:.2f}".format(user_calorie)
        if user_nutrition['protein'] != None:
            user_protein = total_protein - float(user_nutrition['protein'])
            user_protein = "{:.2f}".format(user_protein)

        total_calorie = "{:.2f}".format(total_calorie)
        total_protein = "{:.2f}".format(total_protein)
        return render_template("index.html", total_calorie=total_calorie, total_protein=total_protein, comidas=comidas, registros=registros, recetas=recetas, user_calorie=user_calorie, user_protein=user_protein)


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Eliminamos lo almacenado en la variable de cookies
    session.clear()

    # Si se accede a la ruta con el metodo POST
    if request.method == 'POST':

        # Verificamos si se introdujo el nombre de usuario
        if not request.form.get("username"):
            aviso = "Favor introducir nombre de usuario"
            return render_template("login.html", aviso=aviso)

        # Verificamos si se introdujo la contraseña
        elif not request.form.get("password"):
            aviso = "Favor introducir la contraseña"
            return render_template("login.html", aviso=aviso)

        else:

            # Verificamos si el nombre de usuario y la contraseña son correctos
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get('username'))
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                aviso = "Nombre de usuario o contraseña invalido"
                return render_template("login.html", aviso=aviso)

            else:
                # Guardamos la id del usuario en la varible cookie
                session['id'] = int(rows[0]['id'])

                # Guardamos los datos del usuario en la variable global
                context_processor()

                return redirect('/')

    # Si se accede a la ruta con el metodo GET
    else:
        return render_template("login.html")


@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        for usernames in db.execute("SELECT username FROM users"):
            if username in usernames['username']:
                aviso = "Favor elegir otro nombre de usuario"
                return render_template("registro.html", aviso=aviso)

        if len(password) < 6:
            aviso = "La contraseña debe contener al menos 6 caracteres"
            return render_template("registro.html", aviso=aviso)

        elif password != request.form.get("confirmation"):
            aviso = "Las contraseñas no coinciden"
            return render_template("registro.html", aviso=aviso)

        else:
            hash_password = generate_password_hash(password)
            db.execute("INSERT INTO users (name, last_name, username, hash) VALUES (?, ?, ?, ?)",
                       name, last_name, username, hash_password)

            aviso_registro = "Registro exitoso, ya puede iniciar sesión"

            return render_template("login.html", aviso_registro=aviso_registro)

    else:
        return render_template("registro.html")


@app.route("/logout")
def logout():

    # Olivdamos id de usuario
    session.clear()

    # Olvidamos los datos del usuario
    context_processor()

    # Redirect user to login form
    return redirect("/")


@app.route("/delete")
def delete():
    db.execute("DELETE FROM register")
    return redirect("/")


@app.route("/alimentos", methods=['POST', 'GET'])
@login_required
def alimentos():
    if request.method == 'POST':
        food = request.form.get("food")
        image_url = request.form.get("image_url")
        protein = float(request.form.get("protein"))
        calorie = float(request.form.get("calorie"))
        gramos = float(request.form.get("gramos"))
        unit = request.form.get("unit")
        protein = protein / gramos
        calorie = calorie / gramos
        db.execute("INSERT INTO foods (user_id, food, image_url, protein, calorie, unit) VALUES (?, ?, ?, ?, ?, ?)",
                   session['id'], food, image_url, protein, calorie, unit)
        alimentos = db.execute("SELECT * FROM foods WHERE user_id = ? ORDER BY food", session['id'])
        return render_template("alimentos.html", alimentos=alimentos)
    if request.method == 'GET':
        alimentos = db.execute("SELECT * FROM foods WHERE user_id = ? ORDER BY food", session['id'])
        return render_template("alimentos.html", alimentos=alimentos)


@app.route("/recetas", methods=["POST", "GET"])
@login_required
def recetas():
    if request.method == "POST":
        i = 0
        # Ingresamos todos los datos del usuario y de la receta
        recipe = request.form.get("recipe")
        description = request.form.get("description")
        image_url = request.form.get("image_url")
        portion = request.form.get("portion")
        db.execute("INSERT INTO recipes (user_id, recipe, description, image_url, portion) VALUES (?, ?, ?, ?, ?)",
                   session['id'], recipe, description, image_url, portion)

        calorie = float(0)
        protein = float(0)
        while True:
            i += 1
            ingrediente = request.form.get("ingrediente_" + str(i))

            # Salimos del bucel si no encontramos otro nuevo ingrediente
            if (ingrediente == None):
                break

            # Guardamos los ingredientes
            else:
                # Guardamos la porcion del ingrediente
                portion_food = request.form.get("portion_" + str(i))
                portion_food = float(portion_food)

                # Verificamos de que exsita la columna y si no existe la creamos
                exist = db.execute("SELECT * FROM recipes WHERE user_id = ?", session['id'])
                if not "ingrediente_" + str(i) in exist[0]:
                    db.execute("ALTER TABLE recipes ADD ? TEXT", "ingrediente_" + str(i))
                    db.execute("ALTER TABLE recipes ADD ? TEXT", "portion_" + str(i))

                # Insertamos los ingredientes
                db.execute("UPDATE recipes SET ? = ? WHERE user_id = ? AND recipe = ?",
                           "ingrediente_" + str(i), ingrediente, session['id'], recipe)
                db.execute("UPDATE recipes SET ? = ? WHERE user_id = ? AND recipe = ?",
                           "portion_" + str(i), portion_food, session['id'], recipe)

                # Calculamos e insertamos las calorias y proteinas de la receta creada
                aux = db.execute("SELECT * FROM foods WHERE user_id = ? AND food = ?", session['id'], ingrediente)
                aux = aux[0]

                calorie = calorie + float(aux['calorie']) * portion_food
                protein = protein + float(aux['protein']) * portion_food
        calorie = calorie / float(portion)
        protein = protein / float(portion)
        db.execute("UPDATE recipes SET calorie = ? WHERE user_id = ? AND recipe = ?", calorie, session['id'], recipe)
        db.execute("UPDATE recipes SET protein = ? WHERE user_id = ? AND recipe = ?", protein, session['id'], recipe)

        ingredientes = db.execute("SELECT * FROM foods WHERE user_id = ? ORDER BY food", session["id"])
        recetas = db.execute("SELECT * FROM recipes WHERE user_id = ? ORDER BY recipe", session["id"])
        return render_template("recetas.html", ingredientes=ingredientes, recetas=recetas)

    else:
        recetas = db.execute("SELECT * FROM recipes WHERE user_id = ? ORDER BY recipe", session["id"])
        ingredientes = db.execute("SELECT * FROM foods WHERE user_id = ? ORDER BY food", session["id"])
        return render_template("recetas.html", ingredientes=ingredientes, recetas=recetas)


@app.route("/calculadora", methods=["POST", "GET"])
@login_required
def calculadora():
    if request.method == "POST":
        pass
    if request.method == "GET":
        return render_template("calculadora.html")


@app.route("/data", methods=["POST"])
def data():
    protein = request.form.get("protein")
    if protein == None or protein == "":
        db.execute("UPDATE users SET protein = NULL WHERE id = ?", session['id'])
    else:
        db.execute("UPDATE users SET protein = ? WHERE id = ?", protein, session['id'])
    calorie = request.form.get("calorie")
    if calorie == None or calorie == "":
        db.execute("UPDATE users SET calorie = NULL WHERE id = ?", session['id'])
    else:
        db.execute("UPDATE users SET calorie = ? WHERE id = ?", calorie, session['id'])
    db.execute("UPDATE users SET username = ? WHERE id = ?", request.form.get("username"), session['id'])
    db.execute("UPDATE users SET name = ? WHERE id = ?", request.form.get("name"), session['id'])
    db.execute("UPDATE users SET last_name = ? WHERE id = ?", request.form.get("last_name"), session['id'])
    return redirect('/')
