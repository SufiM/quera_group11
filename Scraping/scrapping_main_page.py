from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import ElementNotSelectableException
import time
import json
import pandas as pd
import os

driver = webdriver.Chrome()
try:
    driver.get("https://coinmarketcap.com/historical/20230825/")
except NoSuchDriverException as err:
    print("error occurred: {}".format(err))
time.sleep(1)
pos = 500
for i in range(0, 20):
    driver.execute_script("window.scrollTo(0, " + str(pos) + ")")
    pos += 500
    time.sleep(1)

rows = driver.find_elements(By.CSS_SELECTOR, ".cmc-table-row")
coins = []
for row in rows:
    try:
        coin = {}
        coin["rank"] = row.find_element(
            By.CSS_SELECTOR, ".cmc-table__cell--sort-by__rank div"
        ).text
        element = row.find_element(By.CSS_SELECTOR, ".cmc-table__column-name--name")
        coin["name"] = element.get_attribute("title")
        coin["symbol"] = row.find_element(
            By.CSS_SELECTOR, ".cmc-table__column-name--symbol"
        ).get_attribute("textContent")
        coin["circulating_supply"] = int(
            "".join(
                filter(
                    str.isdigit,
                    row.find_element(
                        By.CSS_SELECTOR,
                        ".cmc-table__cell--sort-by__circulating-supply div",
                    ).text,
                )
            )
        )
        coin["main_link"] = element.get_attribute("href")
        coin["historical_link"] = coin["main_link"] + "historical-data/"
        coins.append(coin)
    except NoSuchElementException as element_err:
        print("error occurred: {}".format(element_err))
    except NoSuchAttributeException as attribute_err:
        print("error occurred: {}".format(attribute_err))
    except ElementNotSelectableException as select_err:
        print("error occurred: {}".format(select_err))

driver.quit()


folder_name = "Scraped_data"
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
folder_path = os.path.join(parent_directory, folder_name)

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

with open(f"{folder_path}/coins_data.json", "w") as file:
    json.dump(coins, file)

df = pd.read_json(f"{folder_path}/coins_data.json")
df.to_csv(f"{folder_path}/coins_data.csv", index=False)
print(df.head())
