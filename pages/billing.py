import streamlit as st
from datetime import datetime

from db import (
    get_bills,
    get_customers_dropdown,
    get_services_dropdown,
    get_staff_dropdown,
    execute_query,
    fetch_one,
    delete_bill
)

# =====================================================
# BILLING PAGE
# =====================================================

def show_billing():

    st.title("POS Billing System")

    tab1, tab2 = st.tabs([
        "Create Bill",
        "Bills History"
    ])

    # =================================================
    # CREATE BILL
    # =================================================

    with tab1:

        customers = get_customers_dropdown()
        services = get_services_dropdown()
        staff = get_staff_dropdown()

        if not customers:
            st.error(
                "No customers found."
            )
            st.stop()

        if not services:
            st.error(
                "No services found."
            )
            st.stop()

        if not staff:
            st.error(
                "No staff found."
            )
            st.stop()

        # ---------------------------------------------
        # MAPS
        # ---------------------------------------------

        customer_map = {
            c["customer_name"]: c["customer_id"]
            for c in customers
        }

        service_map = {
            s["service_name"]: (
                s["service_id"],
                float(s["sale_price"])
            )
            for s in services
        }

        staff_map = {
            s["staff_name"]: s["staff_id"]
            for s in staff
        }

        # ---------------------------------------------
        # INPUTS
        # ---------------------------------------------

        customer_name = st.selectbox(
            "Customer",
            list(customer_map.keys())
        )

        service_name = st.selectbox(
            "Service",
            list(service_map.keys())
        )

        staff_name = st.selectbox(
            "Staff",
            list(staff_map.keys())
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        discount = st.number_input(
            "Discount",
            min_value=0.0,
            value=0.0
        )

        tax = st.number_input(
            "Tax",
            min_value=0.0,
            value=0.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "Card",
                "Online"
            ]
        )

        # ---------------------------------------------
        # CALCULATIONS
        # ---------------------------------------------

        service_id = service_map[
            service_name
        ][0]

        service_price = service_map[
            service_name
        ][1]

        subtotal = quantity * service_price

        grand_total = (
            subtotal
            - discount
            + tax
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Subtotal",
                f"Rs {subtotal:,.2f}"
            )

        with col2:

            st.metric(
                "Grand Total",
                f"Rs {grand_total:,.2f}"
            )

        # ---------------------------------------------
        # SAVE BILL
        # ---------------------------------------------

        if st.button(
            "Generate Bill",
            use_container_width=True
        ):

            customer_id = customer_map[
                customer_name
            ]

            staff_id = staff_map[
                staff_name
            ]

            user_id = st.session_state.user_id

            if not user_id:

                st.error(
                    "User session missing. Please login again."
                )

                st.stop()

            bill_no = (
                "BILL-"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                )
            )

            result = execute_query(
                """
                INSERT INTO bills
                (
                    bill_no,
                    customer_id,
                    user_id,
                    bill_date,
                    subtotal,
                    discount,
                    tax,
                    grand_total,
                    payment_method
                )
                VALUES
                (
                    %s,%s,%s,NOW(),
                    %s,%s,%s,%s,%s
                )
                """,
                (
                    bill_no,
                    customer_id,
                    user_id,
                    subtotal,
                    discount,
                    tax,
                    grand_total,
                    payment_method
                )
            )

            if not result:

                st.error(
                    "Failed to create bill."
                )

                st.stop()

            bill = fetch_one(
                """
                SELECT bill_id
                FROM bills
                ORDER BY bill_id DESC
                LIMIT 1
                """
            )

            bill_id = bill["bill_id"]

            detail_result = execute_query(
                """
                INSERT INTO bill_details
                (
                    bill_id,
                    service_id,
                    staff_id,
                    quantity,
                    price,
                    line_total
                )
                VALUES
                (
                    %s,%s,%s,%s,%s,%s
                )
                """,
                (
                    bill_id,
                    service_id,
                    staff_id,
                    quantity,
                    service_price,
                    subtotal
                )
            )

            if not detail_result:

                st.error(
                    "Bill saved but bill details failed."
                )

                st.stop()

            st.success(
                f"{bill_no} created successfully."
            )

            st.rerun()

    # =================================================
    # BILL HISTORY
    # =================================================

    with tab2:

        st.subheader(
            "Bills History"
        )

        bills_df = get_bills()

        st.dataframe(
            bills_df,
            use_container_width=True,
            height=450
        )

        st.divider()

        bill_id = st.number_input(
            "Bill ID",
            min_value=1,
            step=1,
            key="delete_bill_id"
        )

        if st.button(
            "Delete Bill"
        ):

            delete_bill(
                bill_id
            )

            st.success(
                "Bill Deleted Successfully"
            )

            st.rerun()