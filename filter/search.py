import csv
from pathlib import Path
from bs4 import BeautifulSoup
import requests

DIR = "./data/data1"
TUBE_URL = "https://www.youtube.com/watch?v="

DIR = Path(DIR)

result = []

with open(DIR/"data.csv", mode="r", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        hash = row[0]
        r = requests.get(TUBE_URL+hash)
        soup = BeautifulSoup(r.text, features="html.parser")
        row.append(soup.title.string)
        result.append(row)

with open(DIR/"temp.csv", mode="w", newline='', encoding='UTF8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in result:
        writer.writerow(row)
