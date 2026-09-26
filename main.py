from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from database import (
    check_user_exists, insert_user,
    get_tables, insert_table, get_available_tables,
    get_reservations, insert_reservation, cancel_reservation
)

app = Flask(__name__)
app.secret_key = 'change-this-secret-key'
bcrypt = Bcrypt(app)


# ---------------- AUTH HELPERS ----------------

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admins only', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return wrapper


# ---------------- AUTH ROUTES ----------------

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        role = request.form['role']

        if check_user_exists(email):
            flash('User already exists, please login instead', 'warning')
            return redirect(url_for('login'))

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        insert_user(full_name, email, phone_number, hashed_pw, role)
        flash('Registered successfully, please login', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = check_user_exists(email)
        if not user:
            flash('No account with that email, please register', 'warning')
            return redirect(url_for('register'))

        stored_hash = user[4]
        if not bcrypt.check_password_hash(stored_hash, password):
            flash('Incorrect password', 'danger')
            return redirect(url_for('login'))

        session['email'] = user[2]
        session['full_name'] = user[1]
        session['role'] = user[5]
        flash('Logged in successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('login'))


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
@login_required
def dashboard():
    reservations = get_reservations()
    tables = get_tables()
    return render_template('dashboard.html', reservations=reservations, tables=tables)


# ---------------- RESERVATIONS ----------------

@app.route('/reservations/add', methods=['GET', 'POST'])
@login_required
def add_reservation():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        phone_number = request.form['phone_number']
        party_size = int(request.form['party_size'])
        table_id = int(request.form['table_id'])
        reservation_time = request.form['reservation_time']

        insert_reservation(customer_name, phone_number, party_size, table_id, reservation_time)
        flash('Reservation created successfully', 'success')
        return redirect(url_for('dashboard'))

    party_size = request.args.get('party_size', 1)
    available_tables = get_available_tables(party_size)
    return render_template('add_reservation.html', tables=available_tables)


@app.route('/reservations/cancel/<int:reservation_id>/<int:table_id>')
@login_required
def cancel(reservation_id, table_id):
    cancel_reservation(reservation_id, table_id)
    flash('Reservation cancelled', 'info')
    return redirect(url_for('dashboard'))


# ---------------- TABLES (admin only) ----------------

@app.route('/tables')
@login_required
@admin_required
def tables():
    all_tables = get_tables()
    return render_template('tables.html', tables=all_tables)


@app.route('/tables/add', methods=['POST'])
@login_required
@admin_required
def add_table():
    table_number = request.form['table_number']
    capacity = int(request.form['capacity'])
    insert_table(table_number, capacity)
    flash('Table added', 'success')
    return redirect(url_for('tables'))


if __name__ == '__main__':
    app.run(debug=True)
