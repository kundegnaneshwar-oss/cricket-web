# AARM Tournaments — Single Page Registration

This version provides the requested flow:

1. Single registration form:
   - Name of Group / Team
   - Captain Name
   - Phone Number
   - OTP verification
   - Email
   - Confirm Booking
2. Confirm Booking opens the payment page.
3. Payment page displays ₹1,399 for one team.
4. Add your real UPI QR image as `payment_qr.png` to show the scanner.
5. After payment confirmation, registration details are emailed to:
   `kundegnaneshwar@gmail.com`

## Run

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

## Real phone OTP

The included app uses a demo OTP so the project can run without paid SMS credentials.

For real SMS OTP verification, connect an SMS provider (for example Twilio, MSG91, or another provider) and replace the demo OTP section with that provider's API.

## Real email delivery

For Gmail SMTP, use a Gmail App Password.

Set environment variables in Terminal before starting Streamlit:

```bash
export AARM_SMTP_USER="your-gmail-address@gmail.com"
export AARM_SMTP_PASSWORD="your-16-character-app-password"
python3 -m streamlit run app.py
```

Do NOT put your Gmail password or App Password directly into `app.py`.

The destination is already set to:

```text
kundegnaneshwar@gmail.com
```

## Payment QR

Place your UPI QR image in the project folder with exactly this filename:

```text
payment_qr.png
```

The payment page will automatically display it.

The app does not automatically verify a bank/UPI payment. It collects the payment/UTR reference and marks the registration as submitted. For automatic payment verification, integrate a payment gateway such as Razorpay or Cashfree.
