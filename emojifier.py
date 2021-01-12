import os
from downloader import Downloader
import pandas as pd
import logging
from fuzzywuzzy import fuzz, process
import csv
import re

# Sets logger up and configures it
logging.getLogger().setLevel(logging.INFO)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s || %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class Emojifier:

    def __init__(self):

        self.punctuation = r'!@#$%¨&*()_+-=[{]}~^,<.>;:/?\|'

        if not os.path.isfile('emojis.csv'):
            # emoji csv not present, must download
            logging.info('> emojis.csv file not found, downloading...')
            Downloader().download_emojis_csv()
            logging.info('> emojis.csv file downloaded!')

        df = pd.read_csv(
            filepath_or_buffer='emojis.csv', 
            engine='python', 
            encoding='utf-8'
        )

        self.emojis_dict = dict(
            zip(
                df['emoji_name'], df['emoji_symbol']
            )
        )

        self.input = pd.read_excel('input.xlsx')
        self.input = list(self.input['input'])

        #self.generate_outputs()
        for output in self.emojify(method='all'):
            print(output)

    def emojify(self, method='one'):

        emojified_inputs = []

        for row in self.input:

            new_text = ''
            raw_words = re.split(r'(\W)', row)
            words = [w for w in raw_words if w not in ['', ' ']]
            print(words)

            for w in words:

                emojis = ''
                w = w.strip()
                
                if w in self.punctuation:
                    new_text += '{} '.format(w)
                
                else:
                        
                    if len(w) > 3:
                            
                        if method == 'all':
                            matches = process.extract(w, self.emojis_dict.keys())
                            emojis = ''.join(
                                self.emojis_dict[m[0]].strip() for m in matches if m[1] >= 90
                            )

                        elif method == 'one':
                            emoji_name, ratio = process.extractOne(w, self.emojis_dict.keys())
                            emojis = self.emojis_dict[emoji_name] if ratio >= 90 else ''

                    emojis = emojis.strip()

                    if len(emojis) == 0:
                        new_text += '{} '.format(w)
                    else:
                        new_text += '{} {} '.format(w, emojis)

            emojified_inputs.append(new_text)

        return emojified_inputs

    def generate_outputs(self):

        for method in ['one', 'all']:

            emojified = self.emojify(method=method)
            for e in emojified:

                print('{}\n--------------------------------'.format(e))
            print('\n--------------------------------')