import streamlit as st

from auth import (
    init_session,
    login_screen,
    is_logged_in,
    logout
)

st.set_page_config(
    page_title="PGD Students Salon POS",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    section[data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

init_session()

st.markdown(
    """
    <style>
    .main-header{
        font-size:32px;
        font-weight:bold;
        color:#1f2937;
    }
    .kpi-card{
        background-color:#ffffff;
        padding:15px;
        border-radius:10px;
        box-shadow:0px 0px 5px #cccccc;
    }
    .sidebar-title{
        font-size:22px;
        font-weight:bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if not is_logged_in():
    login_screen()
    st.stop()

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3050/3050525.png",
    width=100
)

st.sidebar.markdown("## Salon Solutions ERP")
st.sidebar.divider()

st.sidebar.write(f"👤 {st.session_state.username}")
st.sidebar.write(f"🔐 {st.session_state.role}")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Customers",
        "Appointments",
        "Services",
        "Billing",
        "Inventory",
        "Reports",
        "Users",
        "Data Generator"
    ]
)

st.sidebar.divider()

if st.sidebar.button("Logout"):
    logout()
    st.rerun()

if page == "Dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()
elif page == "Customers":
    from pages.customers import show_customers
    show_customers()
elif page == "Appointments":
    from pages.appointments import show_appointments
    show_appointments()
elif page == "Services":
    from pages.services import show_services
    show_services()
elif page == "Billing":
    from pages.billing import show_billing
    show_billing()
elif page == "Inventory":
    from pages.inventory import show_inventory
    show_inventory()
elif page == "Reports":
    from pages.reports import show_reports
    show_reports()
elif page == "Users":
    from pages.users import show_users
    show_users()
elif page == "Data Generator":
    from pages.data_generator import show_data_generator
    show_data_generator()

