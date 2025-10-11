import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="授業理解度アンケート")

st.title("授業理解度アンケート")

st.write("授業の理解度を教えてください")

# --- 回答フォーム ---
with st.form("survey_form"):
    name = st.text_input("出席番号")
    first = st.slider(0, 100, 50)
    
    submitted = st.form_submit_button("送信")

# --- 回答が送信されたときの処理 ---
if submitted:
    # CSVファイルが存在しない場合は作成
    file_path = "answers.csv"
    new_data = pd.DataFrame({
        "出席番号": [name],
        "一時間目": [first],
    })
    if not os.path.exists(file_path):
        new_data.to_csv(file_path, index=False, encoding="utf-8-sig")
    else:
        new_data.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8-sig")

    st.success("回答を送信しました")

# --- 集計結果の表示 ---
st.markdown("---")
if st.checkbox("集計結果を表示する"):
    if os.path.exists("answers.csv"):
      
        data = pd.read_csv("answers.csv")
        st.subheader("回答データ一覧")
        st.dataframe(data)

    else:
        st.warning("集計中...")
