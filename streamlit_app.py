import streamlit as st
import random

st.title("英単語クイズアプリ")

# セッションステートに単語リストを保存
if 'word_list' not in st.session_state:
    st.session_state.word_list = []

# モード選択（登録 or クイズ）
mode = st.sidebar.radio("モードを選んでください", ["単語を登録する", "クイズに挑戦"])

# ----------------------
# 単語登録モード
# ----------------------
if mode == "単語を登録する":
    st.header("単語を登録")

    with st.form(key="word_form"):
        word = st.text_input("英単語を入力:")
        meaning = st.text_input("日本語の意味を入力:")
        submit = st.form_submit_button("登録する")

        if submit:
            if word and meaning:
                st.session_state.word_list.append({"word": word, "meaning": meaning})
                st.success(f"単語 '{word}' を登録しました！")
            else:
                st.error("両方のフィールドに入力してください。")

    # 現在の登録単語の一覧表示
    if st.session_state.word_list:
        st.subheader("登録済みの単語一覧")
        for idx, entry in enumerate(st.session_state.word_list):
            st.write(f"{idx+1}. {entry['word']} - {entry['meaning']}")

# ----------------------
# クイズモード
# ----------------------
elif mode == "クイズに挑戦":
    st.header("クイズに挑戦！")

    if not st.session_state.word_list:
        st.warning("まず単語を登録してください。")
    else:
        # ランダムに1つ出題
        question = random.choice(st.session_state.word_list)
        st.subheader(f"英単語: **{question['word']}** の意味は？")

        user_answer = st.text_input("あなたの答え（日本語）を入力:")
        if st.button("答え合わせ"):
            if user_answer.strip() == question["meaning"]:
                st.success("正解！")
            else:
                st.error(f"不正解！正しい答えは: {question['meaning']}")

import json
import pandas as pd

# サンプル単語データ（正答率トラッキング付き）
word_data = [
    {"word": "Algorithm", "meaning": "アルゴリズム", "correct": 3, "wrong": 2},
    {"word": "Database", "meaning": "データベース", "correct": 1, "wrong": 4},
    {"word": "Encryption", "meaning": "暗号化", "correct": 5, "wrong": 0},
]

# JSONにエクスポート
with open("words.json", "w", encoding="utf-8") as f:
    json.dump(word_data, f, indent=4, ensure_ascii=False)

# CSVにエクスポート（pandas使用）
df = pd.DataFrame(word_data)
df.to_csv("words.csv", index=False, encoding="utf-8-sig")


