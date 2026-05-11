import streamlit as st
import pandas as pd
import math
from pathlib import Path
import datetime
import struct
import base64
import qrcode
from io import BytesIO


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Awizacje DPH',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def encode_awization_base64(supplier, date, hour, pallets):
    supplier_bytes = supplier.encode("ascii", errors="ignore")[:40]
    supplier_bytes = supplier_bytes.ljust(40, b" ")
    
    epoch = datetime.date(1970, 1, 1)
    date_days = (date - epoch).days

    h, m = map(int, hour.split(":"))
    slot = ((h * 60 + m) - (8 * 60)) // 15  # 0–43

    pallets_val = 0 if pallets == 0 else pallets

    binary = struct.pack(
        ">40sIbb",
        supplier_bytes,
        date_days,
        slot,
        pallets_val
    )
    # Encode to Base64 
    return base64.urlsafe_b64encode(binary).decode().rstrip("=")
# -----------------------------------------------------------------------------
# Draw the actual page

'''
# Awizacje DPH
'''

st.header("Stwórz awizacje/Create avization", divider="gray")

with st.form("awization_form"):
    
    supplier = st.text_input(
        "Wybierz dostawcę/Select supplier",
            max_chars=40
    )
    
    selected_date = st.date_input(
        "Wybierz Date/Select date",
        value=datetime.date.today()
    )

    hour = st.selectbox(
        "Wybierz godzinę/Select hour",
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
        "Liczba palet/Number of pallets", 
        min_value=0,
        max_value=999,
        step=1,
        placeholder="0 gdy nie dotyczy/0 if not applicable"
    )


    submitted = st.form_submit_button("Potwierdź/Submit")

if submitted:
    supplier = supplier.strip().upper()

    if not supplier:
            st.error("Dostawca / Supplier is required")
            st.stop()

    display_pallets = "-" if pallets == 0 else pallets
    
    payload_b64 = encode_awization_base64(
            supplier,
            selected_date,
            hour,
            pallets
        )

    st.success("Submitted successfully!")
    st.write("Data/Date: ", selected_date)
    st.write("Dostawca/Supplier: ", supplier)
    st.write("Godzina/Hour: ", hour)
    st.write("Palety/Pallets: ", display_pallets)

    
    st.subheader("Kod Base64")
    st.code(payload_b64, language="text")

    # Generate QR
    qr = qrcode.make(payload_b64)
    buf = BytesIO()
    qr.save(buf)

    st.subheader("QR Code")
    st.image(buf, caption="Zeskanuj kod QR / Scan QR")

