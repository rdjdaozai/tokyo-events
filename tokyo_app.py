import streamlit as st
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(page_title="东京情报站", page_icon="🗼")

# 标题
st.title("🎮 Tokyo ACG Event Hub")

# 读取数据 (增加错误处理)
try:
    df = pd.read_csv("events.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    # 侧边栏：搜索和筛选
    search_query = st.sidebar.text_input("🔍 搜索活动名称", "")
    categories = st.sidebar.multiselect("🏷️ 类别", options=df['category'].unique(), default=df['category'].unique())

    # 数据过滤
    mask = (df['name'].str.contains(search_query, case=False)) & (df['category'].isin(categories))
    filtered_df = df[mask].sort_values(by="date")

    # 展示
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            with st.expander(f"{row['date'].strftime('%m/%d')} | {row['name']}"):
                st.write(f"📍 **地点**: {row['location']}")
                st.write(f"🔥 **推荐度**: {row['rating']}")
                st.write(f"📂 **分类**: {row['category']}")
                st.link_button("🔗 前往官网/票务", row['link'])
    else:
        st.info("没找到相关活动，换个关键词试试？")

except Exception as e:
    st.error("数据库加载失败，请检查 events.csv 格式是否正确。")
