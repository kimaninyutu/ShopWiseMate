import requests
from bs4 import BeautifulSoup


def scrape_image_from_product_page(url):
    full_url = f"https://www.kilimall.co.ke/{url}"
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    image = soup.select_one('div.swipe-image img')['src']
    return image


scrape_image_from_product_page('listing/2517665-home-salevitron-32-inch-frameless-smart-tv-hd-netflix-tv-htc3200s'
                               '-youtube-television-dvbt2-android-11-ac-energy-saving-television-1g8g?skuId=18272411')
