from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import random
import re

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.secret_key = 'your_secret_key'  # Required to use sessions

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Default XAMPP MySQL user
    'password': '',  # Default XAMPP MySQL password (usually empty)
    'database': 'user_db'  # Ensure this matches your MySQL database name
}

# Create a connection to the database
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Route for the signup page (GET request to render the form)
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

# Route to handle signup form submission and insert data into the database (POST request)
@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Extract form data
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        gmail_id = request.form.get('gmail_id')
        password = request.form.get('pwd')
        
        # Generate a random ID
        ID = random.randint(0, 99999999999)
        
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # SQL query to insert data into the user table
        insert_query = '''
        INSERT INTO user (id, first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s, %s)
        '''
        
        # Execute the query and commit changes
        cursor.execute(insert_query, (ID, fname, lname, gmail_id, password))
        connection.commit()
        
        print("Data inserted successfully")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('index'))

# Route for the home page (login page in this context)
@app.route('/')
def index():
    return render_template('login.html')



# Route to handle login form submission and verify user credentials
@app.route('/login', methods=['POST'])
def login():
    gmail_id = request.form.get('userName')
    password = request.form.get('password')
    
    # Establish database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # SQL query to check if the user exists
    cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (gmail_id, password))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if user:
        # Store user info in session
        session['user_id'] = user['id']
        session['fname'] = user['first_name']
        session['lname'] = user['last_name']
        return redirect(url_for('dashboard'))
    else:
        # Invalid credentials, redirect to login with error
        return render_template('login.html', error='Invalid email or password.')

# Route for the dashboard page (only accessible after login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        fname = session['fname']
        lname = session['lname']
        return f'Welcome to your dashboard, {fname} {lname}!'
    else:
        return redirect(url_for('index'))

# Route to handle user logout
@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return redirect(url_for('index'))




# Run the app
if __name__ == '__main__':
    app.run(debug=True)
