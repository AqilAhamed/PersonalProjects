from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/result', methods = ["POST"])
def result():
    oldEmail = request.form["oldEmail"]
    oldPassword = request.form["oldPassword"]

    with open("./Login System/database.csv", "r") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if oldEmail in row and oldPassword in row:
                  return render_template("granted.html", name=row[0])
                else:
                    pass
            return render_template("denied.html")

        except:
            return render_template("denied.html")

@app.route('/details', methods = ["POST"])
def details():
    name = request.form["name"]
    newEmail = request.form["newEmail"]
    newPassword = request.form["newPassword"]
    with open("./Login System/database.csv", "a") as f:
        info = [name, newEmail, newPassword]
        writer = csv.writer(f)
        writer.writerow(info)
        return render_template("created.html", name=name)
if __name__ == "__main__":
    app.run(debug=True)