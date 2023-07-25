import flask
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'L0K1X1DK5R6EYT74Y'
bootstrap = Bootstrap(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

pharmacyId = 123456
adminId = 123


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        password = sha256_crypt.hash(request.form.get('password'))
        passwordConfirm = request.form.get('passwordConfirm')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        active = 0
        if sha256_crypt.verify(passwordConfirm, password):
            if (cur.execute("SELECT * FROM Costumer WHERE username=%s", [username]) == 0) and len(username) >= 5:
                if cur.execute("SELECT * FROM Costumer WHERE email=%s", [email]) == 0:
                    cur.execute("INSERT INTO Costumer(username,email,name,lastname,password,phoneNumber,address,active)"
                                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                [username, email, name, lastname, password, phoneNumber, address, active])
                    mysql.connection.commit()
                    cur.close()
                    flask.flash('Registration successful! Please login.', 'success')
                    return redirect(url_for('login'))
                else:
                    flask.flash('Email exists!', 'danger')
                    return render_template("registration.html")
            else:
                flask.flash('Username exists!', 'danger')
                return render_template("registration.html")
        else:
            flask.flash('Password error!')
            return render_template("registration.html")
    return render_template("registration.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if session.get('username') is None:
            cur = mysql.connection.cursor()
            username = request.form.get('username')
            password = request.form.get('password')
            if cur.execute("SELECT * FROM Costumer WHERE username=%s", [username]) > 0:
                costumer = cur.fetchone()
                if sha256_crypt.verify(password, costumer[4]):
                    session['login'] = True
                    session['username'] = costumer[0]
                    session['name'] = costumer[2]
                    session['lastname'] = costumer[3]
                    mysql.connection.commit()
                    cur.execute("UPDATE Costumer SET active=1 WHERE username=%s ", [username])
                    mysql.connection.commit()
                    flask.flash('Login as costumer successful!', 'success')
                    result_value = cur.execute("SELECT * FROM Medicament")
                    if result_value > 0:
                        medicaments = cur.fetchall()
                        return render_template("medicaments.html", medicaments=medicaments)
                    return render_template("medicaments.html")
                else:
                    flask.flash('Passwords do not match, try again.', 'success')
                    render_template('login.html')
            else:
                if cur.execute("SELECT * FROM Admin WHERE username=%s and password=%s",
                               [username, password]) > 0:
                    admin = cur.fetchone()
                    session['login'] = True
                    session['username'] = admin[1]
                    session['email'] = admin[2]
                    mysql.connection.commit()
                    cur.execute("UPDATE Admin SET active = 1 WHERE username = %s ", [username])
                    mysql.connection.commit()
                    cur1 = mysql.connection.cursor()
                    cur2 = mysql.connection.cursor()
                    cur3 = mysql.connection.cursor()
                    result1 = cur1.execute("SELECT * FROM Medicament")
                    result2 = cur2.execute("SELECT * FROM Pharmacy")
                    result3 = cur3.execute("SELECT * FROM Costumer")
                    med = cur1.fetchall()
                    pharms = cur2.fetchall()
                    costumers = cur3.fetchall()
                    if (result1 or result2 or result3) > 0:
                        flask.flash('Administrator is active.', 'success')
                        return render_template('dashboard.html', medicaments=med, pharms=pharms, costumers=costumers)
                    return render_template('dashboard.html')
                else:
                    flask.flash('Invalid username and password!', 'danger')
                    return render_template('login.html')
        else:
            cur = mysql.connection.cursor()
            result_value = cur.execute("SELECT * from Medicament")
            if result_value > 0:
                medicaments = cur.fetchall()
                return render_template("medicaments.html", medicaments=medicaments)
            return render_template("medicaments.html")
    else:
        if session.get('username') is not None:
            cur = mysql.connection.cursor()
            result_value = cur.execute("SELECT * from Medicament")
            if result_value > 0:
                medicaments = cur.fetchall()
                return render_template("medicaments.html", medicaments=medicaments)
        else:
            return render_template("login.html")
    return render_template("login.html")


@app.route('/medicaments/', methods=['GET', 'POST'])
def medicaments():
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM Medicament")
        med = cur.fetchall()
        if result > 0:
            return render_template('medicaments.html', medicaments=med)
        flask.flash('No Medicaments Found', 'danger')
        return render_template('index.html')


@app.route('/addmedicaments/', methods=['GET', 'POST'])
def add_medicaments():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        idMedicament = request.form.get('idMedicament')
        medicamentName = request.form.get('medicamentName')
        manufacturer = request.form.get('manufacturer')
        stockQuantity = request.form.get('stockQuantity')
        expiryDate = request.form.get('expiryDate')
        price = request.form.get('price')
        descripiton = request.form.get('description')
        cur.execute("INSERT INTO Medicament(idMedicament,medicamentName,manufacturer,stockQuantity,expiryDate,price,"
                    "description,Pharmacy_idPharmacy,Pharmacy_Admin_idAdmin) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [idMedicament, medicamentName, manufacturer, stockQuantity, expiryDate, price, descripiton,
                     pharmacyId, adminId])
        mysql.connection.commit()
        cur.close()
        flask.flash('Medicament added successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        return render_template('addmedicaments.html')


@app.route('/deletemedicament/<int:id>', methods=['POST'])
def delete_medicament(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM Medicament WHERE idMedicament=%s', [id])
        mysql.connection.commit()
        cur.close()
    flask.flash('Medicament deleted.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur1 = mysql.connection.cursor()
        cur2 = mysql.connection.cursor()
        cur3 = mysql.connection.cursor()
        result1 = cur1.execute("SELECT * FROM Medicament")
        result2 = cur2.execute("SELECT * FROM Pharmacy")
        result3 = cur3.execute("SELECT * FROM Costumer")
        med = cur1.fetchall()
        pharms = cur2.fetchall()
        costumers = cur3.fetchall()
        if (result1 or result2 or result3) > 0:
            return render_template('dashboard.html', medicaments=med, pharms=pharms, costumers=costumers)
        cur1.close()
        cur2.close()
        cur3.close()
        flask.flash('No Data Found', 'danger')
    return render_template('index.html')


@app.route('/pharmacy/', methods=['GET', 'POST'])
def pharmacy():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM Pharmacy")
    pharm = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', pharmas=pharm)
    flask.flash('No Pharmacy Found', 'danger')
    return render_template('dashboard.html')


@app.route('/logout/')
def logout():
    if session.get('username') is not None:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Admin SET active = 0 WHERE username = %s ", [session['username']])
        mysql.connection.commit()
        session.pop('username')
        return render_template('index.html')
    else:
        return render_template('index.html')
