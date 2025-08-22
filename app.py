from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database
class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

users = {
    1: User(1, 'Faculty Member', 'faculty@school.edu', 'teacher'),
    2: User(2, 'HOD', 'hod@school.edu', 'hod')
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')  # In real app, verify password hash
        role = request.form.get('role')
        
        # Simple authentication (in real app, use proper authentication)
        user = None
        for u in users.values():
            if u.email == email and u.role == role:
                user = u
                break
        
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))
    
    # Handle file upload and analysis
    # files = request.files.getlist('lectureImages')
    # date = request.form.get('lectureDate')
    # Process images and generate results
    
    return render_template('analysis_result.html', result=analysis_result)

if __name__ == '__main__':
    app.run(debug=True)