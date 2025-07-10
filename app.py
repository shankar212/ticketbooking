from gsheets import append_booking_to_gsheet
from gsheets import get_booked_seats
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import qrcode
import io
import random
import os
from datetime import datetime
import streamlit.components.v1 as components
import urllib.parse
import uuid
import requests
import logging

# ---------------------------- SETTINGS ----------------------------
UPI_ID = os.getenv("UPI_ID", "9154317035@ibl")
PAYEE_NAME = "DAARUNAM"
AMOUNT_PER_SEAT = 50
CSV_PATH = "booking_data.csv"
QR_PATH = "generated_upi_qr.png"
POSTER_PATH = "poster.jpg"  # Replace with your real poster file
CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID", "TEST10710960cff9577f81240f7d026806901701")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY", "cfsk_ma_test_9ba8fd822f213f86035d392b1f89a645_c46125d7")
CASHFREE_BASE_URL = "https://api.cashfree.com/pg/orders"  # Production endpoint for test mode
NGROK_URL = os.getenv("NGROK_URL", "https://moviebookingonline.streamlit.app")  # Replace with ngrok HTTPS URL for local testing

# ---------------------------- INITIALIZATION ----------------------------
st.set_page_config(page_title="DAARUNAM Booking", layout="wide", page_icon="🎬")
logging.basicConfig(level=logging.DEBUG)

# Initialize local CSV
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"]).to_csv(CSV_PATH, index=False)

# Get booked seats from Google Sheet
try:
    booked_seats = get_booked_seats()
except Exception as e:
    st.error("❌ Failed to load booked seats from Google Sheet.")
    st.exception(e)
    booked_seats = set()

# Ensure QR exists
if not os.path.exists(QR_PATH):
    qr_img = qrcode.make(f"upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am=50&cu=INR")
    qr_img.save(QR_PATH)

# Initialize session state
if "booking" not in st.session_state:
    st.session_state.booking = {}
if "step" not in st.session_state:
    st.session_state.step = "form"
if "order_id" not in st.session_state:
    st.session_state.order_id = None

