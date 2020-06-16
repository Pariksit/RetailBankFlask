from flask import render_template, url_for, flash, redirect,request
from RetailBank.models import userstore,Customer,Account
from RetailBank import app,db,bcrypt
from RetailBank.forms import Loginform,NewCustomerForm,DeleteCustomerForm,UpdateCustomerForm,SearchCustomerForm,NewAccountForm,DeleteAccountForm
from datetime import datetime
from flask_login import login_user,current_user,logout_user,login_required


@app.route('/home',methods=['GET', 'POST'])
def home():
	return render_template('home.html',title='Home')

@app.route('/index',methods=['GET','POST'])
@login_required
def index():
	return render_template('home.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=Loginform()
	if form.validate_on_submit():
		user=userstore.query.filter_by(login=form.login.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash('Login Successful', 'success')
			return redirect(next_page) if next_page else redirect(url_for('login'))
            #return"<h1>Login Successful</h1>"
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
			#flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html',title='Login',form=form)

@app.route('/create_customer',methods=['GET','POST'])
@login_required
def create_customer():
	form = NewCustomerForm()
	if form.validate_on_submit():
		print(form.ssd_id.data,form.customer_name.data,form.customer_age.data,form.customer_address.data,form.customer_state.data,form.customer_city.data)
		cust = Customer(ssd_id=form.ssd_id.data,customer_name=form.customer_name.data,customer_age=form.customer_age.data,
			customer_address=form.customer_address.data,
			customer_state=form.customer_state.data,customer_city=form.customer_city.data)
		db.session.add(cust)
		db.session.commit()
		flash(f'Account created for {form.customer_name.data}!', 'success')
		return redirect(url_for('index'))
	return render_template('create_customer.html',title='New Customer',form=form)

@app.route('/delete',methods=['GET','POST'])
@login_required
def delete():
	form = DeleteCustomerForm()
	if form.validate_on_submit():
		ssd_id_1 = form.cus_id.data
		cust = Customer.query.filter_by(ssd_id=ssd_id_1).first()
		if not cust:
			flash(f'{ssd_id_1} not present in the database!', 'danger')
			return redirect(url_for('delete'))
		cust_name=cust.customer_name
		db.session.delete(cust)
		db.session.commit()
		flash(f'Account delete for {cust_name}!', 'success')

	return render_template('delete_customers.html',title='Delete',form=form)

@app.route('/customer_info',methods=['GET','POST'])
@login_required
def customer_info():
	info = Customer.query.all()
	return render_template('customers.html',info=info)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/search',methods=['GET','POST'])
@login_required
def search():
	cust=""
	if request.method == "POST":
		ssd_id_1=request.form["id"]
		cust=Customer.query.filter_by(ssd_id=ssd_id_1).first()
		if not cust:
			flash(f'{ssd_id_1} not present in the database.','danger')
			return redirect(url_for('search'))
		else:
			return redirect(url_for("update",cust_id=ssd_id_1))
	return render_template("search_customer.html",cust=cust)

@app.route('/<cust_id>',methods=['GET','POST'])
@login_required
def update(cust_id):
	cust_info = Customer.query.filter_by(ssd_id=cust_id).first()
	u_form=UpdateCustomerForm()
	if u_form.validate_on_submit():
		cust_info.customer_name=u_form.customer_name.data
		cust_info.customer_age=u_form.customer_age.data
		cust_info.customer_address=u_form.customer_address.data
		cust_info.customer_state=u_form.customer_state.data
		cust_info.customer_city=u_form.customer_city.data
		db.session.commit()
		flash(f'{cust_info.customer_name} s Account Information has been updated!','success')
		return redirect(url_for('search'))
	elif request.method== 'GET':
		u_form.customer_name.data=cust_info.customer_name
		u_form.customer_age.data=cust_info.customer_age
		u_form.customer_address.data=cust_info.customer_address
		u_form.customer_state.data=cust_info.customer_state
		u_form.customer_city.data=cust_info.customer_city

	return render_template("update_customer.html",u_form=u_form)

@app.route('/deposit',methods=['GET','POST'])
@login_required
def deposit():
	d_form=NewAccountForm()
	if d_form.validate_on_submit():
		cust_id=d_form.customer_id.data
		cust_info=Customer.query.filter_by(ssd_id=cust_id).first()
		if not cust_info:
			flash(f'{cust_id} does not exist.Please create a customer first.','danger')
			return redirect(url_for('create_customer'))

		elif Account.query.filter_by(customer_id=cust_id).first():
			if Account.query.filter_by(customer_id=cust_id).first().status==False:
				flash(f'{cust_id} does exist already.','danger')
				return redirect(url_for('deposit'))
			else:
				db.session.delete(Account.query.filter_by(customer_id=cust_id).first())
				db.session.commit()

		if d_form.deposit_amount.data<1000:
			flash('Deposit Amount is less . Should be greater than 1000 ','danger')
			return redirect(url_for('deposit'))
		else:
			if d_form.account_type.data.lower()=='savings':
				d_form.account_type.data='Savings'
			elif d_form.account_type.data.lower()=='current':
				d_form.account_type.data='Current'
			else:
				flash('Enter Account Type correctly')
				return redirect(url_for('deposit'))

		acc = Account(account_type=d_form.account_type.data,balance=d_form.deposit_amount.data,customer_id=d_form.customer_id.data)
		db.session.add(acc)
		db.session.commit()
		flash(f'{cust_info.customer_name} account has been created . ','success')


	return render_template('create_account.html',d_form=d_form)

@app.route('/account',methods=['GET','POST'])
@login_required
def account_info():
	acc=Account.query.all()
	return render_template('accounts.html',acc=acc)

@app.route('/delete_account',methods=['GET','POST'])
@login_required
def delete_account():
	form = DeleteAccountForm()
	account_type=''
	if form.validate_on_submit():
		ssd_id_1 = form.customer_id.data
		acc = Account.query.filter_by(customer_id=ssd_id_1).first()
		if acc.status=='True' or not acc:
			flash(f'{ssd_id_1} not present in the database!', 'danger')
			return redirect(url_for('delete_account'))
		account_type=acc.account_type
		acc.status=True
		db.session.commit()
		flash(f'Account delete for {ssd_id_1}!', 'success')

	return render_template('delete_account.html',title='Delete',form=form,account_type=account_type)