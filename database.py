import psycopg2

# NOTE: change the password below to YOUR OWN local postgres password.
# This is the only place the password lives in the whole project.
def get_connection():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='19477',
        dbname='resto_reserve_db'
    )
    return conn


# ---------------- USERS ----------------

def check_user_exists(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def insert_user(full_name, email, phone_number, password, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO users (full_name, email, phone_number, password, role)
           VALUES (%s, %s, %s, %s, %s)""",
        (full_name, email, phone_number, password, role)
    )
    conn.commit()
    cur.close()
    conn.close()


# ---------------- TABLES ----------------

def get_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tables ORDER BY table_number")
    tables = cur.fetchall()
    cur.close()
    conn.close()
    return tables


def insert_table(table_number, capacity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tables (table_number, capacity, status) VALUES (%s, %s, 'available')",
        (table_number, capacity)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_available_tables(party_size):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM tables WHERE status = 'available' AND capacity >= %s ORDER BY capacity ASC",
        (party_size,)
    )
    tables = cur.fetchall()
    cur.close()
    conn.close()
    return tables


def update_table_status(table_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tables SET status = %s WHERE id = %s", (status, table_id))
    conn.commit()
    cur.close()
    conn.close()


# ---------------- RESERVATIONS ----------------

def get_reservations():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT reservations.id, reservations.customer_name, reservations.phone_number,
               reservations.party_size, reservations.reservation_time, reservations.status,
               tables.id, tables.table_number
        FROM reservations
        JOIN tables ON reservations.table_id = tables.id
        ORDER BY reservations.reservation_time
    """)
    reservations = cur.fetchall()
    cur.close()
    conn.close()
    return reservations


def insert_reservation(customer_name, phone_number, party_size, table_id, reservation_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO reservations (customer_name, phone_number, party_size, table_id, reservation_time, status)
           VALUES (%s, %s, %s, %s, %s, 'confirmed')""",
        (customer_name, phone_number, party_size, table_id, reservation_time)
    )
    cur.execute("UPDATE tables SET status = 'reserved' WHERE id = %s", (table_id,))
    conn.commit()
    cur.close()
    conn.close()


def cancel_reservation(reservation_id, table_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE reservations SET status = 'cancelled' WHERE id = %s", (reservation_id,))
    cur.execute("UPDATE tables SET status = 'available' WHERE id = %s", (table_id,))
    conn.commit()
    cur.close()
    conn.close()
