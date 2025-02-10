import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def queryConverter(query:str):

    "function that formats the query into a query usable for the ecosia search engine"
    
    query = ' '.join(query.split())
    search_query =  query.replace(" ", "%20")

    return search_query


def scrape_web_results(query:str, num_pages:int):
    
    

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode

    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    search_query = queryConverter(query)
    filter_string = "https://"

    i = 0

    while i < num_pages:

        driver = webdriver.Chrome(options=chrome_options)
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
