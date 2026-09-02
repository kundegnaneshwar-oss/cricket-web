import os
import random
import smtplib
from email.message import EmailMessage
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="AARM Tournaments",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f5f8fc 0%, #ffffff 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .brand {
        text-align: center;
        padding: 18px 0 8px;
    }

    .brand h1 {
        margin: 0;
        color: #0a3558;
        font-size: 42px;
        font-weight: 850;
        letter-spacing: -1px;
    }

    .brand p {
        margin: 4px 0 0;
        color: #667085;
        font-size: 15px;
    }

    .form-card, .payment-card, .success-card {
        background: white;
        border: 1px solid #e4e9ef;
        border-radius: 22px;
        padding: 28px;
        box-shadow: 0 12px 35px rgba(16, 24, 40, .08);
    }

    .title {
        color: #102a43;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .subtitle {
        color: #667085;
        margin-bottom: 20px;
    }

    .price-box {
        background: #eef8f5;
        border: 1px solid #cdece3;
        border-radius: 15px;
        padding: 15px 18px;
        margin: 15px 0 20px;
        text-align: center;
    }

    .price {
        color: #087f5b;
        font-size: 30px;
        font-weight: 850;
    }

    .price-label {
        color: #667085;
        font-size: 13px;
    }

    .otp-note {
        background: #fff8e7;
        border: 1px solid #f5df9b;
        padding: 11px 14px;
        border-radius: 12px;
        color: #755b00;
        font-size: 13px;
        margin: 5px 0 15px;
    }

    .payment-title {
        text-align: center;
        color: #102a43;
        font-size: 30px;
        font-weight: 850;
    }

    .payment-amount {
        text-align: center;
        color: #087f5b;
        font-size: 38px;
        font-weight: 900;
        margin: 5px 0 15px;
    }

    .qr-placeholder {
        border: 2px dashed #b9c2cc;
        border-radius: 18px;
        padding: 45px 20px;
        text-align: center;
        color: #667085;
        margin: 10px 0 18px;
        background: #fafbfc;
    }

    .qr-placeholder .big {
        font-size: 54px;
    }

    .success-card {
        text-align: center;
        border-color: #b7ead8;
        background: #f3fffa;
    }

    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 12px;
        margin-top: 30px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 46px;
        font-weight: 750;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Email
# -----------------------------
def send_registration_email(data):
    """
    Configure these environment variables before running:
      AARM_SMTP_USER       Gmail address used to send the email
      AARM_SMTP_PASSWORD   Gmail App Password (NOT your normal password)

    The destination is fixed to the requested registration email.
    """
    smtp_user = os.getenv("AARM_SMTP_USER")
    smtp_password = os.getenv("AARM_SMTP_PASSWORD")
    destination = "kundegnaneshwar@gmail.com"

    if not smtp_user or not smtp_password:
        return False, (
            "Email sending is not configured yet. Set AARM_SMTP_USER and "
            "AARM_SMTP_PASSWORD before running the website."
        )

    body = f"""
New AARM Tournaments registration

Group Name: {data['group_name']}
Captain Name: {data['captain_name']}
Phone Number: {data['phone']}
Email: {data['email']}
Payment Status: {data['payment_status']}
Registration Time: {data['registered_at']}

Amount: ₹1,399
"""

    msg = EmailMessage()
    msg["Subject"] = f"AARM Tournaments - New Registration - {data['group_name']}"
    msg["From"] = smtp_user
    msg["To"] = destination
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        return True, "Registration details sent successfully."
    except Exception as exc:
        return False, f"Email could not be sent: {exc}"


