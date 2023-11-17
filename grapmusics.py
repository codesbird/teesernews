from bs4 import BeautifulSoup
import requests

response  = requests.get(url='https://wynk.in/music/playlist/trending-now/bb_1591697081280?ref=sub_header')
print(response.content)

soup = BeautifulSoup(response.content,"html.parser")
data = soup.find_all('a')
print(data)