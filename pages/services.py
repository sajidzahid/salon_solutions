import streamlit as st

from db import (
    get_services,
    get_service,
    insert_service,
    update_service,
    delete_service
)

def show_services():

    st.title("Service Management")

    tab1, tab2 = st.tabs([
        "Service List",
        "Add Service"
    ])

    # ==================================
    # SERVICE LIST
    # ==================================

    with tab1:

        df = get_services()

        st.dataframe(
            df,
            use_container_width=True,
            height=450
        )

        st.divider()

        service_id = st.number_input(
            "Service ID",
            min_value=1,
            step=1
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Load Service"
            ):

                service = get_service(
                    service_id
                )

                if service:

                    st.session_state.service = service

                else:

                    st.error(
                        "Service Not Found"
                    )

        with col2:

            if st.button(
                "Delete Service"
            ):

                delete_service(
                    service_id
                )

                st.success(
                    "Service Deleted"
                )

                st.rerun()

        # ===============================
        # EDIT SERVICE
        # ===============================

        if "service" in st.session_state:

            s = st.session_state.service

            st.divider()

            st.subheader(
                "Edit Service"
            )

            service_name = st.text_input(
                "Service Name",
                s["service_name"]
            )

            sale_price = st.number_input(
                "Sale Price",
                value=float(
                    s["sale_price"] or 0
                )
            )

            discounted_price = st.number_input(
                "Discounted Price",
                value=float(
                    s["discounted_price"] or 0
                )
            )

            loyalty_points = st.number_input(
                "Loyalty Points",
                value=int(
                    s["loyalty_points"] or 0
                )
            )

            duration_minutes = st.number_input(
                "Duration Minutes",
                value=int(
                    s["duration_minutes"] or 0
                )
            )

            if st.button(
                "Update Service"
            ):

                update_service(
                    s["service_id"],
                    service_name,
                    sale_price,
                    discounted_price,
                    loyalty_points,
                    duration_minutes
                )

                st.success(
                    "Service Updated"
                )

                st.rerun()

    # ==================================
    # ADD SERVICE
    # ==================================

    with tab2:

        st.subheader(
            "Add New Service"
        )

        category_id = st.number_input(
            "Category ID",
            min_value=1,
            step=1
        )

        service_name = st.text_input(
            "Service Name"
        )

        sale_price = st.number_input(
            "Sale Price",
            min_value=0.0
        )

        discounted_price = st.number_input(
            "Discounted Price",
            min_value=0.0
        )

        loyalty_points = st.number_input(
            "Loyalty Points",
            min_value=0
        )

        duration_minutes = st.number_input(
            "Duration Minutes",
            min_value=1
        )

        if st.button(
            "Add Service"
        ):

            insert_service(
                category_id,
                service_name,
                sale_price,
                discounted_price,
                loyalty_points,
                duration_minutes
            )

            st.success(
                "Service Added Successfully"
            )

            st.rerun()