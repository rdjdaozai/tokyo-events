import streamlit as st
import pandas as pd

# 1. 填入你刚才从“发布到网络”获取的那个长链接
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQxcPB4dwr4Z6KG-CLyMSn2u-tjUzBIHKAHIiq2E9nPn0ahWjGDugBvoXsSwZYWIvqyomSVJDZvwI9u/pub?output=csv"

@st.cache_data(ttl=600) # 每 10 分钟刷新一次，保证性能的同时兼顾实时性
def get_data_from_google():
    try:
        # 直接读取 Google 发布的 CSV 链接
        data = pd.read_csv(CSV_URL)
        
        # 预处理：删除空行（防止你在表格下面留了太多空格）
        data = data.dropna(subset=['name'])
        
        # 转换日期格式，防止报错
        data['start_date'] = pd.to_datetime(data['start_date']).dt.date
        data['end_date'] = pd.to_datetime(data['end_date']).dt.date
        
        return data
    except Exception as e:
        st.error(f"数据读取失败：{e}")
        return pd.DataFrame()

# 2. 在主界面显示数据
df = get_data_from_google()

if not df.empty:
    st.success(f"📡 已同步最新情报（共 {len(df)} 条）")
    # 下面接你之前的展示逻辑（st.container 等）
    for _, row in df.iterrows():
        with st.expander(f"📌 {row['name']}"):
            st.write(f"展期：{row['start_date']} 至 {row['end_date']}")
            st.link_button("访问官网", row['link'])
else:
    st.warning("目前表格内没有活动信息，请在 Google 表格中添加。")
