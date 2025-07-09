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
# ---------------------------- SETTINGS ----------------------------
UPI_ID = "9154317035@ibl"
PAYEE_NAME = "DAARUNAM"
AMOUNT_PER_SEAT = 50
CSV_PATH = "booking_data.csv"
QR_PATH = "generated_upi_qr.png"
POSTER_PATH = "poster.jpg"  # Replace with your real poster file

# ---------------------------- INITIALIZATION ----------------------------
st.set_page_config(page_title="DAARUNAM Booking", layout="wide", page_icon="🎬")

# Initialize local CSV (only if not using for availability anymore)
if not os.path.exists(CSV_PATH):
    pd.DataFrame(columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"]).to_csv(CSV_PATH, index=False)

# ✅ Get already booked seats from Google Sheet instead of CSV
try:
    booked_seats = get_booked_seats()
except Exception as e:
    st.error("❌ Failed to load booked seats from Google Sheet.")
    st.exception(e)
    booked_seats = set()

# ✅ Ensure QR exists
if not os.path.exists(QR_PATH):
    qr_img = qrcode.make(f"upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am=50&cu=INR")
    qr_img.save(QR_PATH)

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

# ---------------------------- STEP 2: PAYMENT ----------------------------




# ✅ Correctly defined outside of if-block and at top-level indentation
def generate_ticket(name, seats, amount, uid, txn_id):
    width, height = 1000, 450
    ticket = Image.new("RGB", (width, height), "#1a1a1a")
    draw = ImageDraw.Draw(ticket)

    # Load fonts
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 100)
        font_label = ImageFont.truetype("arial.ttf", 60)
        font_value = ImageFont.truetype("arialbd.ttf", 55)
        font_small = ImageFont.truetype("arial.ttf", 55)
    except:
        font_title = ImageFont.load_default()
        font_label = font_value = font_small = ImageFont.load_default()

    # Header bar
    header_height = 90
    draw.rectangle([0, 0, width, header_height], fill="#ffcc00")
    draw.text((80, 30), "🎬 DAARUNAM MOVIE TICKET", font=font_title, fill="#000000")

    # Poster image (if available)
    if os.path.exists("poster.jpg"):
        poster = Image.open("poster.jpg").resize((180, 250))
        ticket.paste(poster, (20, header_height + 30))

    # Ticket info box
    info_x = 220
    info_y = header_height + 30
    spacing = 42

    info_items = [
        ("👤 Name:", name),
        ("🎟️ Seats:", ", ".join(seats)),
        ("💰 Amount:", f"₹{amount}"),
        ("🔐 UID:", uid),
        ("📄 Txn ID:", txn_id),
        ("🏦 Paid To:", "9154317035@ibl"),
        ("🗓️ Date:", datetime.now().strftime("%d %B %Y")),
        ("📍 Venue:", "TTD Kalyana Mandapam"),
    ]

    for i, (label, value) in enumerate(info_items):
        y = info_y + i * spacing
        draw.text((info_x, y), label, font=font_label, fill="#bbbbbb")
        draw.text((info_x + 160, y), value, font=font_value, fill="#ffffff")

    # QR Code
    qr = qrcode.make(uid)
    qr = qr.resize((110, 110))
    qr_x = width - 140
    qr_y = height - 160
    ticket.paste(qr, (qr_x, qr_y))

    draw.text((qr_x, qr_y + 120), "Scan for UID", font=font_small, fill="#cccccc")

    # Perforated edge circles
    for y in range(90, height - 30, 14):
        draw.ellipse((5, y - 3, 13, y + 5), fill="#555555")
        draw.ellipse((width - 13, y - 3, width - 5, y + 5), fill="#555555")

    return ticket
# ======================= STEP 2: PAYMENT ===========================
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

    st.image(QR_PATH, caption=f"Scan & Pay to {UPI_ID}", width=300)
    st.markdown(f"<a href='upi://pay?pa={UPI_ID}&pn={PAYEE_NAME}&am={info['amount']}&cu=INR' style='color:#ffcc00; text-decoration:none; font-weight:bold;'>🔗 Pay via UPI App</a>", unsafe_allow_html=True)

    txn_id = st.text_input("Enter UPI Transaction ID after payment", placeholder="Enter your UPI transaction ID")
    confirm = st.button("Generate My Ticket")

    if confirm:
        if not txn_id.strip():
            st.error("Please enter your UPI Transaction ID.")
        else:
            uid = f"DRN{random.randint(100, 999)}"
            name = info['name']
            mobile = info['mobile']
            seat_str = ", ".join(info['seats'])

            # ✅ Safely reload CSV here to avoid NameError
            if not os.path.exists(CSV_PATH):
                booked_df = pd.DataFrame(columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"])
            else:
                booked_df = pd.read_csv(CSV_PATH)

            # Save to CSV
            new_row = pd.DataFrame([[name, mobile, seat_str, uid, txn_id.strip(), info['amount']]],
                                   columns=["Name", "Mobile", "Seat Nos", "UID", "Transaction ID", "Amount"])
            updated_df = pd.concat([booked_df, new_row], ignore_index=True)
            updated_df.to_csv(CSV_PATH, index=False)

            # Save to Google Sheet
            append_booking_to_gsheet(name, mobile, seat_str, uid, txn_id.strip(), info['amount'])

            # Generate Ticket
            ticket_img = generate_ticket(name, info['seats'], info['amount'], uid, txn_id)

            buffer = io.BytesIO()
            ticket_img.save(buffer, format="PNG")
            buffer.seek(0)

            st.image(ticket_img, caption="🎫 Your Ticket — Show at Entry")
            st.download_button("📥 Download Ticket", buffer, file_name=f"ticket_{uid}.png", mime="image/png")

            st.success(f"✅ Booking Confirmed! Your UID is: `{uid}`")
            st.info("Please save this ticket or UID for entry verification.")
            st.session_state.clear()

    st.markdown("</div>", unsafe_allow_html=True)



# ---------------------------- FOOTER ----------------------------
st.divider()
st.markdown("<p style='text-align:center; color:#cccccc; font-size:14px;'>© 2025 DAARUNAM Movie | UPI Verification Required at Entry</p>", unsafe_allow_html=True)
