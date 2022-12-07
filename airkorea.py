# AirKorea OpenAPI 사용
import urllib.request
# request 모듈 import

M = '&numOfRows=1&pageNo=1&stationName=신흥동&dataTerm=DAILY&ver=1.3'
key ='tsFgvelgFo8g9a12hc4f1YCn9z2S16kGxMe7FbBTAaPyEcR8gI2K8bFpegdO2S4ngadYMTWn64d0MFzYHzH71w%3D%3D'
url = 'https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=' + key + M
# 변수url의 구조: 'url주소'+'?ServiceKey='+'인증키를 넣기'+조건

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)

rescode = response.getcode()
if(rescode==200):
  response_body = response.read()
  print(response_body.decode('utf-8'))
else:
  print("Error Code:" + rescode)
