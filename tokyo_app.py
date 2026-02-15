import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="东京 ACG 活动看板", layout="wide", page_icon="🗼")

st.title("🎮 东京实时活动情报站")
st.caption("数据每 24 小时自动抓取，涵盖动漫、游戏与音乐展演")

try:
    # 1. 加载数据
    df = pd.read_csv("events.csv")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    # 获取今天的时间
    today = datetime.now()

    # 2. 按日期排序（最近的在前面）
    df = df.sort_values('start_date', ascending=True)

    # 3. 渲染界面
    for _, row in df.iterrows():
        # 定义状态颜色
        status = ""
        color = "blue"
        
        if today < row['start_date']:
            status = "⏳ 预热中 (Coming Soon)"
            color = "blue"
        elif row['start_date'] <= today <= row['end_date']:
            status = "🔥 进行中 (LIVE)"
            color = "green"
        else:
            status = "⌛ 已结束 (Ended)"
            color = "gray"

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(row['name'])
                # 核心需求：展示起止日期
                st.write(f"📅 **展期：** {row['start_date'].strftime('%Y/%m/%d')} — {row['end_date'].strftime('%Y/%m/%d')}")
                st.write(f"📍 地点：东京 (详见官网链接)")
                st.link_button("🔗 官方资讯/票务", row['link'])
            
            with col2:
                # 展示状态标签
                st.markdown(f"### :{color}[{status}]")
                
                # 如果是进行中，显示剩余天数
                if row['start_date'] <= today <= row['end_date']:
                    remains = (row['end_date'] - today).days
                    st.info(f"剩余 {remains} 天结束")

except Exception as e:
    st.warning("数据正在同步中，请稍后刷新页面查看最新情报。")
