import requests
import json
import os

COMPANY_DATA_URL = 'http://data.companieshouse.gov.uk/doc/company/'
FORMAT = '.json'
TEST_COMPANY_NUMBER = 12586212

r = requests.get(COMPANY_DATA_URL + str(TEST_COMPANY_NUMBER) + FORMAT)

print(r.text)