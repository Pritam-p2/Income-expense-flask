from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField,StringField,PasswordField
from wtforms.validators import DataRequired,ValidationError,Length,EqualTo,Email 
from app.models import User

class UserDataForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()],
                                choices=[('income', 'income'),
                                        ('expense', 'expense')])
    category = StringField(label='Category', validators=[DataRequired()]) 
    amount = IntegerField('Amount', validators = [DataRequired()])                                   
    submit = SubmitField('Generate Report')                            


class RegisterForm(FlaskForm): 
    def validate_username(self,username_to_check): 
        user = User.query.filter_by(username=username_to_check.data).first() 
        if user: 
            raise ValidationError('Username already exists! Please try a different username') 
    def validate_email_address(self, email_address_to_check): 
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first() 
        if email_address: 
            raise ValidationError('Email Address already exists! Please try a different email address')
    username = StringField(label='User Name:',validators= [Length(min=2,max=30),DataRequired()]) 
    email_address = StringField(label='Email Address:',validators=[Email(),DataRequired()]) 
    passw = PasswordField(label='Password:',validators=[Length(min=6),DataRequired()]) 
    password2 = PasswordField(label='Confirm Password:',validators= [EqualTo( 'passw'),DataRequired()]) 
    submit = SubmitField(label='Create Account"')      

class LoginForm(FlaskForm): 
    username = StringField(label='User Name:', validators=[DataRequired()]) 
    password = PasswordField(label='Password:', validators=[DataRequired()]) 
    submit = SubmitField(label="Login")      