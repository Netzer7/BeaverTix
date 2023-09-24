from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users,(int(user_id)))

@app.route("/")
def homepage():
    return render_template("test.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email has already been used for an account
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already taken. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
       
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = Users(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.j2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You are now logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
                    
                    
# # Protected route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')                    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

with app.app_context():
    db.create_all()
     