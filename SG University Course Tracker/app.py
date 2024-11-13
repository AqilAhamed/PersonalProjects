from flask import Flask, render_template, request
import sqlite3
import base64

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def home():
    return render_template("index.html")

@app.route('/instructions', methods = ["POST", "GET"])
def instructions():
    return render_template("instructions.html")


@app.route('/NUS', methods = ["POST"])
def NUS():

    # To find Rank Points of the user
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

    ##Ineracting with Database

    #Finding eligible courses from Database

    courses = []
    con = sqlite3.connect("./database/sqldb.db")
    for row in con.execute(f'SELECT * FROM NUS WHERE RankPoint <= {RP}'):
        courses.append([row[0], row[1]])

    con.close()

    #Picture from Database

    con = sqlite3.connect("./database/sqldb.db")
    cursor = con.cursor()

    m = cursor.execute("""
    SELECT * FROM Logo
    """)

    for row in m:
        x = row[0]
        
    con.close()

    data = base64.b64encode(x)
    data = data.decode('UTF-8')

    return render_template("NUS.html", RP = RP, courses = courses, data = data)


@app.route('/NTU', methods = ["POST"])
def NTU():

    # To find Rank Points of the user
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

    ##Ineracting with Database

    #Finding eligible courses from Database

    courses = []
    con = sqlite3.connect("./database/sqldb.db")
    for row in con.execute(f'SELECT * FROM NTU WHERE RankPoint <= {RP}'):
        courses.append([row[0], row[1]])

    con.close()

    #Picture from Database

    con = sqlite3.connect("./database/sqldb.db")
    cursor = con.cursor()

    m = cursor.execute("""
    SELECT * FROM Logo
    """)

    for row in m:
        x = row[1]
        
    con.close()

    data = base64.b64encode(x)
    data = data.decode('UTF-8')

    return render_template("NTU.html", RP = RP, courses = courses, data = data)


@app.route('/SMU', methods = ["POST"])
def SMU():

    # To find Rank Points of the user
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

    ##Ineracting with Database

    #Finding eligible courses from Database

    courses = []
    con = sqlite3.connect("./database/sqldb.db")
    for row in con.execute(f'SELECT * FROM SMU WHERE RankPoint <= {RP}'):
        courses.append([row[0], row[1]])

    con.close()

    #Picture from Database

    con = sqlite3.connect("./database/sqldb.db")
    cursor = con.cursor()

    m = cursor.execute("""
    SELECT * FROM Logo
    """)

    for row in m:
        x = row[2]
        
    con.close()

    data = base64.b64encode(x)
    data = data.decode('UTF-8')

    return render_template("SMU.html", RP = RP, courses = courses, data = data)


## Web Admin

@app.route('/admin', methods = ["POST", "GET"])
def admin():
    return render_template("admin.html")


###### NUS #######

@app.route('/admin/nus_retrieve', methods=["POST", "GET"])
def nus_retrieve():
    courses_and_rp = []
    con = sqlite3.connect("./database/sqldb.db")
    for row in con.execute('SELECT * FROM NUS'):
        courses_and_rp.append([row[2], row[0], row[1]])

    con.close()

    return render_template("nus_retrieve.html", courses_and_rp = courses_and_rp)

@app.route('/admin/nus_insert', methods=["POST", "GET"])
def nus_insert():
    try:
        inserted_course = request.form["course"]
        inserted_rp = float(request.form["rp"])
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = f"""INSERT INTO NUS
                                (Course, RankPoint) 
                                VALUES 
                                ("{inserted_course}", {inserted_rp})"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        cursor.close()

        return render_template("nus_insert.html")

    except:
        return render_template("nus_insert.html")

@app.route('/admin/nus_update', methods=["POST", "GET"])
def nus_update():
    try:
        #Update Course
        try:
            updated_course = request.form["course"]
            update_id = request.form["id-update"]

            sqliteConnection = sqlite3.connect('./database/sqldb.db')
            cursor = sqliteConnection.cursor()

            sql_update_query = f"""Update NUS set Course = '{updated_course}' where id = {update_id}"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()

            return render_template("nus_update.html")

        #Update RP
        except:
            updated_rp = float(request.form["rp"])
            update_id = request.form["id-update"]

            sqliteConnection = sqlite3.connect('./database/sqldb.db')
            cursor = sqliteConnection.cursor()

            sql_update_query = f"""Update NUS set RankPoint = '{updated_rp}' where id = {update_id}"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()

            return render_template("nus_update.html")

            
    except:
        return render_template("nus_update.html")


@app.route('/admin/nus_delete', methods=["POST", "GET"])
def nus_delete():
    try:
        update_id = request.form["id-update"]

        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        # Deleting single record now
        sql_delete_query = f"""DELETE from NUS where id = {update_id}"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        
        cursor.close()

        #Getting right IDs
        count = 0
        count_lst = []
        courses = []
        con = sqlite3.connect("./database/sqldb.db")
        for row in con.execute(f'SELECT * FROM NUS'):
            count += 1
            count_lst.append(count)
            courses.append(row[0])
        con.close()

        #Update seq
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        sql_update_query = f"""Update sqlite_sequence set seq = {count} where name = 'NUS'"""
        cursor.execute(sql_update_query)
        sqliteConnection.commit()
        cursor.close()

        #Updating IDs
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        for i in range(len(courses)):
            sql_update_query = f"""Update NUS set id = {count_lst[i]} where Course = '{courses[i]}'"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
        
        cursor.close()


        return render_template("nus_delete.html")

    except:
        return render_template("nus_delete.html")


###### END OF NUS #######


###### NTU #######

@app.route('/admin/ntu_retrieve', methods=["POST", "GET"])
def ntu_retrieve():
    courses_and_rp = []
    con = sqlite3.connect("./database/sqldb.db")
    for row in con.execute('SELECT * FROM NTU'):
        courses_and_rp.append([row[2], row[0], row[1]])

    con.close()

    return render_template("ntu_retrieve.html", courses_and_rp = courses_and_rp)

@app.route('/admin/ntu_insert', methods=["POST", "GET"])
def ntu_insert():
    try:
        inserted_course = request.form["course"]
        inserted_rp = float(request.form["rp"])
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = f"""INSERT INTO NTU
                                (Course, RankPoint) 
                                VALUES 
                                ("{inserted_course}", {inserted_rp})"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        cursor.close()

        return render_template("ntu_insert.html")

    except:
        return render_template("ntu_insert.html")

