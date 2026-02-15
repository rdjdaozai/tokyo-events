import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="东京情报站 3.0", layout="wide", page_icon="🗼")

# 1. 样式美化
st.markdown("""
    <style>
    .event-card { border: 1px solid #e6e9ef; border-radius: 10px; padding: 15px; margin-bottom: 10px; background: #ffffff; }
    .countdown { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 Tokyo ACG Hub - 自动更新版")

# 2. 读取数据
try:
    df = pd.read_csv("events.csv")
    df['date'] = pd.to_datetime(df['date'])
    df['ticketing_date'] = pd.to_datetime(df['ticketing_date'])

    # --- 顶栏：实时信息 ---
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.metric("今日日期", datetime.now().strftime('%Y-%m-%d'))
    with col_t2:
        # 这里未来接入 OpenWeather API
        st.metric("东京天气 (预测)", "12°C ☀️")

    st.divider()

    # 3. 核心功能展示
    for _, row in df.sort_values('date').iterrows():
        with st.container():
            # 计算倒计时 (功能 C)
            days_to_ticket = (row['ticketing_date'] - datetime.now()).days
            
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(row['name'])
                st.caption(f"📍 {row['location']} | 🏷️ {row['category']}")
                
                # 功能 A: Google Maps 导航
                map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(row['location'])}"
                st.link_button(f"🗺️ 导航到 {row['location']}", map_url)
                
            with c2:
                if days_to_ticket > 0:
                    st.error(f"⌛ 抢票倒计时: {days_to_ticket} 天")
                elif days_to_ticket == 0:
                    st.warning("🚨 今天开票！")
                else:
                    st.success("🎫 售票中/已结束")
                
                st.link_button("🔗 官网详情", row['link'])
            st.divider()

except Exception as e:
    st.error("数据加载中，请稍后刷新...")
