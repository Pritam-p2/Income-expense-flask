from datetime import datetime
from flask_login import UserMixin 
from app import db,bcrypt,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model,UserMixin):
    id=db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True) 
    email_address = db.Column(db.String(length=50), nullable=False, unique=True) 
    password_hash = db.Column(db.String(length=60), nullable=False)
    income = db.relationship('IncomeExpenses',lazy=True)

    # creating new property 
    @property 
    def password(self): 
        return self.password 
    @password.setter 
    def password(self,plain_text_password): 
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') 
    def check_password_correction(self,attempted_password): 
        return bcrypt.check_password_hash(self.password_hash,attempted_password)   

class IncomeExpenses(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), default = 'income', nullable=False)
    category = db.Column(db.String(30), nullable=False, default='rent')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    userId= db.Column(db.Integer(),db.ForeignKey('user.id')) 
    
    def __str__(self):
        return str(self.id)+self.type+self.category
    
   


  