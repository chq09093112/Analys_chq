from datetime import date, datetime
import time
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id1 = os.environ["USER_ID"]
user_id2 = user_id1.split(',')
template_id = os.environ["TEMPLATE_ID"]

def get_weekdays():
  week_list=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  local_time=time.localtime(time.time())
  week_index=local_time.tm_wday
  week=week_list[week_index]
  return week

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


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea,"color":get_random_color()},"city":{"value":city,"color":get_random_color()},"today":{"value":get_weekdays(),"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}

i=0
global user_id
while i < len(user_id2):
  user_id = user_id2[i]
  res = wm.send_template(user_id, template_id, data)
  print(res)
  i+=1
