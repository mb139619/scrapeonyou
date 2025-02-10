import streamlit as st
import pandas as pd
import io
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def queryConverter(query:str):

    "function that formats the query into a query usable for the ecosia search engine"
    
    query = ' '.join(query.split())
    search_query =  query.replace(" ", "%20")

    return search_query


def scrape_web_results(query:str, num_pages:int):
    
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    search_query = queryConverter(query)
    filter_string = "https://"

    i = 0

    while i < num_pages:

        driver = get_driver()
        driver.get(f'https://www.ecosia.org/search?method=index&q={search_query}&p={str(i)}')
        
        time.sleep(5)
        link_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-test-id="result-link"]')


        links_data = []
        for link in link_elements:
            title = link.text  
            href = link.get_attribute("href")
            if filter_string in title:
                pass
            else:
                links_data.append({"title": title, "href": href})

        temp_df = pd.DataFrame(links_data)
        
        if i == 0:

            results_df = temp_df

        else:

            results_df = pd.concat([results_df, temp_df], ignore_index=True)

        driver.quit()

        i += 1

    return results_df


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
        


    
