import streamlit as st
import pandas as pd
from datetime import datetime

# 强制刷新缓存，确保读到的是最新数据
@st.cache_data(ttl=3600)
def load_data():
    return pd.read_csv("events.csv")

st.title("🗼 东京活动实时看板")

try:
    df = load_data()
    # 打印一下列名，方便你在测试阶段排查 (上线后可以删掉)
    # st.write(df.columns) 

    # 转换日期格式
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    # ... 其余展示逻辑 ...
    for _, row in df.iterrows():
        st.write(f"### {row['name']}")
        st.write(f"📅 {row['start_date'].date()} ~ {row['end_date'].date()}")
        st.divider()

except Exception as e:
    st.error(f"异常信息: {e}") # 这里改一下，能让你直接看到报了什么错
