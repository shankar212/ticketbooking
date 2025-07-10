# 🎬 DAARUNAM Booking App

A fully functional **movie ticket booking system** built using **Streamlit**, integrated with **Google Sheets** for real-time booking data, and generates a **professional ticket image** with QR code for UID verification.

---

## 📸 Preview

![Ticket Screenshot](https://github.com/user-attachments/assets/0045c3d5-1df4-4cbb-b86b-460a931a6fd6)



---

## 🚀 Features

- 🎟️ Book multiple seats (up to 10)
- 📲 UPI payment support with manual Transaction ID
- 🧾 Generates downloadable ticket with:
  - Poster
  - Customer & transaction details
  - Unique UID
  - Scannable QR code
- ☁️ Booking data synced with **Google Sheets**
- 📊 Admin-safe: avoids double booking by checking real-time seat availability
- 🎨 Stunning animated UI using custom Streamlit CSS
- **Live at :** https://moviebookingonline.streamlit.app/
---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + HTML/CSS (embedded)
- **Backend**: Python
- **Storage**: Google Sheets API (via `gsheets.py`)
- **Image Generation**: Pillow (PIL), Qrcode
- **File**: CSV for local booking fallback

---

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
├── app.py                 # Main Streamlit app
├── gsheets.py            # Google Sheets helper functions
├── poster.jpg            # Movie poster used on tickets
├── booking_data.csv      # Local fallback for bookings
├── generated_upi_qr.png  # Static UPI QR code
├── README.md             # This file
└── requirements.txt
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
