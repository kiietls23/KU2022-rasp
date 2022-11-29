import requests
from bs4 import BeautifulSoup
import pandas
M='&numOfRows=1&pageNo=1&stationName=신흥동&dataTerm=DAILY&ver=1.0'
key='tsFgvelgFo8g9a12hc4f1YCn9z2S16kGxMe7FbBTAaPyEcR8gI2K8bFpegdO2S4ngadYMTWn64d0MFzYHzH71w%3D%3D
'
url='http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey='+key+M

response-requests.get(url)
soup=BeautifulSoup(response.text, "html.parser")
ItemList=soup.findAll('item')
for item in ItemList:
    a = item.find('datatime').text
    g = item.find('pm10value').text
    i = item.find('pm25value').text
    s = item.find('pm10grade1h').text
    t = item.find('pm25grade1h').text
    print('측정소: 신흥동')
    print('측정시간:'+a)
    print('미세먼지 농도:'+g+'㎍/㎥('+s+')')
    print('초미세먼지 농도:'+i+'㎍/㎥('+s+')')
    print('(좋음:1), (보통:2), (나쁨:3), (매우나쁨:4)')
