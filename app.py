from forgot_password import reset_password
from login import authenticate
from register import register_user
import io
import sqlite3
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st
from report import generate_pdf
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

st.set_page_config(
    page_title="AI Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

load_css()

try:
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ==================================================
# Authentication Menu
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show authentication only before login
if not st.session_state.logged_in:

    page = st.sidebar.radio(
        "🔐 Authentication",
        [
            "Login",
            "Register",
            "Forgot Password"
        ]
    )

else:
    page = "Dashboard"



# ---------------- Register ----------------
if page == "Register":

    st.title("📝 Create Account")

    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register"):

        if username == "" or password == "":
            st.warning("Please fill all fields.")

        elif password != confirm:
            st.error("Passwords do not match.")

        else:
            try:
                register_user(username, password)
                st.success("✅ Account Created Successfully!")
                st.info("Now select Login from the sidebar.")

            except Exception as e:
                st.error(str(e))

    st.stop()

# ---------------- Forgot Password ----------------
elif page == "Forgot Password":

    st.title("🔑 Forgot Password")

    username = st.text_input("Username", key="fp_user")
    password = st.text_input("New Password", type="password", key="fp_pass")
    confirm = st.text_input("Confirm Password", type="password", key="fp_confirm")

    if st.button("Reset Password"):

        if password != confirm:
            st.error("Passwords do not match.")

        else:
            reset_password(username, password)
            st.success("Password Updated Successfully!")

    st.stop()

# ==================================================
# LOGIN PAGE
# ==================================================

elif page == "Login":

    if not st.session_state.logged_in:

        st.markdown("<br>", unsafe_allow_html=True)

        # Center Logo
        left, center, right = st.columns([2,1,2])

        with center:
            st.image(
                "assets/logo.png",
                width=170
            )

        st.markdown(
            """
            <h1 style='text-align:center;
                       color:#1F2937;
                       font-size:50px;
                       margin-top:10px;
                       margin-bottom:0px;'>
                Ahmed Masood
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <h3 style='text-align:center;
                       color:gray;
                       margin-top:0px;
                       margin-bottom:35px;'>
                AI Business Analytics Dashboard
            </h3>
            """,
            unsafe_allow_html=True
        )

        # Login Card
        c1, c2, c3 = st.columns([1.5,1,1.5])

        with c2:

            st.markdown(
                """
                <div class="login-card">
                <h2 style="text-align:center;">Welcome Back</h2>
                <p style="text-align:center;color:gray;">
                Please sign in to continue
                </p>
                """,
                unsafe_allow_html=True
            )

            username = st.text_input(
                "👤 Username",
                placeholder="Enter Username"
            )

            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter Password"
            )

            remember = st.checkbox("Remember Me")

            col1, col2 = st.columns(2)

            with col2:

                st.markdown(
                    """
                    <p style="text-align:right;
                    color:#2563EB;
                    font-weight:600;">
                    Forgot Password?
                    </p>
                    """,
                    unsafe_allow_html=True
                )

            if st.button(
                "🔓 Login",
                use_container_width=True
            ):

                if authenticate(username, password):

                    st.session_state.logged_in = True

                    st.success("Login Successful")

                    st.rerun()

                else:

                    st.error("Invalid Username or Password")

            st.markdown("<hr>", unsafe_allow_html=True)

            st.markdown(
                "<p style='text-align:center;'>Don't have an account?</p>",
                unsafe_allow_html=True
            )

            if st.button(
                "📝 Create New Account",
                use_container_width=True
            ):
                st.session_state.page = "Register"

            st.markdown("</div>", unsafe_allow_html=True)

        st.stop()

#
# -----------------------------
# Login Logo
# -----------------------------
col1, col2, col3 = st.columns([2,1,2])

with col2:
    st.image("assets/logo.png", width=170)

