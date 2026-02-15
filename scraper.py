import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def get_tokyo_events():
    # 抓取东京地区的动漫/游戏活动列表
    url = "https://natalie.mu/anime/event/list/area/13" 
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []

        # 找到活动列表容器
        items = soup.select('.m-eventList_item')
        
        for item in items:
            name = item.select_one('.m-eventList_title').text.strip()
            # 抓取日期区间，例如：2026/02/15(日) 〜 2026/03/01(日)
            date_raw = item.select_one('.m-eventList_date').text.strip()
            link = "https://natalie.mu" + item.select_one('a')['href']
            
            # 简单的日期清洗逻辑
            if "〜" in date_raw:
                start_date = date_raw.split("〜")[0].split("(")[0].strip()
                end_date = date_raw.split("〜")[1].split("(")[0].strip()
            else:
                start_date = date_raw.split("(")[0].strip()
                end_date = start_date

            events.append({
                "name": name,
                "start_date": start_date,
                "end_date": end_date,
                "location": "东京 (详见官网)",
                "category": "动漫/游戏",
                "link": link,
                "ticketing_date": start_date # 默认开票日为开始日，可后期精调
            })
        
        return pd.DataFrame(events)
    except Exception as e:
        print(f"抓取失败: {e}")
        return None

# 执行抓取并覆盖更新 events.csv
df_new = get_tokyo_events()
if df_new is not None and not df_new.empty:
    df_new.to_csv("events.csv", index=False)
    print("数据更新成功！")
