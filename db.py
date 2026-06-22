import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import streamlit as st
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import pandas as pd

# =====================================================
# DATABASE CONFIGURATION
# =====================================================

DB_URL = os.getenv("DATABASE_URL") or os.getenv("DB_URL")


def normalize_db_url(url):

    if not url:
        return url

    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query))

    if "sslmode" not in query:
        query["sslmode"] = "require"

    return urlunparse(
        parsed._replace(
            query=urlencode(query)
        )
    )

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
    "sslmode": os.getenv("DB_SSLMODE", "require")
}

# =====================================================
# CONNECTION POOL
# =====================================================

db_pool = None


def get_db_pool():
    global db_pool

    if db_pool is None:
        if DB_URL:
            db_pool = pool.SimpleConnectionPool(
                1,
                10,
                dsn=normalize_db_url(DB_URL)
            )
        else:
            db_pool = pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

    return db_pool

# =====================================================
# CONNECTION
# =====================================================

def get_connection():
    return get_db_pool().getconn()

# =====================================================
# GENERIC DATABASE FUNCTIONS
# =====================================================

def execute_query(query, params=None):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params or ())
        conn.commit()
        return True

    except Exception as e:
        st.error(f"Database Error: {e}")
        print("DB ERROR:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        get_db_pool().putconn(conn)


def fetch_one(query, params=None):

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()

    except Exception as e:
        print("DB ERROR:", e)
        return None

    finally:
        cursor.close()
        get_db_pool().putconn(conn)


def fetch_all(query, params=None):

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()

    except Exception as e:
        print("DB ERROR:", e)
        return []

    finally:
        cursor.close()
        get_db_pool().putconn(conn)


def fetch_dataframe(query, params=None):

    conn = get_connection()

    try:
        return pd.read_sql(query, conn, params=params)

    except Exception as e:
        print("DB ERROR:", e)
        return pd.DataFrame()

    finally:
        get_db_pool().putconn(conn)

# =====================================================
# DASHBOARD KPI FUNCTIONS
# =====================================================

def get_total_customers():

    row = fetch_one("""
        SELECT COUNT(*) AS total
        FROM customers
    """)

    return row["total"] if row else 0


def get_total_staff():

    row = fetch_one("""
        SELECT COUNT(*) AS total
        FROM staff
    """)

    return row["total"] if row else 0


def get_total_products():

    row = fetch_one("""
        SELECT COUNT(*) AS total
        FROM products
    """)

    return row["total"] if row else 0


def get_total_services():

    row = fetch_one("""
        SELECT COUNT(*) AS total
        FROM services
    """)

    return row["total"] if row else 0


def get_today_sales():

    row = fetch_one("""
        SELECT
            COALESCE(SUM(grand_total), 0) AS total
        FROM bills
        WHERE bill_date::date = CURRENT_DATE
    """)

    return row["total"] if row else 0


def get_today_appointments():

    row = fetch_one("""
        SELECT COUNT(*) AS total
        FROM appointments
        WHERE appointment_date = CURRENT_DATE
    """)

    return row["total"] if row else 0


def monthly_sales_chart():

    query = """
    SELECT
        EXTRACT(MONTH FROM bill_date) AS month_no,
        TO_CHAR(bill_date, 'Month') AS month_name,
        SUM(grand_total) sales
    FROM bills
    GROUP BY
        EXTRACT(MONTH FROM bill_date),
        TO_CHAR(bill_date, 'Month')
    ORDER BY month_no
    """

    return fetch_dataframe(query)

# =====================================================
# CUSTOMER CRUD
# =====================================================

def get_all_customers():

    return fetch_dataframe("""
        SELECT *
        FROM customers
        ORDER BY customer_id DESC
    """)


def get_customer(customer_id):

    return fetch_one("""
        SELECT *
        FROM customers
        WHERE customer_id=%s
    """, (customer_id,))


def insert_customer(
        customer_code,
        customer_name,
        phone,
        email,
        gender,
        dob,
        address,
        referred_by):

    return execute_query("""
        INSERT INTO customers
        (
            customer_code,
            customer_name,
            phone,
            email,
            gender,
            dob,
            address,
            referred_by
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s
        )
    """,
    (
        customer_code,
        customer_name,
        phone,
        email,
        gender,
        dob,
        address,
        referred_by
    ))


def update_customer(
        customer_id,
        customer_name,
        phone,
        email,
        gender,
        dob,
        address):

    return execute_query("""
        UPDATE customers
        SET
            customer_name=%s,
            phone=%s,
            email=%s,
            gender=%s,
            dob=%s,
            address=%s
        WHERE customer_id=%s
    """,
    (
        customer_name,
        phone,
        email,
        gender,
        dob,
        address,
        customer_id
    ))


def delete_customer(customer_id):

    return execute_query("""
        DELETE FROM customers
        WHERE customer_id=%s
    """, (customer_id,))

# =====================================================
# SERVICES CRUD
# =====================================================

def get_services():

    return fetch_dataframe("""
        SELECT s.*,
               c.category_name
        FROM services s
        LEFT JOIN service_categories c
            ON s.category_id = c.category_id
        ORDER BY s.service_id DESC
    """)


def get_service(service_id):

    return fetch_one("""
        SELECT *
        FROM services
        WHERE service_id=%s
    """, (service_id,))


def insert_service(
        category_id,
        service_name,
        sale_price,
        duration_minutes):

    return execute_query("""
        INSERT INTO services
        (
            category_id,
            service_name,
            sale_price,
            duration_minutes
        )
        VALUES
        (
            %s,%s,%s,%s
        )
    """,
    (
        category_id,
        service_name,
        sale_price,
        duration_minutes
    ))


def update_service(
        service_id,
        category_id,
        service_name,
        sale_price,
        duration_minutes):

    return execute_query("""
        UPDATE services
        SET
            category_id=%s,
            service_name=%s,
            sale_price=%s,
            duration_minutes=%s
        WHERE service_id=%s
    """,
    (
        category_id,
        service_name,
        sale_price,
        duration_minutes,
        service_id
    ))


def delete_service(service_id):

    return execute_query("""
        DELETE FROM services
        WHERE service_id=%s
    """, (service_id,))

# =====================================================
# APPOINTMENTS CRUD
# =====================================================

def get_appointments():

    query = """
    SELECT
        a.appointment_id,
        c.customer_name,
        s.staff_name,
        a.appointment_date,
        a.appointment_time,
        a.status
    FROM appointments a

    LEFT JOIN customers c
        ON a.customer_id=c.customer_id

    LEFT JOIN staff s
        ON a.staff_id=s.staff_id

    ORDER BY a.appointment_id DESC
    """

    return fetch_dataframe(query)


def get_appointment(appointment_id):

    return fetch_one("""
        SELECT *
        FROM appointments
        WHERE appointment_id=%s
    """, (appointment_id,))


def insert_appointment(
        customer_id,
        staff_id,
        appointment_date,
        appointment_time,
        status):

    return execute_query("""
        INSERT INTO appointments
        (
            customer_id,
            staff_id,
            appointment_date,
            appointment_time,
            status
        )
        VALUES
        (
            %s,%s,%s,%s,%s
        )
    """,
    (
        customer_id,
        staff_id,
        appointment_date,
        appointment_time,
        status
    ))


def update_appointment(
        appointment_id,
        customer_id,
        staff_id,
        appointment_date,
        appointment_time,
        status):

    return execute_query("""
        UPDATE appointments
        SET
            customer_id=%s,
            staff_id=%s,
            appointment_date=%s,
            appointment_time=%s,
            status=%s
        WHERE appointment_id=%s
    """,
    (
        customer_id,
        staff_id,
        appointment_date,
        appointment_time,
        status,
        appointment_id
    ))


def delete_appointment(appointment_id):

    return execute_query("""
        DELETE FROM appointments
        WHERE appointment_id=%s
    """, (appointment_id,))

# =====================================================
# INVENTORY CRUD
# =====================================================

def get_inventory():

    query = """
    SELECT
        p.product_id,
        p.product_name,
        p.stock_qty,
        p.cost_price,
        p.sale_price,
        b.brand_name,
        c.category_name
    FROM products p

    LEFT JOIN brands b
        ON p.brand_id=b.brand_id

    LEFT JOIN inventory_categories c
        ON p.category_id=c.category_id

    ORDER BY p.product_id DESC
    """

    return fetch_dataframe(query)


def get_product(product_id):

    return fetch_one("""
        SELECT *
        FROM products
        WHERE product_id=%s
    """, (product_id,))


def insert_product(
        category_id,
        brand_id,
        product_name,
        cost_price,
        sale_price,
        stock_qty,
        minimum_stock):

    return execute_query("""
        INSERT INTO products
        (
            category_id,
            brand_id,
            product_name,
            cost_price,
            sale_price,
            stock_qty,
            minimum_stock
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
    """,
    (
        category_id,
        brand_id,
        product_name,
        cost_price,
        sale_price,
        stock_qty,
        minimum_stock
    ))


def update_product(
        product_id,
        category_id,
        brand_id,
        product_name,
        cost_price,
        sale_price,
        stock_qty,
        minimum_stock):

    return execute_query("""
        UPDATE products
        SET
            category_id=%s,
            brand_id=%s,
            product_name=%s,
            cost_price=%s,
            sale_price=%s,
            stock_qty=%s,
            minimum_stock=%s
        WHERE product_id=%s
    """,
    (
        category_id,
        brand_id,
        product_name,
        cost_price,
        sale_price,
        stock_qty,
        minimum_stock,
        product_id
    ))


def delete_product(product_id):

    return execute_query("""
        DELETE FROM products
        WHERE product_id=%s
    """, (product_id,))

# =====================================================
# CATEGORY HELPERS
# =====================================================

def get_service_categories():

    return fetch_all("""
        SELECT *
        FROM service_categories
        ORDER BY category_name
    """)


def get_inventory_categories():

    return fetch_all("""
        SELECT *
        FROM inventory_categories
        ORDER BY category_name
    """)

# =====================================================
# BRAND HELPERS
# =====================================================

def get_brands():

    return fetch_all("""
        SELECT *
        FROM brands
        ORDER BY brand_name
    """)

# =====================================================
# STAFF HELPERS
# =====================================================

def get_staff():

    return fetch_all("""
        SELECT *
        FROM staff
        ORDER BY staff_name
    """)

# =====================================================
# USERS CRUD
# =====================================================

def get_users():

    query = """
    SELECT
        u.user_id,
        u.username,
        u.email,
        u.status,
        r.role_name,
        b.branch_name
    FROM users u

    LEFT JOIN roles r
        ON u.role_id=r.role_id

    LEFT JOIN branches b
        ON u.branch_id=b.branch_id

    ORDER BY u.user_id DESC
    """

    return fetch_dataframe(query)


def get_user(user_id):

    return fetch_one("""
        SELECT *
        FROM users
        WHERE user_id=%s
    """, (user_id,))


def insert_user(
        branch_id,
        role_id,
        username,
        email,
        password_hash,
        status):

    return execute_query("""
        INSERT INTO users
        (
            branch_id,
            role_id,
            username,
            email,
            password_hash,
            status
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s
        )
    """,
    (
        branch_id,
        role_id,
        username,
        email,
        password_hash,
        status
    ))


def update_user(
        user_id,
        branch_id,
        role_id,
        username,
        email,
        status):

    return execute_query("""
        UPDATE users
        SET
            branch_id=%s,
            role_id=%s,
            username=%s,
            email=%s,
            status=%s
        WHERE user_id=%s
    """,
    (
        branch_id,
        role_id,
        username,
        email,
        status,
        user_id
    ))


def delete_user(user_id):

    return execute_query("""
        DELETE FROM users
        WHERE user_id=%s
    """, (user_id,))

# =====================================================
# DROPDOWN HELPERS
# =====================================================

def get_customers_dropdown():

    return fetch_all("""
        SELECT
            customer_id,
            customer_name
        FROM customers
        ORDER BY customer_name
    """)


def get_services_dropdown():

    return fetch_all("""
        SELECT
            service_id,
            service_name,
            sale_price
        FROM services
        ORDER BY service_name
    """)


def get_staff_dropdown():

    return fetch_all("""
        SELECT
            staff_id,
            staff_name
        FROM staff
        ORDER BY staff_name
    """)


def get_roles_dropdown():

    return fetch_all("""
        SELECT
            role_id,
            role_name
        FROM roles
        ORDER BY role_name
    """)


def get_branches_dropdown():

    return fetch_all("""
        SELECT
            branch_id,
            branch_name
        FROM branches
        ORDER BY branch_name
    """)

# =====================================================
# BILLING
# =====================================================

def get_bills():

    query = """
    SELECT
        bill_id,
        bill_no,
        bill_date,
        subtotal,
        discount,
        tax,
        grand_total,
        payment_method
    FROM bills
    ORDER BY bill_id DESC
    """

    return fetch_dataframe(query)


def delete_bill(bill_id):

    execute_query("""
        DELETE FROM bill_details
        WHERE bill_id=%s
    """, (bill_id,))

    return execute_query("""
        DELETE FROM bills
        WHERE bill_id=%s
    """, (bill_id,))


def get_bill_details(bill_id):

    query = """
    SELECT
        bd.detail_id,
        s.service_name,
        st.staff_name,
        bd.quantity,
        bd.price,
        bd.line_total
    FROM bill_details bd

    LEFT JOIN services s
        ON bd.service_id=s.service_id

    LEFT JOIN staff st
        ON bd.staff_id=st.staff_id

    WHERE bd.bill_id=%s
    """

    return fetch_dataframe(
        query,
        (bill_id,)
    )

# =====================================================
# REPORTS
# =====================================================

def sales_report(
        start_date,
        end_date):

    query = """
    SELECT *
    FROM bills
    WHERE bill_date::date
    BETWEEN %s AND %s
    ORDER BY bill_date DESC
    """

    return fetch_dataframe(
        query,
        (
            start_date,
            end_date
        )
    )


def inventory_report():

    query = """
    SELECT
        product_name,
        stock_qty,
        minimum_stock,
        cost_price,
        sale_price
    FROM products
    ORDER BY product_name
    """

    return fetch_dataframe(query)


def appointment_report():

    query = """
    SELECT
        a.appointment_id,
        c.customer_name,
        s.staff_name,
        a.appointment_date,
        a.status
    FROM appointments a

    LEFT JOIN customers c
        ON a.customer_id=c.customer_id

    LEFT JOIN staff s
        ON a.staff_id=s.staff_id

    ORDER BY a.appointment_date DESC
    """

    return fetch_dataframe(query)

# =====================================================
# DASHBOARD CHARTS
# =====================================================

def top_services_chart():

    query = """
    SELECT
        s.service_name,
        COUNT(*) total
    FROM bill_details bd

    JOIN services s
        ON bd.service_id=s.service_id

    GROUP BY s.service_name
    ORDER BY total DESC
    LIMIT 10
    """

    return fetch_dataframe(query)


def low_stock_products():

    query = """
    SELECT
        product_name,
        stock_qty,
        minimum_stock
    FROM products
    WHERE stock_qty <= minimum_stock
    ORDER BY stock_qty
    """

    return fetch_dataframe(query)
