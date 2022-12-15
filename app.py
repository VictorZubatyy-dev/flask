from flask import Flask, render_template, redirect
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json

mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'victor'
app.config['MYSQL_PASSWORD'] = 'HelloWorld$'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = 'lab5mysql.mysql.database.azure.com'
mysql.init_app(app)


@app.route("/add")  # Add Student
def add():
    # parameters submitted in the URL (key=value)
    name = request.args.get('name')
    email = request.args.get('email')

    if name and email:
        cur = mysql.connection.cursor()  # create a connection to the SQL instance
        s = '''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,                                                                  email)  # kludge - use stored proc or params
        cur.execute(s)
        mysql.connection.commit()
        return '{"Result":"Success"}'

    return '{"You forgot to add name or email"}'


@app.route("/update", methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        user_email = request.form['email']
        name = request.form['new_name']
        email = request.form['new_email']

        try:
            if user_email:
                if name:
                    cur = mysql.connection.cursor()  # create a connection to the SQL instance
                    s = '''UPDATE students SET studentName = '{}' WHERE email = '{}';'''.format(name, user_email)  # kludge - use stored proc or params
                    try:
                        cur.execute(s)
                        mysql.connection.commit()
                    except:
                        print("Incorrect user email")
                    else:
                        return '{"Result":"Success"}'

                if email:
                    cur = mysql.connection.cursor()  # create a connection to the SQL instance
                    s = '''UPDATE students SET email = '{}' WHERE email = '{}';'''.format(email, user_email)  # kludge - use stored proc or params
                    try:
                        cur.execute(s)
                        mysql.connection.commit()
                    except:
                        print("Incorrect user email")
                    else:
                        return '{"Result":"Success"}'
        except:
            print("Incorrect user email")


@app.route("/dashboard")
def home():
    return render_template('update.html')

# delete user
@app.route("/delete")
def delete():
    # dont delete by name as multiple names can be the same
    email = request.args.get('email')
    cur = mysql.connection.cursor()  # create a connection to the SQL instance

    if email:
        s = '''DELETE FROM students WHERE email='{}';'''.format(email)
        cur.execute(s)
        mysql.connection.commit()
        return '{Deleted user}'

    return {'Enter the correct email or ID of user you wan to delete.'}

@app.route("/read")  # Default - Show Data
def read():  # Name of the method
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''')  # execute an SQL statment
    rv = cur.fetchall()  # Retreive all rows returend by the SQL statment
    Results = []
    for row in rv:  # Format the Output Results and add to return string
        Result = {}
        Result['Name'] = row[0].replace('\n', ' ')
        Result['Email'] = row[1]
        Result['ID'] = row[2]
        Results.append(Result)
    response = {'Results': Results, 'count': len(Results)}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return ret  # Return the data in a string format


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)  # Run the flask app at port 8080
