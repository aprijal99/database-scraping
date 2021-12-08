from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import numpy as np
import pandas as pd

driver = webdriver.Firefox()

compounds_list = pd.read_csv('List of Compounds.csv')
species_link = compounds_list.loc[:, 'Species Link']

species = []

for link in species_link:
    driver.get('http://herbaldb.farmasi.ui.ac.id/v3/'+link)

    try:
        parent = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "acc"))
        )
    except:
        driver.quit()

    species_rows = parent.find_elements(By.CSS_SELECTOR, ' li:nth-of-type(1) .acc-content table tbody tr:nth-of-type(n+2) td:nth-child(2)')

    tmp = []
    for row in species_rows:
        tmp.append(re.search("[A-Za-z]+.[A-Za-z]+.[A-Za-z]*", row.text)[0])

    species.append(', '.join(tmp))

driver.quit()

species_df = pd.DataFrame(data=np.array(species).T, columns=['Species'])
compounds_with_species = pd.concat([compounds_list, species_df], axis=1)

compounds_with_species.to_csv('List of Compounds + Species.csv')