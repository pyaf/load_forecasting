import requests
from bs4 import BeautifulSoup

base_url = 'https://www.delhisldc.org'
url = base_url + '/Loadcurve.aspx'

resp = requests.get(url)
soup = BeautifulSoup(resp.text, 'lxml')
img_link = soup.find('img', {'id': 'ContentPlaceHolder2_chartcontrol1'})['src']
print(img_link)
url = base_url + img_link

f = open('real_time.png','wb')
f.write(requests.get(url).content)
f.close()
