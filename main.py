import requests
from bs4 import BeautifulSoup
import csv

CSV = "hotels.csv"
URL = "https://www.booking.com/searchresults.ru.html?label=operasoft-sdO15-343337&sid=70b987efb9cd96dd7fe98264da7f9f9b&aid=343337&sb_lp=1&src=index&error_url=https%3A%2F%2Fwww.booking.com%2Findex.ru.html%3Faid%3D343337%3Blabel%3Doperasoft-sdO15-343337%3Bsid%3D70b987efb9cd96dd7fe98264da7f9f9b%3Bsb_price_type%3Dtotal%26%3B&ss=Казань%2C+Россия&is_ski_area=&checkin_year=2022&checkin_month=2&checkin_monthday=3&checkout_year=2022&checkout_month=2&checkout_monthday=4&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&dest_id=-2923066&dest_type=city&search_pageview_id=829757124763012e&search_selected=true&nflt=class%3D4%3Bht_id%3D204"
HEADERS = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.45"
}
def get_html(url, params=""):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="_fe1927d9e _0811a1b54 _a8a1be610 _022ee35ec b9c27d6646 fb3c4512b4 fc21746a73")
    hotels = []

    for item in items:
        hotels.append(
            {
                "title":item.find("div", class_="fde444d7ef _c445487e2").get_text(strip=True),
                "link":item.find("div", class_="_12369ea61").find("a").get("href"),
                "price":item.find("span", class_="fde444d7ef _e885fdc12").get_text(strip=True)
            }
        )
    return hotels

def save_doc(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(['Отели','Ссылка на отель', "Стоимость за 2 взрослых, ночь"])
        for item in items:
            writer.writerow([item['title'], item['link'], item["price"]])

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        hotels = []
        html = get_html(URL)
        hotels.extend(get_content(html.text))
        save_doc(hotels, CSV)
    else:
        print("error")
parser()