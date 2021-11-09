from flask import Flask, request, url_for, redirect, render_template
import sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/apply', methods=['GET','POST'])
def apply():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        fname = request.form['fusername']
        lname = request.form['lusername']
        pos = request.form['jobPosition']
        phone = request.form['phoneNumber']
        email = request.form['emailAddress']
        ssn = request.form['socialSecurityNumber']
        connection  = sqlite3.connect("data.db")
        cursor = connection.cursor()
        stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='applicant';"
        cursor.execute(stmt)
        result = cursor.fetchone()
        if (result):
            query1 = "INSERT INTO applicant VALUES('{f}', '{l}', '{p}', '{ph}', '{e}', '{s}')".format(f = fname, l = lname, p = pos, ph = phone, e = email, s = ssn)
            cursor.execute(query1)
        else:
            stmt = "CREATE TABLE applicant (fname VARCHAR(20), lname VARCHAR(20), pos VARCHAR(20), phone VARCHAR(15), email VARCHAR(20), ssn VARCHAR(15))"
            cursor.execute(stmt)
            query1 = "INSERT INTO applicant VALUES('{f}', '{l}', '{p}', '{ph}', '{e}', '{s}')".format(f = fname, l = lname, p = pos, ph = phone, e = email, s = ssn)
            cursor.execute(query1)
        
        connection.commit()
        connection.close()
        return render_template("index.html")


@app.route('/resultdata')
def resultdata():
    try:
        if request.method == 'GET':
            email = request.args.get("emailAddress")
            connection  = sqlite3.connect("data.db")            
            cursor = connection.cursor()
            query1 = "SELECT ssn from applicant WHERE email = {e}".format (e = email)
            result = cursor.execute(query1)
            result = result.fetchall()[0][0]
    except:
        return render_template("resultData.html", ssn = "")

if __name__ == '__main__':
    app.run(debug=True)