st.markdown(
    "<h1 style='text-align:center;'>Ahmed Masood</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>AI Business Analytics Dashboard</h4>",
    unsafe_allow_html=True
)
# -----------------------------
# Register Page
# -----------------------------
if page == "Register":

    st.title("📝 Create Account")

    new_username = st.text_input(
        "Username",
        key="reg_user"
    )

    new_password = st.text_input(
        "Password",
        type="password",
        key="reg_pass"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="reg_confirm"
    )

    if st.button("Register"):

        if new_username == "" or new_password == "":
            st.warning("Please fill all fields.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:
            try:
                register_user(new_username, new_password)

                st.success("✅ Account created successfully!")
                st.info("Please select Login from the sidebar.")

            except Exception:
                st.error("Username already exists.")

    st.stop()

# -----------------------------
# Login Page
# -----------------------------
if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button("Login"):

        if authenticate(username, password):

            st.session_state.logged_in = True

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Username or Password")

    st.stop()
# -----------------------------
# Forgot Password Page
# -----------------------------
elif page == "Forgot Password":

    st.title("🔑 Reset Your Password")

    st.markdown("""
    Enter your username and create a new password.
    """)

    with st.form("forgot_form"):

        username = st.text_input(
            "👤 Username"
        )

        new_password = st.text_input(
            "🔒 New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password"
        )

        submit = st.form_submit_button("🔄 Reset Password")

    if submit:

        if username == "":
            st.warning("Please enter your username.")

        elif new_password == "":
            st.warning("Please enter a new password.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:

            success = reset_password(
                username,
                new_password
            )

            if success:

                st.success("✅ Password changed successfully.")

                st.info("Now go to the Login page and sign in with your new password.")

                if st.button("🔐 Go to Login"):
                    st.rerun()

            else:

                st.error("❌ Username not found.")
# ---------- Database ----------
conn = sqlite3.connect("analytics.db")
df = pd.read_sql("SELECT * FROM sales", conn)
conn.close()

df["Date"] = pd.to_datetime(df["Date"])

# ---------- Sidebar ----------
st.sidebar.title("📊 AI Dashboard")
menu = st.sidebar.radio("Navigation",
                        ["Dashboard","Prediction","Reports"])

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in=False
    st.rerun()

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

if menu=="Dashboard":
    st.title("📊 AI Business Analytics Dashboard")

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Revenue",f"${filtered_df['Total'].sum():,.0f}")
    c2.metric("Orders",len(filtered_df))
    c3.metric("Customers",filtered_df["Customer"].nunique())
    c4.metric("Avg Order",f"${filtered_df['Total'].mean():.2f}")

    st.subheader("Revenue Trend")
    daily=filtered_df.groupby("Date",as_index=False)["Total"].sum()
    st.plotly_chart(px.line(daily,x="Date",y="Total",markers=True),
                    use_container_width=True)

    st.subheader("Top Products")
    top=(filtered_df.groupby("Product",as_index=False)["Total"]
         .sum().sort_values("Total",ascending=False))
    st.plotly_chart(px.bar(top,x="Product",y="Total",
                           color="Product"),
                    use_container_width=True)

    col1,col2=st.columns(2)

    with col1:
        cat=(filtered_df.groupby("Category",as_index=False)["Total"].sum())
        st.plotly_chart(px.bar(cat,x="Category",y="Total"),
                        use_container_width=True)

    with col2:
        reg=(filtered_df.groupby("Region",as_index=False)["Total"].sum())
        st.plotly_chart(px.pie(reg,names="Region",values="Total",hole=.45),
                        use_container_width=True)

    st.subheader("Sales Summary")
    summary=(filtered_df.groupby("Category")
             .agg(Revenue=("Total","sum"),
                  Orders=("OrderID","count"),
                  Quantity=("Quantity","sum"))
             .reset_index())
    st.dataframe(summary,use_container_width=True)

    search=st.text_input("Search Customer/Product")
    view=filtered_df.copy()
    if search:
        view=view[
            view["Customer"].str.contains(search,case=False)|
            view["Product"].str.contains(search,case=False)
        ]

    st.dataframe(view,use_container_width=True)

elif menu=="Prediction":
    st.title("🤖 AI Sales Prediction")
    model=joblib.load("models/sales_model.pkl")
    qty=st.number_input("Quantity",1,100,2)
    price=st.number_input("Price",1.0,100000.0,100.0)
    pred=model.predict([[qty,price]])
    st.success(f"Predicted Revenue: ${pred[0]:,.2f}")

else:
    st.title("📄 Reports")
    csv=filtered_df.to_csv(index=False)
    st.download_button("Download CSV",csv,"sales_report.csv","text/csv")

    excel=io.BytesIO()
    with pd.ExcelWriter(excel,engine="openpyxl") as writer:
        filtered_df.to_excel(writer,index=False,sheet_name="Sales")
    excel.seek(0)
    st.download_button("Download Excel",excel,
                       "sales_report.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    pdf=generate_pdf(filtered_df)
    with open(pdf,"rb") as f:
        st.download_button("Download PDF",f,
                           "sales_report.pdf",
                           "application/pdf")