# ---------------------------- CUSTOM CSS & JS -----------------------
st.markdown("""
<style>
/* ===================== GLOBAL ===================== */
body, .stApp {
    background: linear-gradient(135deg, #0f0f0f, #1c2526);
    color: #ffffff;
    font-family: 'Montserrat', sans-serif;
    overflow-x: hidden;
    scroll-behavior: smooth;
}

/* ===================== BACKGROUND PARTICLES ===================== */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('https://www.transparenttextures.com/patterns/dark-mosaic.png');
    opacity: 0.03;
    z-index: -2;
    animation: drift 60s linear infinite;
}
@keyframes drift {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-100px, -100px); }
}

.particles {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: -1;
}
.particle {
    position: absolute;
    background: rgba(255, 204, 0, 0.4);
    border-radius: 50%;
    animation: float 15s linear infinite;
}
@keyframes float {
    0% { transform: translateY(0) scale(1); opacity: 0.8; }
    100% { transform: translateY(-100vh) scale(0.5); opacity: 0; }
}

/* ===================== HEADINGS ===================== */
h1 {
    font-size: 4rem;
    color: #ffcc00;
    text-shadow: 0 0 20px rgba(255, 204, 0, 0.7);
    animation: glow 2s ease-in-out infinite alternate;
    text-align: center;
}
h3 {
    font-size: 1.8rem;
    color: #eeeeee;
    text-align: center;
    animation: fadeIn 2s ease-out;
}
@keyframes glow {
    from { text-shadow: 0 0 10px rgba(255, 204, 0, 0.3); }
    to   { text-shadow: 0 0 25px rgba(255, 204, 0, 0.8); }
}

/* ===================== CARD STYLING ===================== */
.card {
    background: rgba(25, 25, 25, 0.95);
    border: 1px solid #ffcc00;
    border-radius: 18px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 35px rgba(255, 204, 0, 0.2);
}

/* ===================== BUTTON ===================== */
.stButton > button {
    background: linear-gradient(90deg, #ffcc00, #ff6600);
    color: #1a1a1a;
    font-weight: 600;
    border: none;
    border-radius: 30px;
    padding: 12px 25px;
    cursor: pointer;
    transition: 0.3s ease;
    box-shadow: 0 5px 12px rgba(255, 204, 0, 0.3);
}
.stButton > button:hover {
    background: linear-gradient(90deg, #ff3300, #ff3300);
    transform: scale(1.03);
    box-shadow: 0 8px 25px rgba(255, 102, 0, 0.5);
}

/* ===================== INPUTS ===================== */
.stTextInput > div > input,
.stMultiSelect > div {
    background: #2a2a2a;
    color: #ffffff;
    border: 2px solid #ffcc00;
    border-radius: 10px;
    padding: 10px;
    font-size: 1rem;
    transition: all 0.3s ease;
}
.stTextInput > div > input:focus,
.stMultiSelect > div:focus-within {
    border-color: #ff6600;
    box-shadow: 0 0 10px rgba(255, 102, 0, 0.4);
}

/* ===================== DIVIDER ===================== */
hr, .stDivider {
    border: none;
    height: 3px;
    background: #ffcc00;
    margin: 35px 0;
    animation: slideIn 1.2s ease-in-out;
}
@keyframes slideIn {
    0% { width: 0; opacity: 0; }
    100% { width: 100%; opacity: 1; }
}

/* ===================== ANIMATIONS ===================== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ===================== RESPONSIVE ===================== */
@media (max-width: 768px) {
    h1 { font-size: 2.5rem; }
    h3 { font-size: 1.3rem; }
    .card { padding: 15px; }
    .stButton > button { padding: 10px 20px; }
}
</style>

<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap" rel="stylesheet">

<script>
// Particle JS (on DOM ready)
function createParticles() {
    const container = document.createElement('div');
    container.className = 'particles';
    document.body.appendChild(container);

    for (let i = 0; i < 40; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        const size = Math.random() * 6 + 4;
        particle.style.width = particle.style.height = size + 'px';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = Math.random() * 100 + 'vh';
        particle.style.animationDuration = (Math.random() * 15 + 8) + 's';
        particle.style.animationDelay = (Math.random() * 10) + 's';
        container.appendChild(particle);
    }
}
document.addEventListener('DOMContentLoaded', createParticles);
</script>
""", unsafe_allow_html=True)

