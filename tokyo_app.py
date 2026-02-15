import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="東京 ACG 情報中心", layout="wide", page_icon="🗼")

# --- 側邊欄：社交媒體實時流 ---
with st.sidebar:
    st.title("📱 SNS 實時熱點")
    st.write("查看 X (Twitter) 上的最新討論")
    # 嵌入 X (Twitter) Widget：搜尋 #東京イベント #ACG 相關內容
    components.html(
        """
        <a class="twitter-timeline" data-height="800" data-theme="light" href="https://twitter.com/hashtag/%E6%9D%B1%E4%BA%AC%E3%82%A4%E3%83%99%E3%83%B3%E3%83%88?src=hash&ref_src=twsrc%5Etfw">#東京活動 實時動態</a> 
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """,
        height=800,
    )

# --- 主界面 ---
st.title("🗼 東京 ACG 活動情報站 4.0")

try:
    df = pd.read_csv("events.csv")
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    today = datetime.now()

    # 排序：進行中的排在最前面
    df['status_rank'] = df.apply(lambda x: 0 if x['start_date'] <= today <= x['end_date'] else 1, axis=1)
    df = df.sort_values(['status_rank', 'start_date'])

    for _, row in df.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.subheader(row['name'])
                st.write(f"📅 展期：{row['start_date'].strftime('%Y/%m/%d')} — {row['end_date'].strftime('%Y/%m/%d')}")
                st.write(f"📍 地點：{row.get('location', '東京')}")
                st.link_button("🔗 詳情/票務鏈接", row['link'])
            with c2:
                if today < row['start_date']:
                    st.info("⌛ 尚未開始")
                elif row['start_date'] <= today <= row['end_date']:
                    st.success("🔥 正在進行")
                else:
                    st.gray("⌛ 已結束")
except Exception as e:
    st.info("數據正在從多個來源同步中，請稍後...")
