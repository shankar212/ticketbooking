# 🎬 DAARUNAM Booking App

A fully functional **movie ticket booking system** built using **Streamlit**, integrated with **Cashfree Payments** and **Google Sheets** for real-time booking data. Generates a **professional ticket image** with QR code for UID verification and entry.
---

## 📸 Preview

![Ticket Screenshot](https://github.com/user-attachments/assets/0045c3d5-1df4-4cbb-b86b-460a931a6fd6)



---

## 🚀 Features

- 🎟️ Book multiple seats (up to 10)
- 💳 **Integrated Cashfree Hosted Checkout Payment Gateway**
  - Secure hosted payments via UPI, Card, NetBanking, Wallets
  - Auto-verification post-payment and redirect to ticket
- 📲 Manual UPI payment support (for fallback mode)
- 🧾 Generates downloadable ticket with:
  - Poster
  - Customer & transaction details
  - Unique UID
  - Scannable QR code
- ☁️ Booking data synced with **Google Sheets**
- 🔐 Prevents double booking with real-time seat availability check
- 🎨 Stunning animated UI using custom Streamlit CSS
- 🌐 **Live at:** [moviebookingonline.streamlit.app](https://moviebookingonline.streamlit.app)
---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + HTML/CSS
- **Backend**: Python
- **Payments**: Cashfree PG Orders API (Hosted Checkout)
- **Storage**: Google Sheets (via `gsheets.py`)
- **Image Generation**: Pillow (PIL), Qrcode
- **File-based Storage**: CSV fallback

---
## 💳 Cashfree Integration

This app uses the [Cashfree Payment Gateway](https://www.cashfree.com/) (PG Orders API with Hosted Checkout) for secure payment processing.

### ✅ Features:
- Secure, PCI-compliant hosted payment page
- Payment verification using `/pg/app/orders/{order_id}` endpoint
- Seamless redirect back to app on success

> **Note:** You'll need your own **production API keys** from Cashfree and must be KYC-verified to 

## 🧰 Requirements

- Python 3.9+
- Dependencies:

```bash
pip install streamlit pandas pillow qrcode gspread oauth2client
```

---

## 📂 Project Structure

```
📁 DAARUNAM-Booking/
├── app.py                     # Main Streamlit app
├── gsheets.py                # Google Sheets helper functions
├── poster.jpg                # Movie poster used on tickets
├── booking_data.csv          # Local fallback for bookings
├── generated_upi_qr.png      # Static UPI QR code
├── requirements.txt
├── term_and_refund_policy.md # T&C and refund info
├── contactus.md              # Contact us info
└── README.md                 # This file
```

---

## 🔧 Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/daarunam-booking.git
cd daarunam-booking
```

### 2. Set up Google Sheets credentials

- Create a Google Cloud project and enable the Google Sheets API
- Download `credentials.json` and place it in the root directory
- In `gsheets.py`, update:
  - Sheet name
  - Worksheet name

### 3. Run the app

```bash
streamlit run app.py
```

---

## 🎟 Ticket Sample

> Generated ticket includes:

- 🎬 Poster image  
- 👤 User name, 📞 Mobile number  
- 🎟 Seats, ₹ Amount  
- 🔐 Unique UID  
- 📄 Transaction ID  
- 📅 Date and 🏛️ Venue  
- 🧾 Scannable QR code for UID verification  

---

## 📸 Screenshots

| Booking Page | Ticket Output |
|--------------|---------------|
| ![](https://github.com/user-attachments/assets/6516e9e6-d148-4f4b-b35b-ec36a9e0ba4c) | ![](https://github.com/user-attachments/assets/f54b45d5-e0ed-4d6a-9ab4-0068680f331a) |

##Gsheet Screenshot
<img width="684" height="441" alt="image" src="https://github.com/user-attachments/assets/94555f76-644a-4282-ae80-deed3816d978" />

---

## 🤝 Contribution

Pull requests and feedback are welcome! To contribute:

```bash
git checkout -b feature/my-feature
git commit -m "Add my feature"
git push origin feature/my-feature
```

---

## 📜 License

This project is licensed under the MIT License.

---

## 🧑‍💻 Author

**Rathod Shanker**  
📧 rs23mcf1r34@student.nitw.ac.in  
📞 +91-7780772877

---
