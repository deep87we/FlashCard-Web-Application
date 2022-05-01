from flask import Flask,render_template,redirect, url_for,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,UserMixin,logout_user
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SECRET_KEY'] = 'thisissecret'
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password= db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    author = db.Column(db.String(20),nullable=False,default='N/A')
    content = db.Column(db.Text(),nullable=False)
    pub_date = db.Column(db.DateTime(),nullable=False,default=datetime.utcnow)  

    
   


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/main')
def main():
    return render_template('main.html')
@app.route('/')
def index():
    data=Card.query.all()
    return render_template('index.html',data=data)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        username=request.form.get('uname')
        user=User(username=username,email=email,fname=fname,lname=lname,password=password)
        db.session.add(user)
        db.session.commit()
        flash('user has been registered successfully','success')
        return redirect('/login')

    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
       username=request.form.get('username')
       password=request.form.get('password')
       user=User.query.filter_by(username=username).first()
       if user and password==user.password:
           login_user(user)
           return redirect('/')
       else:
            flash('invalid credentials','danger')
            return redirect('/login')
        
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')
@app.route("/card",methods=['GET','POST'])
def card():
    if request.method=='POST':
        title=request.form.get('title')
        author=request.form.get('author')
        content=request.form.get('content')
        card=Card(title=title,author=author,content=content)
        db.session.add(card)
        db.session.commit()
        flash("Your card has been created successfully",'success')
        return redirect('/')
    return render_template('card.html')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form.get('title')
        author=request.form.get('author')
        content=request.form.get('content')
        card=Card.query.filter_by(card_id=sno).first()
        card.title=title
        card.author=author
        card.content=content
        db.session.add(card)
        db.session.commit()
        return redirect('/')
    card=Card.query.filter_by(card_id=sno).first()
    return render_template('edit.html',card=card)



    
@app.route('/delete/<int:sno>')
def delete(sno):
    card=Card.query.filter_by(card_id=sno).first()
    db.session.delete(card)
    db.session.commit()
    flash("Your card has been deleted successfully",'success')
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True) 