# -----------------------------
# Session state
# -----------------------------
for key, default in {
    "otp_sent": False,
    "otp": None,
    "phone_verified": False,
    "booking": None,
    "payment_page": False,
    "payment_submitted": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="brand">
    <h1>🏏 AARM TOURNAMENTS</h1>
    <p>Box Cricket Tournament Registration</p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Payment page
# -----------------------------
if st.session_state.payment_page:
    st.markdown('<div class="payment-card">', unsafe_allow_html=True)
    st.markdown('<div class="payment-title">Payment</div>', unsafe_allow_html=True)
    st.markdown('<div class="payment-amount">₹1,399</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;color:#667085;">Single team registration fee</p>',
        unsafe_allow_html=True,
    )

    # Put your real UPI QR image at project root as payment_qr.png.
    qr_path = os.path.join(os.path.dirname(__file__), "payment_qr.png")
    if os.path.exists(qr_path):
        st.image(qr_path, caption="Scan to pay ₹1,399", width=280)
    else:
        st.markdown("""
        <div class="qr-placeholder">
            <div class="big">▦</div>
            <b>PAYMENT QR SCANNER</b>
            <br><br>
            Add your real UPI QR image as <b>payment_qr.png</b>
            in the same folder as <b>app.py</b>.
            <br><br>
            Amount: <b>₹1,399</b>
        </div>
        """, unsafe_allow_html=True)

    st.info("After paying, enter the payment/UTR reference below. The registration will then be emailed to kundegnaneshwar@gmail.com.")

    with st.form("payment_form"):
        payment_ref = st.text_input(
            "Payment / UTR Reference",
            placeholder="Enter your payment reference",
        )
        paid = st.checkbox("I have completed the payment of ₹1,399.")
        submit_payment = st.form_submit_button("Confirm Payment & Registration", type="primary")

    if submit_payment:
        if not paid or not payment_ref.strip():
            st.error("Please complete the payment and enter the payment/UTR reference.")
        else:
            booking = st.session_state.booking
            booking["payment_status"] = "Payment marked as completed"
            booking["payment_reference"] = payment_ref.strip()
            booking["registered_at"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")

            sent, message = send_registration_email(booking)

            if sent:
                st.session_state.payment_submitted = True
                st.markdown("""
                <div class="success-card">
                    <h2>✅ Registration Successful</h2>
                    <p>Your team registration and payment reference have been submitted.</p>
                    <p><b>AARM Tournaments</b> will receive the registration details by email.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(message)
                st.info("Your form data is still captured in this session. Configure Gmail SMTP/App Password to enable automatic email delivery.")

    if st.button("← Back to Registration Form"):
        st.session_state.payment_page = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # -----------------------------
    # Single-page registration form
    # -----------------------------
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Team Registration</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Fill in the details below to book one team for the tournament.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="price-box">
        <div class="price-label">SINGLE TEAM REGISTRATION</div>
        <div class="price">₹1,399</div>
    </div>
    """, unsafe_allow_html=True)

    group_name = st.text_input("Name of Group / Team", placeholder="Enter your team name")
    captain_name = st.text_input("Captain Name", placeholder="Enter captain name")
    phone = st.text_input("Phone Number", placeholder="Enter 10-digit mobile number")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Send OTP", use_container_width=True):
            clean_phone = "".join(ch for ch in phone if ch.isdigit())
            if len(clean_phone) != 10:
                st.error("Enter a valid 10-digit Indian mobile number.")
            else:
                # Demo OTP. For production, connect this function to an SMS provider.
                otp = str(random.randint(100000, 999999))
                st.session_state.otp = otp
                st.session_state.otp_sent = True
                st.session_state.phone_verified = False
                st.info(f"Demo OTP: {otp}. Connect an SMS provider to send it to the phone automatically.")
    with c2:
        if st.session_state.phone_verified:
            st.success("✓ Number verified")

    if st.session_state.otp_sent and not st.session_state.phone_verified:
        st.markdown(
            '<div class="otp-note">Enter the OTP sent to your phone to verify the number.</div>',
            unsafe_allow_html=True,
        )
        otp_entered = st.text_input("Enter OTP", max_chars=6, placeholder="6-digit OTP")
        if st.button("Verify OTP", use_container_width=True):
            if otp_entered == st.session_state.otp:
                st.session_state.phone_verified = True
                st.success("Phone number verified successfully.")
            else:
                st.error("Incorrect OTP. Please try again.")

    email = st.text_input("Email Address", placeholder="Enter your email")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#667085;font-size:13px;">By continuing, you confirm that the team details are correct.</p>',
        unsafe_allow_html=True,
    )

    if st.button("Confirm Booking →", type="primary", use_container_width=True):
        if not group_name.strip():
            st.error("Please enter the group/team name.")
        elif not captain_name.strip():
            st.error("Please enter the captain name.")
        elif not st.session_state.phone_verified:
            st.error("Please verify the phone number with OTP.")
        elif not email.strip() or "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            st.session_state.booking = {
                "group_name": group_name.strip(),
                "captain_name": captain_name.strip(),
                "phone": phone.strip(),
                "email": email.strip(),
                "payment_status": "Pending",
                "payment_reference": "",
                "registered_at": "",
            }
            st.session_state.payment_page = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    AARM Tournaments • Box Cricket Registration<br>
    Team registration fee: ₹1,399
</div>
""", unsafe_allow_html=True)
