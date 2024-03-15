from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="lavitra",
    password="1234567890",
    database="lost_and_found"
)

# Create cursor
cursor = db.cursor()

# Create a table for lost items if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS lost_items (id INT AUTO_INCREMENT PRIMARY KEY, item_name VARCHAR(255), description TEXT, location VARCHAR(255), date_found DATE)")

# Create a table for found items if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS found_items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), Addmission VARCHAR(255), category VARCHAR(255), colour VARCHAR(255), location VARCHAR(255), description TEXT)")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():

    return render_template('lost_items.html')

@app.route('/submit_lost_item', methods=['POST'])
def submit_lost_item():
    if request.method == 'POST':
        name = request.form['name']
        Addmission = request.form['Addmission']
        category = request.form['category']
        colour = request.form['colour']
        location = request.form['location']
        description = request.form['description']

        # Insert the found item into the database
        cursor.execute("INSERT INTO lost_items (name, Addmission, category, colour, location, description) VALUES (%s, %s, %s, %s, %s, %s)", (name, Addmission, category, colour, location, description))
        db.commit()

        return redirect(url_for('index'))


@app.route('/report_found', methods=['GET', 'POST'])
def report_found():

    return render_template('found_items.html')

@app.route('/submit_found_item', methods=['POST'])
def submit_found_item():
    if request.method == 'POST':
        name = request.form['name']
        Addmission = request.form['Addmission']
        category = request.form['category']
        colour = request.form['colour']
        location = request.form['location']
        description = request.form['description']

        # Insert the found item into the database
        cursor.execute("INSERT INTO found_items (name, Addmission, category, colour, location, description) VALUES (%s, %s, %s, %s, %s, %s)", (name, Addmission, category, colour, location, description))
        db.commit()

        return redirect(url_for('index'))

@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    return render_template('login.html')
    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password exist in the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # If the user exists, redirect to some page (e.g., dashboard)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('/login'))  # Change 'dashboard' to the appropriate route

if __name__ == '__main__':
    app.run(debug=True)
