from datetime import date
import requests
from bs4 import BeautifulSoup
import csv


def add_flat(url, location, price, floor, room, sqr):
    today = date.today()
    with open("flats_%s.csv" % today, 'a') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([url, location, price, floor, room, sqr])


text = {}
index_from = int(input())
index_to = int(input())
# 2593 (28.09.20)
for x in range(index_from, index_to):
    http = f'http://crm-realbest.realtsoft.net/estate-{x}.html'
    response = requests.get(http)
    if response.status_code == 200:
        html_data = BeautifulSoup(response.text, "html.parser")
        header = html_data.h3.get_text()
        price = html_data.find(class_='pdf-header-contacts').strong.get_text()
        rooms = html_data.find('img', attrs={'title': 'Кол. комнат'})
        sqr = html_data.find('img', attrs={'title': 'Площадь'})

        if rooms:
            flat_room = rooms.parent.get_text().strip()
        else:
            flat_room = 0

        floor = html_data.find('img', attrs={'title': 'Этаж'})

        if floor:
            flat_floor = floor.parent.get_text().strip()
        else:
            flat_floor = ''

        floor_description = 'Этаж: ' + flat_floor
        if sqr:
            flat_sqr = sqr.parent.get_text().strip()
        else:
            flat_sqr = ''

        # Filtering output
        if "Центр" in header or "Галицький" in header:
            add_flat(http, header, price, floor_description, flat_room, flat_sqr)
