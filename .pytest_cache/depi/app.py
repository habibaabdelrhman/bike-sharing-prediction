import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bike_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

# Home Route
@app.route('/')
def home():
    return render_template('home.html')

# Add Customer Route
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Validate form input
        if not name or not email or not phone:
            flash('All fields are required!', 'danger')
            return redirect(url_for('add_customer'))

        # Add new customer
        new_customer = Customer(name=name, email=email, phone=phone)
        try:
            db.session.add(new_customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            db.session.rollback()
            flash('Error: Email might already exist.', 'danger')

    return render_template('add_customer.html')

# View Customers Route
@app.route('/customers', methods=['GET'])
def customers():
    search = request.args.get('search', '')
    if search:
        customer_list = Customer.query.filter(
            (Customer.name.like(f"%{search}%")) | (Customer.email.like(f"%{search}%"))
        ).all()
    else:
        customer_list = Customer.query.all()
    return render_template('customers.html', customers=customer_list)

# Edit Customer Route
@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        try:
            db.session.commit()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating customer.', 'danger')
    return render_template('edit_customer.html', customer=customer)

# Delete Customer Route
@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting customer.', 'danger')
    return redirect(url_for('customers'))

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
