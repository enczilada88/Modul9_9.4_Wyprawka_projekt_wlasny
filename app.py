import csv, flask_wtf
from flask import Flask, render_template, request, redirect, jsonify

heading = ["name", "quantity", "dedication", "remarks"]


def save(data):
    with open(r"C:\pythonProjectKodilla\file.csv", "w") as file:
        w = csv.DictWriter(file, fieldnames=heading)
        w.writeheader()
        for i in data:
            w.writerow(i)


def read():
    base_list = []
    try:
        with open(r"C:\pythonProjectKodilla\file.csv", "r") as file:
            base = csv.DictReader(file)
            for row in base:
                base_list.append(row)
    except IOError:
        with open(r"C:\pythonProjectKodilla\file.csv", "w") as file:
            w = csv.DictWriter(file, fieldnames=heading)
            w.writeheader()
    return base_list


app = Flask(__name__)

base = read()


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/add', methods=['GET'])
def add():
    return render_template("add.html")


@app.route('/add', methods=['POST'])
def add_post():
    name = request.form.get("name")
    quantity = request.form.get("quantity")
    dedication = request.form.get("dedication")
    remarks = request.form.get("remarks")
    temp = {
        "name": name,
        "quantity": quantity,
        "dedication": dedication,
        "remarks": remarks
    }
    base.append(temp)
    save(base)
    return redirect("/")


@app.route('/find', methods=['GET'])
def find():
    return render_template("find.html")


@app.route('/find', methods=['POST'])
def find_out():
    new_list = []
    option = request.form.get("option")
    value = request.form.get("value")
    for i in base:
        if i[option] == value:
            new_list.append(i)
    print(new_list)
    return render_template("find.html", result=new_list)


@app.route('/delete', methods=['GET'])
def delete():
    return render_template("delete.html")


@app.route('/delete', methods=['POST'])
def delete_out():
    out = False
    name = request.form.get("name")
    quantity = request.form.get("quantity")
    for i in base:
        if i["name"] == name and i["quantity"] == quantity:
            base.remove(i)
            out = True
    save(base)
    if out:
        message = "Plik usunięto"
    else:
        message = "Nie znalezono pasujących elementów"
    return render_template("delete.html", msg=message)


@app.route('/all', methods=['GET'])
def show_all():
    return render_template("all.html", result=base)


@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(base)