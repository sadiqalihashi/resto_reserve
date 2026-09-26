# Resto Reserve

A simple restaurant table reservation system built with Flask and PostgreSQL, with staff login (admin / waiter roles).

## Setup

Open up a new terminal and run the following commands:

```
pip install flask
pip install psycopg2-binary
pip install flask-bcrypt
```

## Database setup

Open your Postgres SQL shell (psql). Once connected to postgres:

1. Create a new database called resto_reserve_db:
```
CREATE DATABASE resto_reserve_db;
```

2. Connect to that database:
```
\c resto_reserve_db
```

3. Create the tables using schema.sql (run each statement, or run the whole file with `\i schema.sql` if you're inside the project folder in psql).

## Set your password

Open `database.py` and change this line to your own local postgres password:

```python
password='CHANGE_ME',
```

## Run the app

```
python main.py
```

Then open the address it prints (usually http://127.0.0.1:5000) in your browser.

## How it works

- **Register** creates a staff account as either `admin` or `waiter`.
- **Login** authenticates against the hashed password stored in `users`.
- **Dashboard** shows all tables (color-coded by status) and all reservations.
- **New Reservation** lets any logged-in staff member book a table for a customer at a given time. Only `available` tables that fit the party size show up.
- **Manage Tables** (admin only) lets an admin add new tables to the restaurant.
- Cancelling a reservation frees the table back up (`status` returns to `available`).

## Project structure

```
resto_reserve/
├── main.py          -> Flask app & routes
├── database.py      -> All database queries (psycopg2)
├── schema.sql        -> Table definitions
├── templates/        -> HTML pages (Jinja2 + Bootstrap)
└── static/
    └── style.css
```
