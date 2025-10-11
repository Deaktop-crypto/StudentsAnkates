import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="授業理解度アンケート", page_icon="📊")

st.title("📖 授業理解度アンケート")

st.write("授業の理解度を教えてください。今後の授業改善の参考にします！")

# --- 回答フォーム ---
with st.form("survey_form"):
    name = st.text_input("お名前（任意）")
    understanding = st.slider("授業の理解度（0〜100）", 0, 100, 50)
    comment = st.text_area("授業へのコメント（感想・疑問など）")

    submitted = st.form_submit_button("送信")

# --- 回答が送信されたときの処理 ---
if submitted:
    # CSVファイルが存在しない場合は作成
    file_path = "answers.csv"
    new_data = pd.DataFrame({
        "名前": [name if name else "匿名"],
        "理解度": [understanding],
        "コメント": [comment]
    })
    if not os.path.exists(file_path):
        new_data.to_csv(file_path, index=False, encoding="utf-8-sig")
    else:
        new_data.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8-sig")

    st.success("✅ 回答を送信しました。ありがとうございます！")

# --- 集計結果の表示（教師用） ---
st.markdown("---")
if st.checkbox("📈 集計結果を表示する"):
    if os.path.exists("answers.csv"):
        data = pd.read_csv("answers.csv")
        st.subheader("🧮 回答データ一覧")
        st.dataframe(data)

        st.subheader("📊 平均理解度")
        avg_score = round(data["理解度"].mean(), 1)
        st.metric("平均スコア", f"{avg_score} 点")

        st.subheader("📈 理解度の分布")
        st.bar_chart(data["理解度"])

        st.subheader("💬 コメント一覧")
        for _, row in data.iterrows():
            st.write(f"- **{row['名前']}**: {row['コメント']}")
    else:
        st.warning("まだ回答データがありません。")
