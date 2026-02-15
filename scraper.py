import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_tokyo_events():
    # 使用日本东京地区的动漫活动列表
    url = "https://natalie.mu/anime/event/list/area/13" 
    
    # 模拟真实浏览器的身份证明 (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://natalie.mu/"
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        print(f"DEBUG: 网页响应状态码: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []

        # 尝试更宽泛的选择器，防止类名变动
        items = soup.select('li.m-eventList_item')
        if not items:
            # 备选方案：找所有包含 title 的 p 标签
            items = soup.find_all('p', class_='m-eventList_title')
            print(f"DEBUG: 使用备选方案找到 {len(items)} 个标题")

        for item in soup.select('li.m-eventList_item'):
            try:
                # 抓取标题和链接
                title_node = item.select_one('.m-eventList_title')
                link_node = item.select_one('a')
                date_node = item.select_one('.m-eventList_date')
                
                if title_node and date_node:
                    name = title_node.get_text(strip=True)
                    date_raw = date_node.get_text(strip=True)
                    link = "https://natalie.mu" + link_node['href'] if link_node else ""
                    
                    # 格式化日期：2026/02/15 〜 2026/03/01
                    if "〜" in date_raw:
                        parts = date_raw.split("〜")
                        start = parts[0].split("(")[0].strip().replace("/", "-")
                        end = parts[1].split("(")[0].strip().replace("/", "-")
                    else:
                        start = date_raw.split("(")[0].strip().replace("/", "-")
                        end = start

                    events.append({
                        "name": name,
                        "start_date": start,
                        "end_date": end,
                        "location": "东京地区",
                        "link": link
                    })
            except Exception as e:
                continue

        return pd.DataFrame(events)
    except Exception as e:
        print(f"ERROR: 网络请求异常: {e}")
        return pd.DataFrame()

# 强制执行并输出
df_new = get_tokyo_events()
print(f"DEBUG: 最终抓取到的活动总数: {len(df_new)}")

if not df_new.empty:
    df_new.to_csv("events.csv", index=False)
    print("SUCCESS: 数据已写入 events.csv")
else:
    # 如果抓取不到，为了让 GitHub 有东西可提交，我们写一个“占位符”错误
    print("FAILURE: 本次抓取为空")
