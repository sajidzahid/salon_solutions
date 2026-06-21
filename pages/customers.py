import streamlit as st

from db import (
    get_all_customers,
    get_customer,
    insert_customer,
    update_customer,
    delete_customer
)

def show_customers():

    st.title("Customer Management")

    tab1, tab2 = st.tabs([
        "Customer List",
        "Add Customer"
    ])

    # ====================================
    # CUSTOMER LIST
    # ====================================

    with tab1:

        df = get_all_customers()

        st.dataframe(
            df,
            use_container_width=True,
            height=450
        )

        st.divider()

        customer_id = st.number_input(
            "Customer ID",
            min_value=1,
            step=1
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Load Customer"
            ):

                customer = get_customer(
                    customer_id
                )

                if customer:

                    st.session_state.customer = customer

                else:

                    st.error(
                        "Customer Not Found"
                    )

        with col2:

            if st.button(
                "Delete Customer"
            ):

                delete_customer(
                    customer_id
                )

                st.success(
                    "Customer Deleted"
                )

                st.rerun()

        # ====================================
        # EDIT CUSTOMER
        # ====================================

        if "customer" in st.session_state:

            c = st.session_state.customer

            st.divider()

            st.subheader(
                "Edit Customer"
            )

            name = st.text_input(
                "Customer Name",
                c["customer_name"]
            )

            phone = st.text_input(
                "Phone",
                c["phone"]
            )

            email = st.text_input(
                "Email",
                c["email"]
            )

            gender = st.selectbox(
                "Gender",
                ["Male","Female","Other"]
            )

            dob = st.date_input(
                "Date Of Birth",
                c["dob"]
            )

            address = st.text_area(
                "Address",
                c["address"]
            )

            if st.button(
                "Update Customer"
            ):

                update_customer(
                    c["customer_id"],
                    name,
                    phone,
                    email,
                    gender,
                    dob,
                    address
                )

                st.success(
                    "Customer Updated"
                )

                st.rerun()

    # ====================================
    # ADD CUSTOMER
    # ====================================

    with tab2:

        st.subheader(
            "Add New Customer"
        )

        code = st.text_input(
            "Customer Code"
        )

        name = st.text_input(
            "Customer Name"
        )

        phone = st.text_input(
            "Phone"
        )

        email = st.text_input(
            "Email"
        )

        gender = st.selectbox(
            "Gender",
            ["Male","Female","Other"]
        )

        dob = st.date_input(
            "Date Of Birth"
        )

        address = st.text_area(
            "Address"
        )

        referred_by = st.text_input(
            "Referred By"
        )

        if st.button(
            "Add Customer"
        ):

            insert_customer(
                code,
                name,
                phone,
                email,
                gender,
                dob,
                address,
                referred_by
            )

            st.success(
                "Customer Added Successfully"
            )

            st.rerun()