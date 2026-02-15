import streamlit as st
import pandas as pd
from datetime import datetime

# 设置网页基础配置
st.set_page_config(page_title="东京 ACG 活动情报站", layout="wide", page_icon="🗼")

# 你的 Google 表格发布的 CSV 链接
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQxcPB4dwr4Z6KG-CLyMSn2u-tjUzBIHKAHIiq2E9nPn0ahWjGDugBvoXsSwZYWIvqyomSVJDZvwI9u/pub?output=csv"

@st.cache_data(ttl=300) 
def get_data_from_google():
    try:
        df = pd.read_csv(CSV_URL)
        if 'name' in df.columns:
            # 过滤掉重复表头和空名
            df = df[df['name'] != 'name']
            df = df.dropna(subset=['name'])
        
        # 强制日期转换
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
        df = df.dropna(subset=['start_date'])
        df = df.sort_values(by='start_date')
        return df
    except Exception as e:
        st.error(f"⚠️ 数据同步失败：{e}")
        return pd.DataFrame()

# --- 网页界面渲染 ---
st.title("🗼 东京 ACG 活动情报站")
st.markdown("---")

df = get_data_from_google()
today = datetime.now().date()

if not df.empty:
    st.info(f"📊 当前已收录 {len(df)} 条活跃活动情报")
    
    for _, row in df.iterrows():
        start_val = row['start_date'].date()
        end_val = row['end_date'].date() if pd.notnull(row['end_date']) else start_val
        
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(row['name'])
                st.write(f"📅 **时间**：{start_val} — {end_val}")
                # 检查 location 字段
                loc = row.get('location', '东京')
                if pd.notnull(loc):
                    st.write(f"📍 **地点**：{loc}")
            with col2:
                # 状态逻辑
                if today < start_val:
                    st.warning("⌛ 尚未开始")
                elif start
