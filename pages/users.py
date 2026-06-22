import streamlit as st

from db import (
    get_users,
    get_user,
    insert_user,
    update_user,
    delete_user
)

def show_users():

    st.title("User Management")

    tab1, tab2 = st.tabs([
        "User List",
        "Add User"
    ])

    # ==================================
    # USER LIST
    # ==================================

    with tab1:

        df = get_users()

        st.dataframe(
            df,
            use_container_width=True,
            height=450
        )

        st.divider()

        user_id = st.number_input(
            "User ID",
            min_value=1,
            step=1
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Load User"
            ):

                user = get_user(
                    user_id
                )

                if user:

                    st.session_state.user = user

                else:

                    st.error(
                        "User Not Found"
                    )

        with col2:

            if st.button(
                "Delete User"
            ):

                delete_user(
                    user_id
                )

                st.success(
                    "User Deleted"
                )

                st.rerun()

        # ==================================
        # EDIT USER
        # ==================================

        if "user" in st.session_state:

            u = st.session_state.user

            st.divider()

            st.subheader(
                "Edit User"
            )

            username = st.text_input(
                "Username",
                u["username"],
                disabled=True
            )

            email = st.text_input(
                "Email",
                u["email"]
            )

            status = st.selectbox(
                "Status",
                [
                    "Active",
                    "Inactive"
                ]
            )

            if st.button(
                "Update User"
            ):

                update_user(
                    u["user_id"],
                    email,
                    status
                )

                st.success(
                    "User Updated"
                )

                st.rerun()

    # ==================================
    # ADD USER
    # ==================================

    with tab2:

        st.subheader(
            "Add New User"
        )

        branch_id = st.number_input(
            "Branch ID",
            min_value=1,
            step=1
        )

        role_id = st.number_input(
            "Role ID",
            min_value=1,
            step=1
        )

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Add User"
        ):

            insert_user(
                branch_id,
                role_id,
                username,
                email,
                password
            )

            st.success(
                "User Added Successfully"
            )

            st.rerun()