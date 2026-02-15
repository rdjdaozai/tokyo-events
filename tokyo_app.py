import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="东京活动实时看板", layout="wide")

st.title("🗼 东京最新活动 (自动更新版)")

try:
    # 加载爬虫生成的数据
    df = pd.read_csv("events.csv")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    today = datetime.now()

    # 简单的统计
    st.caption(f"最后更新时间：{today.strftime('%Y-%m-%d %H:%M')}")

    for _, row in df.iterrows():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(row['name'])
                st.write(f"📅 展期：{row['start_date'].strftime('%Y/%m/%d')} 〜 {row['end_date'].strftime('%Y/%m/%d')}")
                st.write(f"📍 {row['location']}")
                st.link_button("查看官网详情", row['link'])
            
            with col2:
                # 状态逻辑：计算当前处于展期的哪个阶段
                if today < row['start_date']:
                    st.warning("📅 尚未开始")
                elif row['start_date'] <= today <= row['end_date']:
                    st.success("🔥 正在进行中")
                else:
                    st.error("⌛ 已结束")

except Exception as e:
    st.info("数据正在努力抓取中，请稍后再试...")
