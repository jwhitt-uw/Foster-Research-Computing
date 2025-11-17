# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:45:24 2023

@author: jwhitt
""" 

import os
import re
import io
from requests import get
from bs4 import BeautifulSoup, UnicodeDammit
from time import sleep

#If your list of CIKs doesn't include the leading zeros this will add them in
def cik_zeros(cik_list) -> list:
    ciks = []
    for c in cik_list:
        n_zeros = 10 - len(c)
        new_cik = '0' * n_zeros + c
        ciks.append(new_cik)
    return ciks

# Create folder if it doesn't exist
def make_folder(folder_name: str):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

# Write the filing text to a file within the folder
def write_filing_text(text, file_name, folder_name):
    folder_path = folder_name
    if os.path.isdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with io.open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
    else:
        print(f'Folder Not Found: {folder_path}')

# Locate the filing on EDGAR, fetch the text
def get_filing(path: str):
    base_url = 'https://www.sec.gov'
    #Put your own email for User-Agent
    headers = {
        'User-Agent': '',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.sec.gov'
    }
    try:
        with get(base_url + '/Archives/' + path, headers=headers) as r:
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'lxml')
            link_tag = soup.find('table').find_all('a')[0]
            link = link_tag.get('href')
    except Exception as e:
        print(f"Error fetching filing page: {e}")
        return ""

    # Clean link if it contains '/ix?doc='
    if re.search(r'\/ix\?doc=', link):
        link = re.sub(r'\/ix\?doc=', '', link)

    sleep(0.2)
    try:
        with get(base_url + link, headers=headers) as f:
            f.raise_for_status()
            filing_soup = BeautifulSoup(f.content, 'lxml')
            ix_tag = filing_soup.find('div', style='display:none')
            if ix_tag is not None:
                ix_tag.decompose()
            filing_text = UnicodeDammit(filing_soup.text, ['latin-1', 'windows-1252']).unicode_markup
        return filing_text
    except Exception as e:
        print(f"Error fetching filing content: {e}")
        return ""

# Download and save filing text based on row info
def download(row):
    path = row.iname
    folder_name = str(row.cik)
    file_name = f"{row.cik}_{row.fdate}_{row.form}.html"
    make_folder(folder_name)
    text = get_filing(path)
    if text:
        write_filing_text(text, file_name, folder_name)