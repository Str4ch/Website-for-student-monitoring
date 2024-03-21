from flask import Flask, render_template, request, redirect
import src.dbreq

app = Flask(__name__, template_folder="site/pages", static_folder="site/static")

username = ""
password = ""
@app.route("/")
def index():
    global username
    global password
    if username == "":
        return redirect('/login')
    else:
        if password is None:
            password = ""
        data = src.dbreq.execute_req_for_pages(username, password, 1)
    table1 = data[0]
    table2 = data[1]
    return render_template("index.html", un=username, arr=data[0], arr2=data[1], time=data[2])


@app.route('/login', methods=['post', 'get'])
def login():
    global username
    global password
    if request.method == 'POST':
        username = request.form.get('Uinput')
        password = request.form.get('Pinput')
        return redirect("/")
    return render_template('login.html')


@app.route('/populations/<course>/<year>/<period>', methods=['post','get'])
def populations(course, year, period):
    data = src.dbreq.execute_req_for_pages(username, password, 2, course, year, period)
    return render_template("populations.html", arr1=data[0], arr2=data[1], course=course, year=year, period=period)


@app.route('/student/<email>')
def student(email):
    data = src.dbreq.execute_req_for_pages(username, password, 3, email)
    return render_template("student.html", arr1=data)


@app.route('/students/<course>/<year>/<period>')
def students(course, year, period):
    data = src.dbreq.execute_req_for_pages(username, password, 4, course, year, period)
    return render_template("student.html", arr1=data)


if __name__ == "__main__":
    app.run(debug=True)
