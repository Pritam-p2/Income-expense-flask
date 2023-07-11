from app import app,db 
from flask import render_template,flash,redirect,url_for,get_flashed_messages
from app.forms import UserDataForm,RegisterForm,LoginForm
from app.models import IncomeExpenses,User
import json
from flask_login import login_user,logout_user,login_required,current_user 

@app.route('/') 
def home():
    return render_template('home.html')
@app.route('/index') 
@login_required
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html',title = "index",entries=entries)
    

 
@app.route('/register',methods=['GET','POST']) 
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,email_address=form.email_address.data, password=form.passw.data) 
        db.session.add(user_to_create) 
        db.session.commit() 
        login_user(user_to_create) 
        flash(f'Account Created Successfully! You are now logged in as {user_to_create.username}', category="success")
        return render_template('index.html',form=form,title='register')
    if form.errors != {}: #if no errors from the validators 
        for err_msg in form.errors.values(): 
            flash(f'{err_msg}',category='danger') 
    return render_template('register.html',form=form) 


@app.route('/login', methods=['GET', 'POST']) 
def login(): 
    form = LoginForm() 
    if form.validate_on_submit(): 
        attempted_user = User.query.filter_by(username=form.username.data).first() 
        if attempted_user and attempted_user.check_password_correction( 
            attempted_password=form.password.data): 
            login_user(attempted_user) 
            flash(f'Success! You are logged in as: {attempted_user.username}', category="success") 
            return redirect(url_for('index')) 
        else: 
            flash('Username and password are not match! Please try again', category='danger')    
    return render_template('login.html', form=form)         

@app.route('/logout')
@login_required
def logout():
    IncomeExpenses.query.delete()
    db.session.commit()
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home")) 

    




@app.route('/add',methods=['GET','POST'])
@login_required
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data,amount=form.amount.data,category=form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash("Successful entry",'success')
        return redirect(url_for('index'))
    return render_template ("add.html",title='add data',form=form)
    
       
@app.route('/Income')
@login_required
def filterIncome():
    entries = IncomeExpenses.query.filter_by(type='income').order_by(IncomeExpenses.date.desc()).all()
    return render_template("index.html",entries=entries)

   

@app.route('/Expense')
@login_required
def filterExpense():
    entries = IncomeExpenses.query.filter_by(type='expense').order_by(IncomeExpenses.date.desc()).all()
    return render_template("index.html",entries=entries)


@app.route('/delete/<int:entry_id>')
@login_required
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was successful",'success')
    return redirect(url_for("index"))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
       
        income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()
    #category_comparison=db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).filter(db.and_(IncomeExpenses.category == 'salary', IncomeExpenses.category == 'side_hustle')).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()
        category_income = db.session.query(IncomeExpenses.category,IncomeExpenses.id).filter(IncomeExpenses.type=='income').all()
        category_comparison = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()

        dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).filter(IncomeExpenses.type=='expense').group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

        
        taka = []
        category1=[]
        for amounts,category in category_comparison:
            taka.append(int(amounts))
            category1.append(category)
        
        category_income_a=[]
        for c,d in category_income:
            category_income_a.append(c)

        color=[]
        for category in category1:
            if category in category_income_a:
                color.append('#FAA43A')
            else:
                color.append('#5DA5DA')    
                 

        income_expense = []
        for total_amount,_ in income_vs_expense:
            income_expense.append(total_amount)

        over_time_expenditure = []
        dates_label = []
        for amount, date in dates:
            dates_label.append(date.strftime("%m-%d-%y"))
            over_time_expenditure.append(amount)

        return render_template('dashboard.html',
                            income_vs_expense=json.dumps(income_expense),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label =json.dumps(dates_label),
                            taka =json.dumps(taka),
                            category =json.dumps(category1),
                            color=json.dumps(color)
                        )
    else:
        return redirect("register.html")