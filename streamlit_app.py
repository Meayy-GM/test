import streamlit as st
import random
import json

# サンプル単語と意味のリスト
# 本番環境ではこのデータを外部ファイルやAPIから取得することもできます
word_list = [
    {"word": "Algorithm", "meaning": "A step-by-step procedure for solving a problem."},
    {"word": "API", "meaning": "A set of protocols for building and interacting with software applications."},
    {"word": "Database", "meaning": "An organized collection of structured information or data."},
    {"word": "Framework", "meaning": "A set of tools and libraries used to create software applications."},
    {"word": "Cloud Computing", "meaning": "The delivery of computing services like storage and processing over the internet."},
    {"word": "Encryption", "meaning": "The process of converting information into a code to prevent unauthorized access."},
    {"word": "Object-Oriented Programming", "meaning": "A programming paradigm based on objects and data rather than actions."},
    {"word": "Data Structure", "meaning": "A particular way of organizing and storing data."},
    {"word": "Version Control", "meaning": "A system that tracks changes to code or documents over time."},
    {"word": "Machine Learning", "meaning": "A branch of AI that uses algorithms to allow computers to learn from data."}
]

# ユーザーの進捗を保存する（ユーザーが覚えた単語を記録する）
if 'learned_words' not in st.session_state:
    st.session_state.learned_words = []

# フラッシュカード形式の学習モード
def learning_mode():
    if len(st.session_state.learned_words) < len(word_list):
        # まだ覚えていない単語を表示
        remaining_words = [w for w in word_list if w not in st.session_state.learned_words]
        word = random.choice(remaining_words)  # ランダムに単語を選ぶ
        st.write(f"### 単語: {word['word']}")
        st.write(f"意味: {word['meaning']}")

        # 覚えたかどうかを選択するボタン
        correct = st.button("覚えた！")
        if correct:
            st.session_state.learned_words.append(word)
            st.success(f"'{word['word']}' を覚えました！")
    else:
        st.write("すべての単語を覚えました！")
        st.write("復習モードへ進むことができます。")

# 復習モード
def review_mode():
    if len(st.session_state.learned_words) > 0:
        word = random.choice(st.session_state.learned_words)  # 覚えた単語の中からランダムに選ぶ
        st.write(f"### 覚えた単語: {word['word']}")
        st.write(f"意味: {word['meaning']}")

        # 再度覚えたかどうかを確認するボタン
        correct = st.button(f"'{word['word']}' を再度確認")
        if correct:
            st.success(f"再確認しました！")
    else:
        st.write("まだ覚えた単語がありません。まずは学習モードから始めましょう！")

# サイドバーでタブを切り替え
st.sidebar.title("システム単語学習アプリ")
mode = st.sidebar.radio("学習モードを選んでください", ["学習モード", "復習モード"])

if mode == "学習モード":
    st.title("学習モード")
    learning_mode()
elif mode == "復習モード":
    st.title("復習モード")
    review_mode()

