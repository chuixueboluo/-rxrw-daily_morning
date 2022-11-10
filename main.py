from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
morning_template_id = os.environ["MORNING_TPID"]

def get_date():
  week=""
  if datetime.now.weekday()==0:
    week="星期一"
  elif datetime.now.weekday()==1:
    week="星期二"
  elif datetime.now.weekday()==2:
    week="星期三"
  elif datetime.now.weekday()==3:
    week="星期四"
  elif datetime.now.weekday()==4:
    week="星期五"
  elif datetime.now.weekday()==5:
    week="星期六"
  elif datetime.now.weekday()==6:
    week="星期日"
  datetime.now.weekday()+1
  return today.strftime('%Y-%m-%d')+" "+week

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_morning_msg():
    url = f"http://api.tianapi.com/zaoan/index?key=8aed16381cecc47f036d997cdf04ba1c"
    ret = requests.get(url)
    ret = ret.content.decode('utf8').replace("'", '"')
    data_json = json.loads(ret)
    msg = data_json['newslist'][-1]['content']
    print(msg)
    return msg

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"date_date":{"value":get_date(),"color":get_random_color()},"zaoan":{"value":get_morning_msg(),"color":get_random_color()},"weather":{"value":wea,"color":get_random_color()},"temp":{"value":temperature,"color":get_random_color()},"meet_days":{"value":get_count()},"birthday_left":{"value":get_birthday()}}
res = wm.send_template(user_id, morning_template_id, data)
print(res)
