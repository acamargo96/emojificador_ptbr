from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import logging

logging.getLogger().setLevel(logging.INFO)

# Disable logging for chromedriver
options = Options()
options.add_argument('--disable-logging')
# Enter silent mode
options.headless = True
options.add_experimental_option("excludeSwitches", ["enable-logging"])

class Downloader:

    def __init__(self, verbose=True):
        self.verbose = verbose

    def download_emojis_csv(self):

        emoji_symbol = [] # emoji_font
        emoji_name = []   # emoji_name truncate
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.get('https://www.emojiall.com/pt/all-emojis')

        emojis = driver.find_elements_by_class_name('emoji_card')
        
        counter = 1
        total_count = len(emojis)

        for emoji in emojis:

            hrefs = emoji.find_elements_by_tag_name('a')

            for a in hrefs:
                
                a_class = a.get_attribute('class')
                if a_class == 'emoji_font':
                    emoji_symbol.append(a.text)
                elif a_class == 'emoji_name truncate':
                    emoji_name.append(a.text)

            if self.verbose:
                logging.info('\t> Done with emoji {} ({} of {})'.format(
                    emoji_symbol[counter - 1],
                    counter,
                    total_count
                    )
                )
            
            counter += 1

        pd.DataFrame(data={
            'emoji_symbol' : emoji_symbol,
            'emoji_name'   : emoji_name
        }).to_csv('emojis.csv', index=False)