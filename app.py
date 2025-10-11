import streamlit as st
import pandas as pd
import datetime
import os

# CSVファイル名
DATA_FILE = "data.csv"
DATA_FILE2 = "data.csv"

# データファイルがない場合は作成
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["日付", "時間", "理解度"])
    df2 = pd.DataFrame(columns=["出席番号", "日付", "時間", "理解度"])
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    df2.to_csv(DATA_FILE2, index=False, encoding="utf-8-sig")                   

# タイトル
st.title(" 授業理解度アンケート ")

# 今日の日付
today = datetime.date.today()

# 選択フォーム
st.header("出席番号")
name = st.text_input("出席番号")

st.subheader(" 時間を選択してください")
period = st.selectbox("時間を選んでください", [f"{i}時間目" for i in range(1, 7)])

st.subheader(f"{period} の理解度を入力してください")
understanding = st.slider("理解度（1: 難しかった 〜 5: よく理解できた）", 1, 5, 3)

# 送信ボタン
if st.button("送信"):
    if not name:
        st.error("入力されていない項目があります")
    else:
    new_data = pd.DataFrame({
        "日付": [today],
        "時間": [period],
        "理解度": [understanding]
    })
    new_data2 = pd.DataFrame({
        "出席番号":[name],
        "日付":[today],
        "時間":[period],
        "理解度":[understanding]
    })
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    df2 = pd.read_csv(DATA_FILE2)
    df2 = pd.concat([df2, new_data2], ignore_index=True)
    df2.to_csv(DATA_FILE2, index=False, encoding="utf-8-sig")
    st.success(" 回答が送信されました。")

# 集計表示
st.header(" 集計結果")
df = pd.read_csv(DATA_FILE)
df2 = pd.read_csv(DATA_FILE2)

# 日付フィルター
selected_date = st.date_input("日付を選択", today)

filtered_df = df[df["日付"] == str(selected_date)]

if filtered_df.empty:
    st.info("この日付のデータはまだありません。")
else:
    avg_scores = filtered_df.groupby("時間")["理解度"].mean().reset_index()
    st.bar_chart(avg_scores.set_index("時間"))
    
    st.dataframe(filtered_df)
