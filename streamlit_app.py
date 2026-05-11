import streamlit as st
import pandas as pd
import math
from pathlib import Path
import datetime
import struct
import base64
import qrcode
from io import BytesIO
from fpdf import FPDF
from PIL import Image


favicon = Image.open(Path(__file__).parent / "assets" / "favicon.png")

st.set_page_config(
    page_title="Awizacje DPH / Delivery Notifications",
    page_icon=favicon,
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def encode_delivery_notification_base64(supplier, date, hour, pallets):
    supplier_bytes = supplier.encode("ascii", errors="ignore")[:40]
    supplier_bytes = supplier_bytes.ljust(40, b" ")

    epoch = datetime.date(1970, 1, 1)
    date_days = (date - epoch).days

    h, m = map(int, hour.split(":"))
    slot = ((h * 60 + m) - (8 * 60)) // 15

    pallets_val = 0 if pallets == 0 else pallets

    binary = struct.pack(
        ">40sIBH",
        supplier_bytes,
        date_days,
        slot,
        pallets_val
    )

    return base64.urlsafe_b64encode(binary).decode().rstrip("=")


def create_delivery_notification_pdf(
    supplier,
    selected_date,
    hour,
    pallets_display,
    payload_b64,
):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AWIZACJA DOSTAWY / DELIVERY NOTIFICATION", ln=True)

    pdf.ln(5)

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Supplier / Dostawca: {supplier}", ln=True)
    pdf.cell(0, 8, f"Delivery date / Data dostawy: {selected_date}", ln=True)
    pdf.cell(0, 8, f"Time slot / Przedział czasowy: {hour}", ln=True)
    pdf.cell(0, 8, f"Pallets / Palety: {pallets_display}", ln=True)

    pdf.ln(10)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "DPH Code / Kod DPH:", ln=True)

    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 6, payload_b64)

    pdf.ln(10)

    qr = qrcode.make(payload_b64)
    qr_buf = BytesIO()
    qr.save(qr_buf)
    qr_buf.seek(0)

    pdf.image(qr_buf, x=60, y=None, w=90)

    pdf_buf = BytesIO()
    pdf.output(pdf_buf)
    pdf_buf.seek(0)

    return pdf_buf


# -----------------------------------------------------------------------------
# Draw the actual page

'''
# Awizacje DPH / Delivery Notifications
'''

st.header("Stwórz awizację / Create delivery notification", divider="gray")

with st.form("delivery_notification_form"):

    supplier = st.text_input(
        "Wybierz dostawcę / Select supplier",
        max_chars=40
    )

    selected_date = st.date_input(
        "Wybierz datę dostawy / Select delivery date",
        value=datetime.date.today()
    )

    hour = st.selectbox(
        "Wybierz przedział czasowy / Select time slot",
        [
            "08:00", "08:15", "08:30", "08:45",
            "09:00", "09:15", "09:30", "09:45",
            "10:00", "10:15", "10:30", "10:45",
            "11:00", "11:15", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45",
            "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:15", "14:30", "14:45",
            "15:00", "15:15", "15:30", "15:45",
            "16:00", "16:15", "16:30", "16:45",
            "17:00", "17:15", "17:30", "17:45",
            "18:00", "18:15", "18:30", "18:45"
        ]
    )

    pallets = st.number_input(
        "Liczba palet / Number of pallets",
        min_value=0,
        max_value=999,
        step=1,
        placeholder="0 gdy nie dotyczy / 0 if not applicable"
    )

    submitted = st.form_submit_button("Potwierdź / Generate notification")


if submitted:
    supplier = supplier.strip().upper()

    if not supplier:
        st.error("Dostawca jest wymagany / Supplier is required")
        st.stop()

    pallets_display = "-" if pallets == 0 else pallets

    payload_b64 = encode_delivery_notification_base64(
        supplier,
        selected_date,
        hour,
        pallets
    )

    pdf_buf = create_delivery_notification_pdf(
        supplier,
        selected_date,
        hour,
        pallets_display,
        payload_b64,
    )

    st.success("Awizacja wygenerowana / Delivery notification generated")

    st.download_button(
        label="⬇️ Pobierz PDF / Download PDF",
        data=pdf_buf,
        file_name="awizacja_dostawy_delivery_notification.pdf",
        mime="application/pdf",
    )