@app.route('/admin/ntu_update', methods=["POST", "GET"])
def ntu_update():
    try:
        #Update Course
        try:
            updated_course = request.form["course"]
            update_id = request.form["id-update"]

            sqliteConnection = sqlite3.connect('./database/sqldb.db')
            cursor = sqliteConnection.cursor()

            sql_update_query = f"""Update NTU set Course = '{updated_course}' where id = {update_id}"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()

            return render_template("ntu_update.html")

        #Update RP
        except:
            updated_rp = float(request.form["rp"])
            update_id = request.form["id-update"]

            sqliteConnection = sqlite3.connect('./database/sqldb.db')
            cursor = sqliteConnection.cursor()

            sql_update_query = f"""Update NTU set RankPoint = '{updated_rp}' where id = {update_id}"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()

            return render_template("ntu_update.html")

            
    except:
        return render_template("ntu_update.html")


@app.route('/admin/ntu_delete', methods=["POST", "GET"])
def ntu_delete():
    try:
        update_id = request.form["id-update"]

        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        # Deleting single record now
        sql_delete_query = f"""DELETE from NTU where id = {update_id}"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        
        cursor.close()

        #Getting right IDs
        count = 0
        count_lst = []
        courses = []
        con = sqlite3.connect("./database/sqldb.db")
        for row in con.execute(f'SELECT * FROM NTU'):
            count += 1
            count_lst.append(count)
            courses.append(row[0])
        con.close()

        #Update seq
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        sql_update_query = f"""Update sqlite_sequence set seq = {count} where name = 'NTU'"""
        cursor.execute(sql_update_query)
        sqliteConnection.commit()
        cursor.close()

        #Updating IDs
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        for i in range(len(courses)):
            sql_update_query = f"""Update NTU set id = {count_lst[i]} where Course = '{courses[i]}'"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
        
        cursor.close()


        return render_template("ntu_delete.html")

    except:
        return render_template("ntu_delete.html")


###### END OF NTU #######


##### SMU ######

@app.route('/admin/smu_retrieve', methods=["POST", "GET"])
def smu_retrieve():
    courses_and_rp = []
    con = sqlite3.connect("./database/sqldb.db")
    for row in con.execute('SELECT * FROM SMU'):
        courses_and_rp.append([row[2], row[0], row[1]])

    con.close()

    return render_template("smu_retrieve.html", courses_and_rp = courses_and_rp)

@app.route('/admin/smu_insert', methods=["POST", "GET"])
def smu_insert():
    try:
        inserted_course = request.form["course"]
        inserted_rp = float(request.form["rp"])
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = f"""INSERT INTO SMU
                                (Course, RankPoint) 
                                VALUES 
                                ("{inserted_course}", {inserted_rp})"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        cursor.close()

        return render_template("smu_insert.html")

    except:
        return render_template("smu_insert.html")

@app.route('/admin/smu_update', methods=["POST", "GET"])
def smu_update():
    try:
        #Update Course
        try:
            updated_course = request.form["course"]
            update_id = request.form["id-update"]

            sqliteConnection = sqlite3.connect('./database/sqldb.db')
            cursor = sqliteConnection.cursor()

            sql_update_query = f"""Update SMU set Course = '{updated_course}' where id = {update_id}"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()

            return render_template("smu_update.html")

        #Update RP
        except:
            updated_rp = float(request.form["rp"])
            update_id = request.form["id-update"]

            sqliteConnection = sqlite3.connect('./database/sqldb.db')
            cursor = sqliteConnection.cursor()

            sql_update_query = f"""Update SMU set RankPoint = '{updated_rp}' where id = {update_id}"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()

            return render_template("smu_update.html")

            
    except:
        return render_template("smu_update.html")


@app.route('/admin/smu_delete', methods=["POST", "GET"])
def smu_delete():
    try:
        update_id = request.form["id-update"]

        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        # Deleting single record now
        sql_delete_query = f"""DELETE from SMU where id = {update_id}"""
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()
        
        cursor.close()

        #Getting right IDs
        count = 0
        count_lst = []
        courses = []
        con = sqlite3.connect("./database/sqldb.db")
        for row in con.execute(f'SELECT * FROM SMU'):
            count += 1
            count_lst.append(count)
            courses.append(row[0])
        con.close()

        #Update seq
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        sql_update_query = f"""Update sqlite_sequence set seq = {count} where name = 'SMU'"""
        cursor.execute(sql_update_query)
        sqliteConnection.commit()
        cursor.close()

        #Updating IDs
        sqliteConnection = sqlite3.connect('./database/sqldb.db')
        cursor = sqliteConnection.cursor()

        for i in range(len(courses)):
            sql_update_query = f"""Update SMU set id = {count_lst[i]} where Course = '{courses[i]}'"""
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
        
        cursor.close()


        return render_template("smu_delete.html")

    except:
        return render_template("smu_delete.html")


##### END OF SMU ######

if __name__ == "__main__":
    app.run(debug=True)