from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Default password for XAMPP's MySQL is empty
app.config['MYSQL_DB'] = 'billing_system'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    try:
        customer_id = request.form['customer_id']
        units_consumed = request.form['units_consumed']

        # Calculate the bill amount
        rate_per_unit = 5.0  # Example rate
        amount = int(units_consumed) * rate_per_unit

        # Insert into bills table
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO bills (customer_id, units_consumed, amount)
            VALUES (%s, %s, %s)
        ''', (customer_id, units_consumed, amount))
        mysql.connection.commit()

        # Fetch the bill details along with the customer name
        cur.execute('''
            SELECT b.id AS bill_id, b.customer_id, c.name AS customer_name, b.units_consumed, b.amount
            FROM bills b
            JOIN customers c ON b.customer_id = c.id
            WHERE b.id = LAST_INSERT_ID()
        ''')
        bill = cur.fetchone()
        cur.close()

        return render_template('index.html', bill=bill)

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while generating the bill."


if __name__ == '__main__':
    app.run(debug=True)
