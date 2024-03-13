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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        location = request.form['location']

        # Insert the lost item into the database
        cursor.execute("INSERT INTO lost_items (item_name, description, location) VALUES (%s, %s, %s)", (item_name, description, location))
        db.commit()

        return redirect(url_for('index'))

    return render_template('report.html')

@app.route('/found_items')
def found_items():
    # Fetch found items from the database
    cursor.execute("SELECT * FROM lost_items")
    found_items = cursor.fetchall()
    return render_template('found_items.html', found_items=found_items)

@app.route('/lost_items')
def lost_items():
    # Fetch lost items from the database
    cursor.execute("SELECT * FROM lost_items")
    lost_items = cursor.fetchall()
    return render_template('lost_items.html', lost_items=lost_items)

@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        location = request.form['location']

        # Insert the found item into the database
        cursor.execute("INSERT INTO lost_items (item_name, description, location) VALUES (%s, %s, %s)", (item_name, description, location))
        db.commit()

        return redirect(url_for('found_items'))

    return render_template('report_found.html')

if __name__ == '__main__':
    app.run(debug=True)
