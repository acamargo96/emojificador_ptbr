# emojificador_ptbr
Usa fuzzy matching para emojificar textos lidos de um arquivo .xlsx.

- downloader.py: módulo de webscraping para baixar emojis e seus títulos.
- emojifier.py: contém a classe Emojifier, que lê um arquivo .xlsx com inputs e os emojifica.

Dependências:

- pandas
- fuzzywuzzy, python-Levenshtein
- selenium
- webdriver_manager
