from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from algorithm import encrypt_text, decrypt_text
from main import main
import ast
from smtp import send_email
import random
import mysql.connector


# Initialize Flask app with the correct template folder
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

# Route for the login page
@app.route('/')
def index():
    return render_template('login.html')

# Route for the signup page
@app.route('/signup')
def signup_page():
    return render_template('signup.html')

# Route to fetch updated messages
@app.route('/fetch_messages')
def fetch_messages():
    final_messages_list = []
    messages_list = main() 
    for i in messages_list:
        if i['from'] == 'quantaamail@gmail.com':
            i['subject'] = decrypt_text(ast.literal_eval(i['subject']))
            i['snippet'] = decrypt_text(ast.literal_eval(i['snippet']))
            final_messages_list.append(i)
    return jsonify(final_messages_list)

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    final_messages_list = []
    messages_list = main() 
    try:
        for i in messages_list:
            if i['from'] == 'quantaamail@gmail.com':
                decrypt_text_body = ast.literal_eval(i['body'])
                print('Body before:', i['body'])
                i['body'] = decrypt_text(decrypt_text_body)
                print('Body after:', i['body'])
                final_messages_list.append(i)
    except:
        print('no mails found from quantamail')
    print(final_messages_list)

    return render_template('dashboard.html', messages_list=final_messages_list)

@app.route('/dashboard.html')
def dashboard_template():
    return render_template('dashboard.html')


# Route to handle signup form submission
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



@app.route('/login', methods=['POST'])
def login():
    gmail_id = request.form.get('userName')
    password = request.form.get('password')
    
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # SQL query to check if the user exists
    cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (gmail_id, password))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if user:
        
        session['user_id'] = user['id']
        session['fname'] = user['first_name']
        session['lname'] = user['last_name']
        return redirect(url_for('dashboard'))
    else:
        
        return render_template('login.html', error='Invalid email or password.')

@app.route('/send_mail', methods=['POST'])
def send_mail():
    to = request.form.get('to')
    subject = request.form.get('subject')
    body = request.form.get('body')
    global body_encrypt
    body_encrypt = encrypt_text(body)
    print("body encrypt: ", str(body_encrypt))
    
    #SMTP sending mail
    send_email(to,subject,str(body_encrypt))
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
    
    

