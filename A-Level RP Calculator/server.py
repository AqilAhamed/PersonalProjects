from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods = ["POST"])
def results():

    h2Grade1 = float(request.form["h2-grade-1"])
    h2Grade2 = float(request.form["h2-grade-2"])
    h2Grade3 = float(request.form["h2-grade-3"])
    h1Grade = float(request.form["h1-grade-1"])
    pwGrade = float(request.form["pw-grade"])
    gpGrade = float(request.form["gp-grade"])
    mtlGrade = request.form["mtl-grade"]

    if mtlGrade == "NIL":
        RP = h2Grade1 + h2Grade2 + h2Grade3 + h1Grade + pwGrade + gpGrade

    elif mtlGrade != "NIL":
        rp_without_mtl = h2Grade1 + h2Grade2 + h2Grade3 + h1Grade + pwGrade + gpGrade
        rp_with_mtl = (h2Grade1 + h2Grade2 + h2Grade3 + h1Grade + pwGrade + gpGrade + float(mtlGrade)) * 0.9

        if rp_without_mtl <= rp_with_mtl:
            RP = rp_with_mtl

        elif rp_without_mtl >= rp_with_mtl:
            RP = rp_without_mtl

    return render_template("index.html", RP = RP)

if __name__ == "__main__":
    app.run(debug=True)