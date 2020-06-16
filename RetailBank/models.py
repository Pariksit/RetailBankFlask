from datetime import datetime
from RetailBank import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return userstore.query.get(int(user_id))

class userstore(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	login=db.Column(db.String(20),unique=True,nullable=False)
	password=db.Column(db.String(60),nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"userstore('{self.login}','{self.password}','{self.date_posted}')"

class Customer(db.Model):
	ssd_id=db.Column(db.Integer,primary_key=True)
	customer_name=db.Column(db.String(60),nullable=False)
	customer_age=db.Column(db.String(3),nullable=False)
	customer_address=db.Column(db.String(100),nullable=False)
	customer_state=db.Column(db.String(20),nullable=False)
	customer_city=db.Column(db.String(20),nullable=False)
	accounts = db.relationship('Account',backref='customers',lazy=True)

	def __repr__(self):
		return f"Customer('{self.ssd_id}','{self.customer_name}','{self.customer_age}','{self.customer_address}','{self.customer_state}','{self.customer_city}')"

class Account(db.Model):
	account_id=db.Column(db.Integer,primary_key=True)
	account_type=db.Column(db.String(10),nullable=False)
	balance=db.Column(db.Integer,nullable=False)
	status = db.Column(db.Boolean(), default=False)
	transaction_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	customer_id=db.Column(db.Integer, db.ForeignKey('customer.ssd_id'), nullable=False)

	def __repr__(self):
		return f"Account('{self.account_id}','{self.account_type}','{self.balance}','{self.status}','{self.transaction_timestamp},'{self.customer_id}')"

