import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="东京活动站", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQxcPB4dwr4Z6KG-CLyMSn2u-tjUzBIHKAHIiq2E9nPn0ahWjGDugBvoXsSwZYWIvqyomSVJDZvwI9u/pub?output=csv"

@st.cache_data(ttl=300) 
def get_data():
    try:
        df = pd.read_csv(CSV_URL)
        df = df[df['name'] != 'name']
        df = df.dropna(subset=['name'])
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
        return df.dropna(subset=['start_date']).sort_values('start_date')
    except Exception as e:
        st.error(f"同步失败: {e}")
        return pd.DataFrame()

st.title("🗼 东京 ACG 活动情报站")
df = get_data()
today = datetime.now().date()

if not df.empty:
    for _, row in df.iterrows():
        s_date = row['start_date'].date()
        e_date = row['end_date'].date() if pd.notnull(row['end_date']) else s_date
        
        with st.container(border=True):
            st.subheader(row['name'])
            st.write(f"📅 {s_date} — {e_date} | 📍 {row.get('location', '东京')}")
            
            # 状态显示
            if today < s_date:
                st.info("⌛ 尚未开始")
            elif s_date <= today <= e_date:
                st.success("🔥 正在进行中")
            else:
                st.text("🔒 活动已结束")
            
            # --- 核心修复：链接清洗逻辑 ---
            raw_link = str(row.get('link', '')).strip() # 去掉前后空格
            
            if raw_link and raw_link != 'nan':
                # 如果链接不包含 http，自动补全（防止变成相对路径）
                clean_link = raw_link if raw_link.startswith('http') else f"https://{raw_link}"
                st.link_button("🔗 查看详情", clean_link)
            else:
                st.button("🚫 暂无官方链接", disabled=True)
else:
    st.warning("📭 暂无数据，请检查 Google 表格。")

with st.sidebar:
    if st.button("🔄 刷新数据"):
        st.cache_data.clear()
        st.rerun()
