import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def get_free_events():
    # 使用 RSSHub 的公共网关（如果这个挂了可以换一个）
    # 来源：Eventernote 东京活动
    url = "https://rsshub.app/eventernote/actors/13" 
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        # RSS 是 XML 格式，非常容易解析
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        events = []
        for item in items:
            title = item.title.text
            link = item.link.text
            description = item.description.text # 里面通常包含日期和地点
            
            # 使用正则从标题或描述中提取日期 (例如 2026-02-15)
            date_match = re.search(r'\d{4}-\d{2}-\d{2}', title + description)
            found_date = date_match.group(0) if date_match else "2026-02-15"
            
            events.append({
                "name": title.split(' [')[0], # 清洗标题
                "start_date": found_date,
                "end_date": found_date, # 演出通常是单日
                "link": link,
                "location": "东京"
            })
        return pd.DataFrame(events)
    except Exception as e:
        print(f"抓取失败: {e}")
        return pd.DataFrame()

df = get_free_events()
if not df.empty:
    df.to_csv("events.csv", index=False)
    print(f"成功免费获取 {len(df)} 条数据")
