# Require pandas, numpy, matplotlib, lxml, html5lib, and BeautifulSoup4 packages
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import sys
import matplotlib.pyplot as plt

url = input("Enter the url here: ")
htmlContent = requests.get(url).content

# Use bs4 to get wiki article's title
soup = BeautifulSoup(htmlContent, "lxml")
try:
    heading = soup.find(id="firstHeading").text
except:
    heading = "Placeholder title"

try:
    # get tables using pandas
    tables = pd.read_html(htmlContent)
except ValueError:
    sys.exit("No tables found in this page")

for table in tables:
    # find numeric cols in tables
    numericCols = table.select_dtypes(include=np.number)
    column_headings = numericCols.columns.tolist()

    for colHeading in column_headings:
        # add 1 to index to let index starts from 1
        table.index = np.arange(1, len(table) + 1)
        plt.plot(table.index, table[colHeading], label=colHeading)
        plt.xlabel("index")
        plt.ylabel(colHeading)
        plt.legend()
        plt.title(heading)

        fileName = colHeading + ".pdf"
        plt.figure.savefig("outputs/" + fileName)
        plt.clf()
