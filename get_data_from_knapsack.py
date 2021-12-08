from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import re

driver = webdriver.Firefox()

compounds_data = pd.read_csv('List of Compounds + Species 2.csv')
id_knapsack = compounds_data.loc[:, 'ID Knapsack']

compound_name = []
formula = []
mw = []
InChlKey = []
InChlCode = []
Smiles = []

for id in id_knapsack:
    driver.get('http://www.knapsackfamily.com/knapsack_core/information.php?word='+id)

    try:
        parent = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table[class=\"d3\"] tbody'))
        )
    except:
        compound_name.append('')
        formula.append('')
        mw.append('')
        InChlKey.append('')
        InChlCode.append('')
        Smiles.append('')
        continue

    data = parent.find_elements(By.CSS_SELECTOR, 'tr:nth-child(-n+8)')

    compound_name_raw = data[0].find_element(By.CSS_SELECTOR, ' td')
    compound_name.append(', '.join(compound_name_raw.text.split('\n')))

    formula_raw = data[1].find_element(By.CSS_SELECTOR, 'td')
    formula.append(formula_raw.text)

    mw_raw = data[2].find_element(By.CSS_SELECTOR, 'td')
    mw.append(mw_raw.text)

    InChlKey_raw = data[5].find_element(By.CSS_SELECTOR, 'td')
    InChlKey.append(InChlKey_raw.text)

    InChlCode_raw = data[6].find_element(By.CSS_SELECTOR, 'td')
    InChlCode.append(InChlCode_raw.text)

    Smiles_raw = data[7].find_element(By.CSS_SELECTOR, 'td')
    Smiles.append(Smiles_raw.text)

driver.quit()

knapsack_df = pd.DataFrame(data=np.array([compound_name, formula, mw, InChlKey, InChlCode, Smiles]).T, columns=['Knapsack Compound Name', 'Formula', 'Molecular Weight', 'InChlKey', 'InChlCode', 'SMILES'])
knapsack_df.to_csv('knapsack.csv')

compounds_data_plus = pd.concat([compounds_data, knapsack_df], axis=1)
compounds_data_plus.to_csv('Compounds from HerbalDB and Knapsack.csv')