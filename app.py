from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import re
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simulated user database
users = {}

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(email_regex, email) is not None

def is_strong_password(password):
    return (
        len(password) >= 8 and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        any(char.isdigit() for char in password) and
        any(not char.isalnum() for char in password)
    )

@app.route('/')
def index():
    # Health issues data
    health_issues = [
        {
            'title': 'Nipah virus',
            'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcScJweLpIVOmC7rfr6tOY4SjGyfnsBlQR3icQ&s',
            'description': 'A zoonotic pathogen that can be transmitted from animals to humans. In September 2024, India reported a fatal case of Nipah virus in a 24-year-old student from Bengaluru. The virus is linked to fruit-eating bats and pigs in southern India.',
            'link': 'https://www.cidrap.umn.edu/nipah/india-reports-another-fatal-nipah-virus-case'
        },
        {
            'title': 'Chandipura virus',
            'image': 'https://vajiram-prod.s3.ap-south-1.amazonaws.com/Chandipura_Virus_Infection_32296c62f1.webp',
            'description': 'A member of the Rhabdoviridae family that causes acute encephalitis syndrome (AES). In 2024, India reported a large outbreak of Chandipura virus, with 245 cases of AES and 82 deaths.',
            'link': 'https://www.who.int/emergencies/disease-outbreak-news/item/2024-DON529'
        },
        {
            'title': 'Dengue',
            'image': 'https://i.pinimg.com/736x/54/be/63/54be633a7d4a7d8996f2438e23daa869.jpg',
            'description': 'A flu-like disease transmitted from human to human through mosquitoes. In 2024, Kerala reported more than 2,000 cases of dengue fever.',
            'link': 'https://www.careinsurance.com/blog/health-insurance-articles/viral-threats-in-kerala-one-state-multiple-outbreaks'
        },
        {
            'title': 'Mumps',
            'image': 'https://i.pinimg.com/236x/3d/d6/fd/3dd6fdb3d901dc93cf2f9de578b093a4.jpg',
            'description': 'A viral infection spread through direct contact or air by droplets from an infected persons respiratory tract. In the first half of 2024, Kerala reported more than 11,000 cases of mumps.',
            'link': 'https://www.careinsurance.com/blog/health-insurance-articles/viral-threats-in-kerala-one-state-multiple-outbreaks'
        },
        {
            'title': 'Monkeypox',
            'image': 'https://cdn.apollohospitals.com/health-library-prod/2022/08/Monkeypox-Symptoms.jpg',
            'description': 'A health concern in Kerala, with several cases reported since the beginning of 2024.',
            'link': 'https://www.careinsurance.com/blog/health-insurance-articles/viral-threats-in-kerala-one-state-multiple-outbreaks'
        },
        {
            'title': 'Chikungunya',
            'image': 'https://disease.expert/system/items/images/000/000/096/original/nok_Chikungunya_virus_disease_450eefbb-879f-44f7-b51e-2693273b8f5c.jpg?1677945880',
            'description': 'Chikungunya in the state of Telangana, India. CDC has identified a higher-than-expected number of chikungunya cases among U.S. travelers.',
            'link': 'https://www.thehindu.com/news/national/telangana/telangana-reports-447-chikungunya-cases-till-november-majority-during-monsoon-months/article68894049.ece'
        }
    ]
    
    is_logged_in = 'user_email' in session
    return render_template('index.html', health_issues=health_issues, is_logged_in=is_logged_in)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not is_valid_email(email):
            flash('Please enter a valid Gmail address', 'error')
            return render_template('login.html')

        if email in users and users[email]['password'] == password:
            session['user_email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not is_valid_email(email):
            flash('Please enter a valid Gmail address', 'error')
            return render_template('signup.html')

        if email in users:
            flash('Email already registered', 'error')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')

        if not is_strong_password(password):
            flash('Password must be at least 8 characters long and include uppercase, lowercase, number, and special character', 'error')
            return render_template('signup.html')

        users[email] = {
            'password': password
        }

        session['user_email'] = email
        flash('Signup successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/load_more')
def load_more():
    # Check if user is logged in
    if 'user_email' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    # Pass all health issues to the dashboard
    return render_template('dash.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route("/run_ai_model", methods=["POST"])
def run_ai_model():
    try:
        # Run the Python script and capture its output
        result = subprocess.check_output(["python", "ai_model.py"], universal_newlines=True)
        return jsonify({"status": "success", "output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": str(e)})

@app.route('/help')
def help():
    return "Help Page - Coming Soon!"

if __name__ == '__main__':
    app.run(debug=True)
