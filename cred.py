from flask import Flask, request, render_template, send_from_directory, render_template_string
import os

app = Flask(__name__)

@app.route('/intrestedstyle.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'intrestedstyle.css')

@app.route('/')
def index():
    with open('intrested.html', 'r') as f:
        html_content = f.read()
    return render_template_string(html_content)  

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email_bar']
    
    print(f"Registered email: {email}")
    
    return "Registration successful! You will be notified when updates are made."

if __name__ == '__main__':
    app.run(debug=True)
