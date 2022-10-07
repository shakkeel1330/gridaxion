from urllib import response
import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import zipfile


DOMAIN = "https://www.ercot.com"
req = requests.get("https://www.ercot.com/misapp/GetReports.do?reportTypeId=13091&reportTitle=Historical%20DAM%20Clearing%20Prices%20for%20Capacity&showHTMLView=&mimicKey")

soup = BeautifulSoup(req.content, "html.parser")

zip_list = soup.find_all('a')

file_link = zip_list[1].get('href')
file_name = "sample.zip"
url = DOMAIN + file_link

# print(url)

urllib.request.urlretrieve(url, file_name) ## Depreciation expected! Look for alternate options

with zipfile.ZipFile('sample.zip', 'r') as zip_ref:
    zip_ref.extractall('')