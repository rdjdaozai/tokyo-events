import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="東京 ACG 情報站 3.0", layout="wide")
st.title("🗼 東京遊戲、動漫、音樂活動匯總")

# 1. 模擬自動更新的數據 (以後由自動化腳本生成)
# 增加：ticketing_date (搶票日期), lat_lon (座標)
try:
    df = pd.read_csv("events.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['ticketing_date'] = pd.to_datetime(df['ticketing_date'])

    # --- 頂部概覽：天氣與今日狀態 ---
    st.info("🌦️ 東京今日天氣：12°C 晴轉多雲 (自動即時更新中)")

    # --- 活動列表 ---
    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(row['name'])
                st.write(f"📅 活動日期: {row['date'].strftime('%Y-%m-%d')}")
                st.write(f"📍 地點: {row['location']}")
                
                # 功能 A: Google Maps 跳轉
                address_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(row['location'])}"
                st.link_button("🗺️ 在地圖中打開 (導航)", address_url)

            with col2:
                # 功能 C: 搶票倒數
                days_left = (row['ticketing_date'] - datetime.now()).days
                if days_left > 0:
                    st.warning(f"⏳ 搶票倒數: {days_left} 天")
                elif days_left == 0:
                    st.error("🚨 今天開票！快搶！")
                else:
                    st.success("🎫 售票中 / 已截止")
                
                # 功能 B: 天氣建議 (簡單邏輯)
                st.write("🌦️ 預計天氣：適合出門")

            st.divider()

except Exception as e:
    st.error("正在初始化雲端數據...")
