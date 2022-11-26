# import requests
# from bs4 import BeautifulSoup as BS



# file = open("test.html", encoding="utf-8")

# html = file.read()

# soup = BS(html, "html.parser")
# menu_list = soup.find("div", {"class":"container"}).find("div", {"class":"navigation-container"})
# ul = menu_list.find("ul",{"class":"menu"})
# li_list = ul.find_all("li")

# # for li in li_list:
# #     print(li.text) 


# # content = soup.find("div",{"class":"container"}).find("div",{"class":"content container"})
# # post_list = content.find_all("div",{"class":"post"})
# # for post in post_list:
# #     print(post.find("h1",{"class":"title"}))
# #     print(title.text.strip)


# footer = soup.find("div",{"class":"footer"})
# box = footer.find_all("div",{"class":"box"})
# for content in box:
#     p=content.find("p",{"class":"description"})
#     print(p.text)




