import streamlit as st
import pandas as pd
import datetime
import calendar
import os

DATA_FILE = "data.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["出席番号","週","月", "曜日", "時間",])
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")               

st.title(" 苦手な授業調査 ")

today = datetime.date.today()
first_day = today.replace(day=1)

week_number = (today.day + first_day.weekday()) // 7 + 1

month = today.month

st.header("出席番号")
name = st.text_input("出席番号")

st.subheader("曜日を選択してください")
youbi = ['月曜日','火曜日','水曜日','木曜日','金曜日']
period = st.selectbox("", youbi, index = None)

time = ['一時間目','二時間目','三時間目','四時間目','五時間目','六時間目']
st.subheader(f"{period} の時間を選択してください")
understanding = st.selectbox("", time, index = None)

if st.button("送信"):
    if not name:
        st.write("入力されていない項目があります")
    else:
        new_data = pd.DataFrame({
        "出席番号":[name],
        "週": [week_number],
        "月":[month],
        "曜日": [period],
        "時間": [understanding]
    })
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    st.success(" 回答が送信されました。")

st.header(" 集計結果")
df = pd.read_csv(DATA_FILE)


month_options = ['10','11','12','1','2','3']
selected_month = st.selectbox("月を選択してください", month_options, index = None)
week_options = ['1','2','3','4']
selected_week = st.selectbox("何週目かを選択してください", week_options, index = None)

filtered_df = df[(df["月"] == str(selected_month)) & (df["週"] == str(selected_week))]

if filtered_df.empty:
    st.info("この日付のデータはまだありません。")
else:
    graph = filterd_df.groupby("曜日")["時間"]
    st.bar_chart(graph.set_index("曜日"))
if name == "イチジクのタルト":
        st.dataframe(filtered_df)
