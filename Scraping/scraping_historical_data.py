import os
import time
import logging
import glob
import pandas as pd
from tqdm import tqdm
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException


def get_driver(url, logger):
    try:
        # Make download_directory
        folder_name = "Scraped_data"
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        download_directory = os.path.join(parent_directory, folder_name)
        if not os.path.exists(download_directory):
            os.mkdir(download_directory)

        # Set download_directory to options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })

        # Create driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        return driver
    except NoSuchDriverException as err:
        logger.error("No Such Driver occurred: {}".format(err))
    return None


def extract_data(driver, url):
    try:
        # Find and click on date button
        date_button = driver.find_elements(By.CSS_SELECTOR, '.htGqtu button.dalfmx')[0]
        date_button.click()
        time.sleep(1)

        # Find and click on 'Last 365 days' button
        li_element = driver.find_element(By.CSS_SELECTOR, '.heoICr li:last-child')
        driver.execute_script("arguments[0].click();", li_element)
        time.sleep(1)

        # Find and click on 'Continue' button
        continue_button = driver.find_element(By.CSS_SELECTOR, '.bcCCXI')
        driver.execute_script("arguments[0].click();", continue_button)
        time.sleep(5)

        # Find and click on 'Download CSV' button
        download_csv_button = driver.find_elements(By.CSS_SELECTOR, '.htGqtu button.dalfmx')[1]
        download_csv_button.click()
        time.sleep(3)

    except NoSuchElementException as err:
        logger.error("No Such Element occurred: {}".format(err))
    except ElementClickInterceptedException as err:
        logger.error("Element Click Intercepted occurred: {}".format(err))


if __name__ == "__main__":

    # Set up logging configuration
    logging.basicConfig(filename='get_coins_csv_files.log', filemode='w', format='%(asctime)s %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Read urls
    df = pd.read_csv('../Scraped_data/coins_data.csv')
    urls = df['historical_link'].tolist()
    # urls = urls[0:10]

    for url_num in tqdm(range(len(urls))):
        url = urls[url_num]
        driver = get_driver(url, logger)

        if driver != None:
            try:
                extract_data(driver, url)
            except:
                logger.warning('Failed to extract data from the page [{}]'.format(url))

        # Sleep for a random time to avoid being blocked
        time_milliseconds = randint(500, 2000)
        time_sec = 0.001 * time_milliseconds
        logger.info('Sleeping for {} seconds'.format(time_sec))
        time.sleep(time_sec)
        logger.info('Woke up')

    

    currency_data = pd.read_csv("coins_data.csv")
    csv_files = glob.glob(os.path.join("history/", '*.csv'))
    dfs = []

    for file in csv_files:
        # Extract the currency name from the file name
        currency_name = os.path.splitext(os.path.basename(file))[0].split('_')[0]
        
        df = pd.read_csv(file, sep=';')
        currency_id = currency_data.loc[currency_data['name'] == currency_name, 'rank'].values[0]
        df['id'] = currency_id
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv('all_historical_data.csv', index=False)