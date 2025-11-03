import streamlit as st
import pandas as pd
import datetime
import os

DATA_FILE = "data.csv"

# CSVがなければ作成
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["出席番号","日付","時間"])
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

st.title("難しかった授業アンケート")

# ----------- 入力UI ------------------

num = st.number_input("出席番号", min_value=1, max_value=31, step=1)
date = st.date_input("日付", datetime.date.today())
jikan = st.selectbox("時間", [1,2,3,4,5,6])

# ----------- 保存 ---------------------

if st.button("送信"):
    new_data = pd.DataFrame([{
        "出席番号": num,
        "日付": date.strftime("%Y-%m-%d"),   # 日付を文字列にして保存
        "時間": jikan
    }])

    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

    st.success("アンケートを送信しました")

target_date = datetime.date(2025, 9, 9)
if date == target_date:
    st.write("イチジクのタルト")
