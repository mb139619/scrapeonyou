import streamlit as st
from functions import queryConverter, scrape_web_results
import pandas as pd
import io

buffer = io.BytesIO()

st.write("How about scraping the web for gettting some new leads?")

query = st.text_input("What are you looking for?")
num_pages = st.slider("How many pages you wanna scrape?", 1, 10, 1)

if st.button("Run!"):
    with st.spinner("Be patient, i'm fetching data from the web for you to work less.."):
        results = scrape_web_results(query, num_pages)

        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            results.to_excel(writer, sheet_name='Sheet1')
        
        st.download_button(
                    label="Download your data",
                    data=buffer,
                    file_name="results.xlsx",
                    mime="application/vnd.ms-excel")
        


    