# gsheets.py
import gspread
import json
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

SHEET_NAME = "DaarunamBookings"

def get_worksheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["google"]
    creds_json = json.dumps(creds_dict)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json), scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet.sheet1

def get_booked_seats():
    worksheet = get_worksheet()
    records = worksheet.get_all_records()
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
