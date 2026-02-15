import streamlit as st
import pandas as pd
from datetime import datetime

# 设置网页基础配置
st.set_page_config(page_title="东京 ACG 活动情报站", layout="wide", page_icon="🗼")

# 你的 Google 表格发布的 CSV 链接
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQxcPB4dwr4Z6KG-CLyMSn2u-tjUzBIHKAHIiq2E9nPn0ahWjGDugBvoXsSwZYWIvqyomSVJDZvwI9u/pub?output=csv"

@st.cache_data(ttl=300) # 每 5 分钟刷新一次缓存
def get_data_from_google():
    try:
        # 1. 读取 CSV 数据
        df = pd.read_csv(CSV_URL)
        
        # 2. 数据清洗：去掉重复的表头行（如果有）并过滤空行
        if 'name' in df.columns:
            df = df[df['name'] != 'name']
            df = df.dropna(subset=['name'])
        
        # 3. 日期转换：将日期字符串转为真正的日期对象，无法转换的变为 NaT
        # errors='coerce' 会自动处理无效格式，避免崩溃
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
        
        # 4. 剔除日期缺失的无效行
        df = df.dropna(subset=['start_date'])
        
        # 5. 排序：按开始日期升序排列
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
    
    # 遍历显示活动
    for _, row in df.iterrows():
        # 判断活动状态
        start_val = row['start_date'].date()
        end_val = row['end_date'].date() if pd.notnull(row['end_date']) else start_val
        
        with st.container(border=True):
