import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="东京情报指挥中心", layout="wide")

# --- 侧边栏：社交媒体墙 (这是你现在获取动态最稳的方式) ---
with st.sidebar:
    st.header("📱 SNS 实时情报")
    st.write("以下是 X (Twitter) 上关于 #东京活动 的实时推文：")
    # 使用 Twitter 官方 Widget
    components.html(
        """
        <a class="twitter-timeline" data-height="800" href="https://twitter.com/hashtag/%E6%9D%B1%E4%BA%AC%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88?src=hash&ref_src=twsrc%5Etfw">#東京イベント</a> 
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """,
        height=800,
    )

# --- 主界面 ---
st.title("🗼 东京 ACG 情报站")

try:
    df = pd.read_csv("events.csv")
    st.subheader("🗓️ 精选活动列表")
    for _, row in df.iterrows():
        with st.expander(f"📍 {row['name']}"):
            st.write(f"展期: {row['start_date']} 至 {row['end_date']}")
            st.link_button("访问官网", row['link'])
except:
    st.info("活动列表正在维护中，请先参考左侧实时 SNS 情报。")
