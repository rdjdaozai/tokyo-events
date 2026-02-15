import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_source(url, headers):
    try:
        print(f"DEBUG: 嘗試抓取 {url}")
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            return BeautifulSoup(res.text, 'html.parser')
    except:
        return None
    return None

def get_combined_events():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    all_events = []

    # 來源 1: Natalie Anime (修正後的 URL)
    soup1 = scrape_source("https://natalie.mu/anime/event/list?area=13", headers)
    if soup1:
        for item in soup1.select('.m-eventList_item'):
            title = item.select_one('.m-eventList_title').text.strip()
            date_raw = item.select_one('.m-eventList_date').text.strip()
            link = "https://natalie.mu" + item.select_one('a')['href']
            dates = date_raw.split("〜")
            start = dates[0].split("(")[0].strip().replace("/", "-")
            end = dates[1].split("(")[0].strip().replace("/", "-") if len(dates) > 1 else start
            all_events.append({"name": title, "start_date": start, "end_date": end, "link": link})

    # 來源 2: Tokyo Big Sight (預算備用，可根據需要增加更多源)
    # 這裡可以持續擴展其他網站的邏輯...

    return pd.DataFrame(all_events)

df = get_combined_events()
if not df.empty:
    df.to_csv("events.csv", index=False)
    print(f"SUCCESS: 總共更新了 {len(df)} 條活動數據")
else:
    print("FAILURE: 所有來源均未獲取到數據")
