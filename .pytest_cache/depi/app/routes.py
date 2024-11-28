from app import db
from app.forms import SalesStaffForm
from app.models import Customer

main = Blueprint('main', __name__)  # Create a blueprint for the main routes

# Route: Home with SalesStaff Form
@main.route('/', methods=['GET', 'POST'])
def home():
    form = SalesStaffForm()  # Create an instance of the SalesStaffForm

    if form.validate_on_submit():  # Check if form submission is valid
        # Create a new Customer instance using form data
        new_customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            active=form.active.data,
            store_id=form.store_id.data,
            manager_id=form.manager_id.data
        )

        # Add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()
        flash('New customer added successfully!', 'success')

        return redirect(url_for('main.home'))  # Redirect to the home page

    # Render the home template with the form
    return render_template('home.html', form=form)


# Route: Display DataFrames
@main.route('/dataframes')
def display_dataframes():
    # Load dataframes using the custom load_data function
    products_df = load_data('products')        # Load products data
    customers_df = load_data('customers')      # Load customers data
    orders_df = load_data('customer_orders')   # Load customer orders
    order_items_df = load_data('order_items_revenue')  # Load order items data

    # Convert DataFrames to HTML tables with 'data' CSS class
    products_html = products_df.to_html(classes='data', header=True, index=False)
    customers_html = customers_df.to_html(classes='data', header=True, index=False)
    orders_html = orders_df.to_html(classes='data', header=True, index=False)
    order_items_html = order_items_df.to_html(classes='data', header=True, index=False)

    # Render the dataframes.html template with HTML tables
    return render_template(
        'dataframes.html',
        products=products_html,
        customers=customers_html,
        orders=orders_html,
        order_items=order_items_html
    )


# Route: View and Search Customers
@main.route('/customers')
def customers():
    search = request.args.get('search', '')  # Get the search query from request
    if search:
        # Filter customers based on name or email matching the search query
        customer_list = Customer.query.filter(
            (Customer.first_name.like(f"%{search}%")) | (Customer.email.like(f"%{search}%"))
        ).all()
    else:
        customer_list = Customer.query.all()  # Get all customers if no search query

    # Render the customers template with the customer list
    return render_template('customers.html', customers=customer_list)
