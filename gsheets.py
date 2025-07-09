# gsheets.py
import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "DaarunamBookings"

def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = dict(st.secrets["google"])  # Convert AttrDict to plain dict
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet.sheet1

def get_booked_seats():
    worksheet = get_worksheet()
    try:
        records = worksheet.get_all_records()
    except Exception as e:
        st.error("❌ Failed to load booked seats from Google Sheet.")
        st.exception(e)
        return set()

    booked = set()
    for row in records:
        seats = str(row.get("Seat Nos", ""))
        for seat in seats.split(","):
            seat_clean = seat.strip()
            if seat_clean:
                booked.add(seat_clean)
    return booked



def append_booking_to_gsheet(name, mobile, seat_str, uid, txn_id, amount):
    worksheet = get_worksheet()
    worksheet.append_row([name, mobile, seat_str, uid, txn_id, amount])