# ---------------------------- HEADER ----------------------------
st.markdown("<h1>🎬 DAARUNAM</h1>", unsafe_allow_html=True)
st.markdown("<h3>Now Booking — ₹50 Per Seat</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    if os.path.exists(POSTER_PATH):
        st.image(POSTER_PATH, width=350, caption="Official Poster")
with col2:
    st.markdown("""
    <div class='card'>
        <p><strong>📅 Releasing:</strong> 12th July 2025</p>
        <p><strong>📍 Venue:</strong> TTD Kalyana Mandapam, Gandhi Park Road, Adilabad</p>
        <p><strong>🎞 Genre:</strong> Thriller • Telugu</p>
        <p><strong>⏱ Duration:</strong> 2h 14min</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------------------- STEP 1: FORM ----------------------------
st.subheader("✍️ Step 1: Enter Booking Details")
available_seats = [str(i) for i in range(1, 301) if str(i) not in booked_seats]

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.form("booking_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        mobile = st.text_input("Mobile Number", placeholder="Enter your 10-digit mobile number")
        selected_seats = st.multiselect("Select Your Seat Numbers", available_seats, max_selections=10, placeholder="Choose available seats")
        total_amount = len(selected_seats) * AMOUNT_PER_SEAT
        st.markdown(f"<p style='font-size:1.3rem; color:#ffcc00;'>💰 <strong>Total Payable:</strong> ₹{total_amount}</p>", unsafe_allow_html=True)
        form_submit = st.form_submit_button("Proceed to Payment")
    st.markdown("</div>", unsafe_allow_html=True)

if form_submit:
    if not name.strip() or not mobile.strip() or not selected_seats:
        st.error("Please fill all details and select at least one seat.")
    elif not mobile.isdigit() or len(mobile) != 10:
        st.error("Mobile number must be exactly 10 digits and contain only numbers.")
    else:
        st.session_state.booking = {
            "name": name.strip(),
            "mobile": mobile.strip(),
            "seats": selected_seats,
            "amount": total_amount
        }
        st.session_state.step = "payment"
        st.rerun()

# ---------------------------- TICKET GENERATION FUNCTION ----------------------------
def generate_ticket(name, seats, amount, uid, txn_id):
    ticket = Image.new("RGB", (1400, 700), "#ffffff")
    draw = ImageDraw.Draw(ticket)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 60)
        font_text = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Background gradient
    for y in range(700):
        r = 30 + (y / 700) * 20
        g = 30
        b = 40
        draw.line((0, y, 1400, y), fill=(int(r), int(g), int(b)))

    # Perforated edges
    for x in [50, 1350]:
        for y in range(50, 650, 10):
            draw.ellipse((x-5, y-5, x+5, y+5), fill="#888888")
    for y in [50, 650]:
        for x in range(50, 1350, 10):
            draw.ellipse((x-5, y-5, x+5, y+5), fill="#888888")

    # Header
    draw.rectangle([50, 50, 1350, 150], fill="#ffcc00")
    draw.text((60, 60), "🎬 DAARUNAM MOVIE TICKET", font=font_title, fill="#1a1a1a")

    # Poster
    x = 400
    if os.path.exists(POSTER_PATH):
        poster = Image.open(POSTER_PATH).resize((300, 400))
        ticket.paste(poster, (60, 180))

    # Details
    draw.text((x, 180), f"Name: {name}", font=font_text, fill="#ffffff")
    draw.text((x, 240), f"Seats: {', '.join(seats)}", font=font_text, fill="#ffffff")
    draw.text((x, 300), f"Amount: ₹{amount}", font=font_text, fill="#ffffff")
    draw.text((x, 360), f"UID: {uid}", font=font_text, fill="#ffffff")
    draw.text((x, 420), f"Txn ID: {txn_id}", font=font_text, fill="#ffffff")
    draw.text((x, 480), f"Paid To: {UPI_ID}", font=font_text, fill="#ffffff")
    draw.text((x, 540), f"Date: 12 July 2025 • Venue: TTD Kalyana Mandapam", font=font_small, fill="#cccccc")

    # QR Code
    qr = qrcode.make(uid)
    qr = qr.resize((100, 100))
    ticket.paste(qr, (1250, 550))

    return ticket

# ---------------------------- STEP 2: PAYMENT ----------------------------
if st.session_state.get("step") == "payment":
    info = st.session_state.get("booking")
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.success("🎉 Booking Info Confirmed")
    st.markdown(f"""
    <p><strong>Name:</strong> {info['name']}</p>
    <p><strong>Mobile:</strong> {info['mobile']}</p>
    <p><strong>Seats:</strong> {', '.join(info['seats'])}</p>
    <p style='color:#ffcc00;'><strong>💰 Pay:</strong> ₹{info['amount']}</p>
    """, unsafe_allow_html=True)

    # Generate dynamic UPI QR code
    qr_img = qrcode.make(f"upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am={info['amount']}&cu=INR")
    qr_img.save(QR_PATH)
    st.image(QR_PATH, caption=f"Scan to Pay ₹{info['amount']} via UPI (or use Cashfree below)", width=300)
    st.markdown(f"<a href='upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am={info['amount']}&cu=INR' style='color:#ffcc00; text-decoration:none; font-weight:bold;'>🔗 Pay via UPI App</a>", unsafe_allow_html=True)
    st.info("After paying via UPI, submit your Transaction ID below for manual verification.")

    with st.form("upi_verification"):
        upi_txn_id = st.text_input("Enter UPI Transaction ID")
        submit_upi = st.form_submit_button("Submit UPI Transaction ID")
        if submit_upi and upi_txn_id:
            st.success(f"UPI Transaction ID {upi_txn_id} submitted. We will verify and send your ticket.")
            try:
                if not os.path.exists(CSV_PATH):
                    booked_df = pd.DataFrame(columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"])
                else:
                    booked_df = pd.read_csv(CSV_PATH)
                uid = f"DRN{random.randint(100, 999)}"
                seat_str = ", ".join(info['seats'])
                new_row = pd.DataFrame([[info['name'], info['mobile'], seat_str, uid, upi_txn_id, info['amount']]],
                                       columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"])
                updated_df = pd.concat([booked_df, new_row], ignore_index=True)
                updated_df.to_csv(CSV_PATH, index=False)
                append_booking_to_gsheet(info['name'], info['mobile'], seat_str, uid, upi_txn_id, info['amount'])
                ticket_img = generate_ticket(info['name'], info['seats'], info['amount'], uid, upi_txn_id)
                buffer = io.BytesIO()
                ticket_img.save(buffer, format="PNG")
                buffer.seek(0)
                st.image(ticket_img, caption="🎫 Your Ticket — Show at Entry (Pending UPI Verification)")
                st.download_button("📥 Download Ticket", buffer, file_name=f"ticket_{uid}.png", mime="image/png")
                st.success(f"✅ Booking Submitted! Your UID is: `{uid}`. Await UPI verification.")
                st.session_state.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to process UPI booking: {str(e)}")
                logging.error(f"UPI booking error: {e}")

    # Cashfree Payment Integration
    order_id = f"DAARUNAM_{uuid.uuid4().hex[:8]}"
    return_url = (
        f"https://moviebookingonline.streamlit.app/"  # Use https://moviebookingonline.streamlit.app or ngrok HTTPS URL
        f"?payment=success&oid={order_id}"
        f"&name={urllib.parse.quote_plus(info['name'])}"
        f"&mobile={info['mobile']}"
        f"&seats={','.join(info['seats'])}"
        f"&amount={info['amount']}"
        f"&cf_id={order_id}"
    )

    payload = {
        "customer_details": {
            "customer_id": info['mobile'],
            "customer_email": "test@example.com",
            "customer_phone": info['mobile']
        },
        "order_amount": float(info['amount']),
        "order_currency": "INR",
        "order_id": order_id,
        "order_meta": {
            "return_url": return_url
        }
    }

    headers = {
        "x-api-version": "2023-08-01",
        "Content-Type": "application/json",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }

    if st.button("💳 Pay via Cashfree"):
        logging.debug(f"Sending payload: {payload}")
        logging.debug(f"Headers: {headers}")
        try:
            response = requests.post(CASHFREE_BASE_URL, json=payload, headers=headers)
            logging.debug(f"Response status: {response.status_code}, Response body: {response.text}")
            if response.status_code == 200:
                payment_link = response.json().get("payment_link")
                st.markdown(f"[👉 Click to Pay ₹{info['amount']}]({payment_link})", unsafe_allow_html=True)
                st.session_state.order_id = order_id
                st.info(f"After completing the payment, you will be redirected to: {return_url}")
                st.info("Ensure the return URL is whitelisted in the Cashfree dashboard (Developers > Webhooks).")
            elif response.status_code == 400 and response.json().get("code") == "order_meta.return_url_invalid":
                st.error("❌ Invalid return URL. Cashfree requires an HTTPS URL.")
                st.json(response.json())
                st.info("For local testing, run `ngrok http 8501` and update NGROK_URL in secrets.toml with the HTTPS URL. For production, use your Streamlit Cloud URL (e.g., https://moviebookingonline.streamlit.app).")
            elif response.status_code == 401:
                st.error("❌ Authentication failed with Cashfree. Please check your API credentials or contact support.")
                st.json(response.json())
                st.info("Ensure CASHFREE_APP_ID and CASHFREE_SECRET_KEY are valid test credentials.")
            else:
                st.error(f"❌ Failed to initiate payment with Cashfree. Status: {response.status_code}")
                st.json(response.json())
        except Exception as e:
            st.error(f"❌ Payment request failed: {str(e)}")
            logging.error(f"Payment error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------- POST-PAYMENT REDIRECT HANDLING ----------------------------
query_params = st.query_params
logging.debug(f"Received query params: {query_params}")
st.markdown(f"<p style='color:#cccccc;'>Debug: Received query params: {query_params}</p>", unsafe_allow_html=True)

if query_params.get("payment") == "success" and "oid" in query_params:
    logging.debug("Post-payment logic triggered")
    # Reconstruct booking details
    order_id = query_params["oid"]
    name = urllib.parse.unquote_plus(query_params.get("name", "Guest"))
    mobile = query_params.get("mobile", "")
    seats = query_params.get("seats", "").split(",")
    amount = int(query_params.get("amount", 0))

    # Verify seats are still available
    try:
        booked_seats = get_booked_seats()
        if any(seat in booked_seats for seat in seats):
            st.error("One or more selected seats are already booked. Please choose different seats.")
            st.session_state.clear()
            st.rerun()
    except Exception as e:
        st.error(f"❌ Failed to verify seat availability: {str(e)}")
        logging.error(f"Seat verification error: {e}")
        st.rerun()

    # Verify payment status
    verify_url = f"{CASHFREE_BASE_URL}/{order_id}"
    headers = {
        "x-api-version": "2023-08-01",
        "Content-Type": "application/json",
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY
    }
    try:
        response = requests.get(verify_url, headers=headers)
        logging.debug(f"Verification response: {response.status_code}, {response.text}")
        if response.status_code == 200 and response.json().get("order_status") == "PAID":
            uid = f"DRN{random.randint(100, 999)}"
            txn_id = order_id
            seat_str = ", ".join(seats)

            # Save to CSV
            if not os.path.exists(CSV_PATH):
                booked_df = pd.DataFrame(columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"])
            else:
                booked_df = pd.read_csv(CSV_PATH)

            new_row = pd.DataFrame([[name, mobile, seat_str, uid, txn_id, amount]],
                                   columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"])
            updated_df = pd.concat([booked_df, new_row], ignore_index=True)
            updated_df.to_csv(CSV_PATH, index=False)

            # Save to Google Sheet
            try:
                append_booking_to_gsheet(name, mobile, seat_str, uid, txn_id, amount)
            except Exception as e:
                st.error(f"❌ Failed to save to Google Sheet: {str(e)}")
                logging.error(f"Google Sheet error: {e}")

            # Generate ticket
            try:
                ticket_img = generate_ticket(name, seats, amount, uid, txn_id)
                buffer = io.BytesIO()
                ticket_img.save(buffer, format="PNG")
                buffer.seek(0)

                st.image(ticket_img, caption="🎫 Your Ticket — Show at Entry")
                st.download_button("📥 Download Ticket", buffer, file_name=f"ticket_{uid}.png", mime="image/png")
                st.success(f"✅ Booking Confirmed! Your UID is: `{uid}`")
                st.info("Please save this ticket or UID for entry verification.")
                st.session_state.clear()
            except Exception as e:
                st.error(f"❌ Failed to generate ticket: {str(e)}")
                logging.error(f"Ticket generation error: {e}")
        elif response.status_code == 401:
            st.error("❌ Authentication failed during payment verification. Please check your API credentials or contact support.")
            st.json(response.json())
            st.info("Ensure CASHFREE_APP_ID and CASHFREE_SECRET_KEY are valid test credentials.")
        else:
            st.error("❌ Payment not completed or failed. Please complete the payment or try again.")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Verification request failed with status: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Payment verification failed: {str(e)}")
        logging.error(f"Verification error: {e}")
else:
    logging.debug(f"Post-payment logic not triggered. Query params: {query_params}")
    # Fallback for missing query parameters
    if st.session_state.get("order_id"):
        st.warning("⚠️ Redirect query parameters missing. Please enter your Order ID to verify payment.")
        with st.form("order_id_fallback"):
            manual_order_id = st.text_input("Enter Cashfree Order ID (e.g., DAARUNAM_1b5c6535)")
            submit_order_id = st.form_submit_button("Verify Payment")
            if submit_order_id and manual_order_id:
                # Reconstruct query params manually
                query_params["payment"] = "success"
                query_params["oid"] = manual_order_id
                query_params["name"] = info.get("name", "Guest") if st.session_state.get("booking") else "Guest"
                query_params["mobile"] = info.get("mobile", "") if st.session_state.get("booking") else ""
                query_params["seats"] = ",".join(info.get("seats", [])) if st.session_state.get("booking") else ""
                query_params["amount"] = str(info.get("amount", 0)) if st.session_state.get("booking") else "0"
                query_params["cf_id"] = manual_order_id
                st.session_state.step = "payment"
                st.rerun()

# ---------------------------- FOOTER ----------------------------
st.divider()
st.markdown("<p style='text-align:center; color:#cccccc; font-size:14px;'>© 2025 DAARUNAM Movie | UPI Verification Required at Entry</p>", unsafe_allow_html=True)
