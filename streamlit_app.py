import streamlit as st
import random

st.title("🧠 英文記憶学習アプリ")

# セッション状態の初期化
if 'sentences' not in st.session_state:
    st.session_state.sentences = []

if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0

if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

st.subheader("1. 覚えたい英語の文章を入力")

input_text = st.text_area("英語の文章を1行ずつ入力してください（例：This is a pen.）", height=150)

if st.button("📥 保存する"):
    lines = input_text.strip().split('\n')
    st.session_state.sentences.extend([line.strip() for line in lines if line.strip()])
    st.success("文章が保存されました！")

if st.session_state.sentences:
    st.subheader("2. 学習メニュー")

    menu = st.radio("学習モードを選んでください", ["🔁 フラッシュカード", "✏️ 穴埋めクイズ", "❓ クイズ形式"])

    sentences = st.session_state.sentences

    if menu == "🔁 フラッシュカード":
        st.write("英語の文章を1つずつ表示して記憶しましょう")
        idx = st.session_state.quiz_index % len(sentences)
        st.markdown(f"### 👉 {sentences[idx]}")
        if st.button("次へ"):
            st.session



