import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_tokyo_events():
    # Natalie 东京动漫活动列表页面
    url = "https://natalie.mu/anime/event/list/area/13" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8' # 强制编码，防止日文乱码
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []

        # 修改为更精准的定位：直接找所有的 li 标签
        items = soup.find_all('li', class_='m-eventList_item')
        print(f"DEBUG: 找到 HTML 节点数量: {len(items)}") 

        for item in items:
            # 抓取标题
            title_node = item.find('p', class_='m-eventList_title')
            # 抓取日期
            date_node = item.find('p', class_='m-eventList_date')
            # 抓取链接
            link_node = item.find('a')

            if title_node and date_node and link_node:
                name = title_node.get_text(strip=True)
                date_raw = date_node.get_text(strip=True)
                link = "https://natalie.mu" + link_node['href']
                
                # 处理日期逻辑：2026/02/15(日) 〜 2026/03/01(日)
                if "〜" in date_raw:
                    parts = date_raw.split("〜")
                    start_date = parts[0].split("(")[0].replace("/", "-").strip()
                    end_date = parts[1].split("(")[0].replace("/", "-").strip()
                else:
                    start_date = date_raw.split("(")[0].replace("/", "-").strip()
                    end_date = start_date

                events.append({
                    "name": name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "location": "东京地区",
                    "category": "动漫展演",
                    "link": link,
                    "ticketing_date": start_date
                })

        return pd.DataFrame(events)
    except Exception as e:
        print(f"ERROR: 抓取过程中出现异常: {e}")
        return pd.DataFrame()

# 执行抓
