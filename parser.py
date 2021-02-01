from datetime import date
import requests
from bs4 import BeautifulSoup
import csv
import threading

# 2593 (28.09.20)
# 3120 (29.01.21)
def add_flat(url, location, price, floor, room, sqr):
    today = date.today()
    with open("flats_%s.csv" % today, 'a') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([url, location, price, floor, room, sqr])

def load_flats(index_from, index_to):
    for x in range(index_from, index_to):
        print(index_from)
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
                print('here')
                add_flat(http, header, price, floor_description, flat_room, flat_sqr)

try:
    t1 = threading.Thread(target=load_flats, args=(2593, 2693))
    t2 = threading.Thread(target=load_flats, args=(2694, 2793))
    t3 = threading.Thread(target=load_flats, args=(2794, 3120))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
except:
    print ("Error: unable to start thread")
