from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import re

driver = webdriver.Firefox()
driver.get('http://herbaldb.farmasi.ui.ac.id/v3/index.php?v=kontensenyawa')

page_num = driver.find_element(By.CSS_SELECTOR, 'table tbody tr td:last-child div:nth-of-type(2) div center > b')
page_num = int(page_num.text)

compound_name = []
id_knapsack = []
species_link = []

for i in range(page_num):
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'next'))
        )

        compound_table = driver.find_element(By.CSS_SELECTOR, 'table tbody tr td:last-child table:nth-of-type(2) tbody')
        compound_rows = compound_table.find_elements(By.CSS_SELECTOR, 'tr:nth-of-type(n+2)')

        for row in compound_rows:
            if(row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text != ''):
                compound_name.append(row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text)
                id_knapsack.append(row.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text)
                species_link.append(re.search("popdetails_content.php\?con_id=\d+", row.find_element(By.CSS_SELECTOR, 'td:nth-child(2) a').get_attribute('onclick'))[0])

        next_btn.click()
    except:
        driver.quit()

driver.quit()

compound_df = pd.DataFrame(data=np.array([compound_name,id_knapsack,species_link]).T, columns=['Compound Name', 'ID Knapsack', 'Species Link'])
compound_df.to_csv('List of Compounds 3.csv')