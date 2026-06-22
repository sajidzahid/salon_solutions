import streamlit as st
from db import fetch_one

# =====================================================
# SESSION INITIALIZATION
# =====================================================

def init_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "role" not in st.session_state:
        st.session_state.role = None

# =====================================================
# LOGIN
# =====================================================

def login(username, password):

    query = """
    SELECT
        u.user_id,
        u.username,
        u.password_hash,
        u.status,
        r.role_name
    FROM users u

    LEFT JOIN roles r
        ON u.role_id = r.role_id

    WHERE u.username = %s
    """

    user = fetch_one(
        query,
        (username,)
    )

    if not user:
        return False

    if user["status"] != "Active":
        return False

    # Plain Text Password Validation
    # Change to bcrypt later if needed

    if password != user["password_hash"]:
        return False

    st.session_state.logged_in = True
    st.session_state.user_id = user["user_id"]
    st.session_state.username = user["username"]
    st.session_state.role = user["role_name"]

    return True

# =====================================================
# LOGOUT
# =====================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None

# =====================================================
# LOGIN CHECK
# =====================================================

def is_logged_in():

    return st.session_state.logged_in

# =====================================================
# CURRENT USER
# =====================================================

def current_user():

    return {
        "user_id": st.session_state.user_id,
        "username": st.session_state.username,
        "role": st.session_state.role
    }

# =====================================================
# SECURITY HELPERS
# =====================================================

def require_login():

    if not st.session_state.logged_in:

        st.warning(
            "Please login first."
        )

        st.stop()

# -----------------------------------------------------

def require_admin():

    require_login()

    if st.session_state.role != "Admin":

        st.error(
            "Admin Access Only"
        )

        st.stop()

# -----------------------------------------------------

def require_manager():

    require_login()

    if st.session_state.role not in [
        "Admin",
        "Manager"
    ]:

        st.error(
            "Manager Access Only"
        )

        st.stop()

# -----------------------------------------------------

def require_cashier():

    require_login()

    if st.session_state.role not in [
        "Admin",
        "Cashier"
    ]:

        st.error(
            "Cashier Access Only"
        )

        st.stop()

# -----------------------------------------------------

def require_reception():

    require_login()

    if st.session_state.role not in [
        "Admin",
        "Receptionist"
    ]:

        st.error(
            "Reception Access Only"
        )

        st.stop()

# =====================================================
# LOGIN SCREEN
# =====================================================

def login_screen():

    st.markdown(
        """
        <h1 style='text-align:center;'>
            Salon Solutions ERP
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.subheader(
            "User Login"
        )

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            success = login(
                username,
                password
            )

            if success:

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )