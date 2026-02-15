import streamlit as st
import pandas as pd
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="Tokyo ACG Event Tracker", page_icon="🗼", layout="wide")

# 自定义 CSS 样式（符合日系简洁审美）
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stCard { border-radius: 10px; padding: 20px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .type-tag { font-size: 12px; padding: 2px 8px; border-radius: 4px; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. 模拟数据库 (2026年最新活动)
events_data = [
    {"名称": "名侦探柯南 30周年展", "日期": "2026-02-20", "地点": "东京巨蛋", "分类": "动漫", "推荐度": "⭐⭐⭐⭐⭐"},
    {"名称": "hololive SUPER EXPO 2026", "日期": "2026-03-06", "地点": "幕张展览馆", "分类": "VTuber/音乐", "推荐度": "⭐⭐⭐⭐⭐"},
    {"名称": "Death Stranding 音乐会", "日期": "2026-02-23", "地点": "涩谷公会堂", "分类": "游戏音乐", "推荐度": "⭐⭐⭐⭐"},
    {"名称": "AnimeJapan 2026", "日期": "2026-03-28", "地点": "东京 Big Sight", "分类": "综合动漫", "推荐度": "⭐⭐⭐⭐⭐"},
    {"名称": "Final Fantasy Pop-up Store", "日期": "2026-02-15", "地点": "新宿伊势丹", "分类": "游戏", "推荐度": "⭐⭐⭐"},
    {"名称": "米津玄师 2026 巡演 (东京站)", "日期": "2026-03-12", "地点": "国立竞技场", "分类": "音乐", "推荐度": "⭐⭐⭐⭐⭐"},
]

df = pd.DataFrame(events_data)
df['日期'] = pd.to_datetime(df['日期'])

# --- 侧边栏筛选 ---
st.sidebar.title("🗼 东京活动筛选")
category = st.sidebar.multiselect("选择分类", options=df['分类'].unique(), default=df['分类'].unique())
date_range = st.sidebar.date_input("选择日期范围", [datetime(2026, 2, 1), datetime(2026, 4, 1)])

# 过滤数据
filtered_df = df[(df['分类'].isin(category)) & 
                 (df['日期'] >= pd.to_datetime(date_range[0])) & 
                 (df['日期'] <= pd.to_datetime(date_range[1]))]

# --- 主界面 ---
st.title("🎮 Tokyo ACG & Music Hub")
st.caption(f"你好，产品经理！今天是 2026年2月15日。这是为您汇总的最新情报。")

# 核心统计
col1, col2, col3 = st.columns(3)
col1.metric("本月活动", len(filtered_df[filtered_df['日期'].dt.month == 2]))
col2.metric("热门场次", "4 场")
col3.metric("最近更新", "15 分钟前")

st.divider()

# 活动展示卡片
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        with st.container():
            c1, c2, c3 = st.columns([2, 5, 2])
            with c1:
                st.write(f"📅 **{row['日期'].strftime('%Y-%m-%d')}**")
            with c2:
                st.subheader(row['名称'])
                st.write(f"📍 {row['地点']} | 🏷️ {row['分类']}")
            with c3:
                st.write(f"热度: {row['推荐度']}")
                st.button("查看详情", key=index)
            st.divider()
else:
    st.warning("所选范围内暂无活动，去涩谷喝杯咖啡吧！")

# 底部功能
st.sidebar.info("💡 提示：这是一个基于 Python 的实时 Web 应用原型。")