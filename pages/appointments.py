import streamlit as st

from db import (
    get_appointments,
    get_appointment,
    insert_appointment,
    update_appointment,
    delete_appointment
)

def show_appointments():

    st.title("Appointment Management")

    tab1, tab2 = st.tabs([
        "Appointment List",
        "Book Appointment"
    ])

    # ======================================
    # APPOINTMENT LIST
    # ======================================

    with tab1:

        df = get_appointments()

        st.dataframe(
            df,
            use_container_width=True,
            height=450
        )

        st.divider()

        appointment_id = st.number_input(
            "Appointment ID",
            min_value=1,
            step=1
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Load Appointment"
            ):

                appointment = get_appointment(
                    appointment_id
                )

                if appointment:

                    st.session_state.appointment = appointment

                else:

                    st.error(
                        "Appointment Not Found"
                    )

        with col2:

            if st.button(
                "Delete Appointment"
            ):

                delete_appointment(
                    appointment_id
                )

                st.success(
                    "Appointment Deleted"
                )

                st.rerun()

        # ======================================
        # UPDATE
        # ======================================

        if "appointment" in st.session_state:

            a = st.session_state.appointment

            st.divider()

            st.subheader(
                "Update Appointment"
            )

            status = st.selectbox(
                "Status",
                [
                    "Booked",
                    "Completed",
                    "Cancelled"
                ]
            )

            notes = st.text_area(
                "Notes",
                a["notes"] or ""
            )

            if st.button(
                "Update Appointment"
            ):

                update_appointment(
                    a["appointment_id"],
                    status,
                    notes
                )

                st.success(
                    "Appointment Updated"
                )

                st.rerun()

    # ======================================
    # BOOK APPOINTMENT
    # ======================================

    with tab2:

        st.subheader(
            "Book New Appointment"
        )

        customer_id = st.number_input(
            "Customer ID",
            min_value=1,
            step=1
        )

        staff_id = st.number_input(
            "Staff ID",
            min_value=1,
            step=1
        )

        appointment_date = st.date_input(
            "Appointment Date"
        )

        appointment_time = st.time_input(
            "Appointment Time"
        )

        notes = st.text_area(
            "Notes"
        )

        if st.button(
            "Book Appointment"
        ):

            insert_appointment(
                customer_id,
                staff_id,
                appointment_date,
                appointment_time,
                notes
            )

            st.success(
                "Appointment Booked Successfully"
            )

            st.rerun()