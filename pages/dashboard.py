import streamlit as st
from db import *

def show_dashboard():

    st.title("The Beauty Hub Dashboard")

    customers = get_total_customers()
    staff = get_total_staff()
    products = get_total_products()
    sales = get_today_sales()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Customers",
            customers
        )

    with c2:
        st.metric(
            "Staff",
            staff
        )

    with c3:
        st.metric(
            "Products",
            products
        )

    with c4:
        st.metric(
            "Today's Sales",
            f"Rs {sales:,.0f}"
        )

    st.divider()

    # ===============================
    # Monthly Sales
    # ===============================

    st.subheader("Monthly Sales")

    sales_df = monthly_sales_chart()

    if not sales_df.empty:

        st.line_chart(
            sales_df.set_index("month_name")["sales"]
        )

    else:

        st.info("No Sales Data Available")

    # ===============================
    # Customers
    # ===============================

    st.subheader("Recent Customers")

    customers_df = get_all_customers()

    if not customers_df.empty:

        st.dataframe(
            customers_df.head(10),
            use_container_width=True
        )

    else:

        st.info("No Customers Found")

    # ===============================
    # Appointments
    # ===============================

    st.subheader("Today's Appointments")

    try:

        appt_df = get_appointments()

        st.dataframe(
            appt_df.head(10),
            use_container_width=True
        )

    except:

        st.info(
            "No Appointment Data"
        )