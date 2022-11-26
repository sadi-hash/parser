from bs4 import BeautifulSoup as BS
import requests
from datetime import datetime
import xlsxwriter



def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def get_posts_links(html):
    # Достает 10 ссылок с каждой страницы
    links = []
    soup = BS(html, "html.parser")
    container = soup.find("div", {"class": "container body-container"})
    main = container.find("div", {"class":"main-content"})
    listings = main.find("div", {"class": "listings-wrapper"})
    posts = listings.find_all("div", {"class":"listing"})
    for post in posts:
        header = post.find("div", {"class": "left-side"})
        link = header.find("a").get("href")
        full_link = "https://www.house.kg"+link
        links.append(full_link)
    return links

def get_post_data(html):
    soup = BS(html, "html.parser")
    main = soup.find("div", {"class":"main-content"})
    header = main.find("div",{"class":"details-header"})
    title = header.find("div",{"class":"left"}).find("h1").text.strip()
    address = header.find("div", {"class":"adress"}).text.strip()
    dollar = header.find("div", {"class":"price-dollar"}).text
    som = header.find("div", {"class":"price-som"}).text
    mobile = main.find("div", {"class":"phone-fixable-block"}).find("div",{"class":"number"}).text
    desc = main.find("div", {"class":"description"})
    desc = desc.text.strip() if desc else "Описание отсутствует"
    lon = main.find("div", {"id":"map2gis"}).get("data-lon") # долгота
    lat =  main.find("div", {"id": "map2gis"}).get("data-lat") # ширина
    infos = main.find("div",{"class":"details-main"}).find_all("div", {"class":"info-row"})
    add_info = {}
    for info in infos:
        key = info.find("div",{"class":"label"}).text.strip()
        value = info.find("div", {"class":"info"}).text.strip()
        add_info.update({key:value})
    data = {
        "title": title,
        "address": address,
        "dollar": dollar,
        "som":som,
        "mobile":mobile,
        "description":desc,
        "lon":lon,
        "lat":lat,
        # "add_info":add_info 
    }
    return data

def get_last_page(html):
    soup = BS(html, "html.parser")
    ul = soup.find("ul", {"class":"pagination"})
    li_list = ul.find_all("a", {"class":"page-link"})
    lp_number = li_list[-1].get("data-page")
    return int(lp_number)

def write_excel(data, row_number):
    workbook = xlsxwriter.Workbook("house_kg.xlsx",options={"in_memory":True})
    worksheet = workbook.add_worksheet()
    col = 0 # column
    for value in data.values():
        worksheet.write(row_number, col, value)
        col += 1 
    
    workbook.close()




def main():
    start = datetime.now()
    URL = "https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc"
    lp_number = get_last_page(get_html(URL))
    print(f"КОЛИЧЕСТВО СТРАНИЦ:{lp_number}")
    row_number = 0
    for i in range(1, 2):
        page_url = URL + f"&page={i}"
        print(page_url)
        html = get_html(page_url)
        links=get_posts_links(html)
        for link in links:
            detail_html = get_html(link)
            data=get_post_data(detail_html)
            write_excel(data=data,row_number=row_number)
            row_number += 1
    end = datetime.now()
    result = end - start
    print(f"Время выполнения программы: {result}")

if __name__ == "__main__":
    main()        






