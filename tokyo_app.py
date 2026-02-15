import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="东京活动实时看板", layout="wide")
st.title("🗼 东京最新活动")

@st.cache_data(ttl=600)
def load_data():
    return pd.read_csv("events.csv")

try:
    df = load_data()
    
    # 核心排错逻辑：检查列名
    required_columns = ['name', 'start_date', 'end_date']
    missing = [col for col in required_columns if col not in df.columns]
    
    if missing:
        st.error(f"⚠️ 数据库结构错误！缺少列: {missing}")
        st.info("请检查 events.csv 的表头是否包含 name, start_date, end_date")
        # 展示当前的表头供 PM 参考
        st.write("当前 CSV 的表头为:", list(df.columns))
    else:
        # 正常渲染逻辑
        df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
        today = datetime.now()

        for _, row in df.iterrows():
            with st.container(border=True):
                st.subheader(row['name'])
                # 安全读取日期
                d_start = row['start_date'].strftime('%Y/%m/%d') if pd.notnull(row['start_date']) else "待定"
                d_end = row['end_date'].strftime('%Y/%m/%d') if pd.notnull(row['end_date']) else "待定"
                st.write(f"📅 展期：{d_start} 〜 {d_end}")
                st.link_button("查看详情", row['link'])
                st.divider()

except Exception as e:
    st.error(f"系统运行异常: {e}")
