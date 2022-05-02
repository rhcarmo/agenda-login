from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
app.config['SECRET_KEY'] = 'qEChL7R3SpF72cEA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    created_at = db.Column(db.String())
    update_at = db.Column(db.String())

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    image = db.Column(db.String())
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.String())
    update_at = db.Column(db.String())

@app.route('/')
def index():
    return render_template('login.html', Users=Users)

# depois do login
@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    new_contacts = Contacts(
        name = name,
        email = email,
        phone = phone
    )
    db.session.add(new_contacts)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    delete = Contacts.query.filter_by(id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    update = Contacts.query.filter_by(id=id).first()
    update.name = name
    update.email = email
    update.phone = phone
    db.session.commit()
    return redirect('/')

# Antes do Login
@app.route('/signin', methods=['POST'])
def signup():
  email_input = request.form.get('email')
  password_input = request.form.get('password')

  # Verificar se já existe o email no bd
  user = Users.query.filter_by(email=email_input).first()
  if not user:
    return redirect('/login')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register')
def register():
  return render_template('register.html')
  
@app.route('/signup', methods=['POST'])
def signup():
  name_input = request.form.get('name')
  email_input = request.form.get('email')
  password_input = request.form.get('password')

  # Verificar se já existe o email no bd
  user = Users.query.filter_by(email=email_input).first()
  if user:
    return redirect('/register')

  new_user = Users(
    name=name_input,
    email=email_input,
    password=generate_password_hash(password_input)
  )
  db.session.add(new_user)
  db.session.commit()
  return redirect('/login')

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)