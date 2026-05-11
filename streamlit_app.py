import streamlit as st
import pandas as pd
import math
from pathlib import Path
import datetime

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Awizacje DPH',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

'''
# Awizacje Delpharm
'''

st.header("Stwórz awizacje/Create avization", divider="gray")

with st.form("awization_form"):
    selected_date = st.date_input(
        "Wybierz Date/Select date",
        value=datetime.date.today()
    )
    
    supplier = st.text_input(
        "Wybierz dostawcę/Select supplier",
    )

    hour = st.selectbox(
        "Wybierz godzinę/Select hour",
        ["08:00", "12:00", "16:00"]
    )

    submitted = st.form_submit_button("Potwierdź/Submit")

if submitted:
    supplier = supplier.strip().upper()
    
    st.success("Submitted successfully!")
    st.write("Data/Date:", selected_date)
    st.write("Dostawca/Supplier:", supplier)
    st.write("Godzina/Hour:", hour)
