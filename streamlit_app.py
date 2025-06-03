import streamlit as st
import random

# 単語リストと辞書をセッションステートで管理
if "words_to_learn" not in st.session_state:
    st.session_state.words_to_learn = []

if "word_dict" not in st.session_state:
    st.session_state.word_dict = {}

if "incorrect_words" not in st.session_state:
    st.session_state.incorrect_words = []

# 1. 単語を入力するフォーム
def input_words():
    st.title("英単語学習アプリ")
    st.write("覚えたい英単語とその意味を入力してください。")

    with st.form(key='word_form'):
        word = st.text_input("英単語")
        meaning = st.text_input("意味")
        submit_button = st.form_submit_button(label="単語を追加")

    if submit_button:
        if word and meaning:
            if word not in st.session_state.words_to_learn:
                st.session_state.words_to_learn.append(word)
                st.session_state.word_dict[word] = meaning
                st.success(f"単語「{word}」が追加されました。")
            else:
                st.warning("この単語はすでにリストにあります。")
        else:
            st.error("単語と意味を両方入力してください。")

# 2. クイズを出題する関数
def quiz():
    st.title("英単語クイズ")

    if not st.session_state.words_to_learn:
        st.warning("まず、覚えたい単語を入力してください。")
        return

    # 間違えた単語があれば優先的に出題
    if st.session_state.incorrect_words:
        word_to_ask = random.choice(st.session_state.incorrect_words)
    else:
        word_to_ask = random.choice(st.session_state.words_to_learn)

    meaning = st.session_state.word_dict[word_to_ask]

    st.write(f"この英単語の意味は何ですか？: **{word_to_ask}**")
    answer = st.text_input("意味を入力してください:", key="quiz_answer")

    if answer:
        if answer.strip().lower() == meaning.strip().lower():
            st.success("正解！")
            if word_to_ask in st.session_state.incorrect_words:
                st.session_state.incorrect_words.remove(word_to_ask)
            # 入力クリアのために再読み込みする小ワザ
            st.experimental_rerun()
        else:
            st.error(f"不正解。正しい意味は「{meaning}」です。")
            if word_to_ask not in st.session_state.incorrect_words:
                st.session_state.incorrect_words.append(word_to_ask)
            st.experimental_rerun()

# 3. 進捗ダッシュボード
def progress_dashboard():
    st.title("進捗ダッシュボード")

    total = len(st.session_state.words_to_learn)
    incorrect = len(st.session_state.incorrect_words)
    learned = total - incorrect

    st.metric("覚えた単語数", learned)
    st.metric("覚えていない単語数", incorrect)
    st.metric("単語総数", total)

    if total > 0:
        progress = (learned / total) * 100
        st.progress(progress)
        st.write(f"進捗率: {progress:.1f}%")

    if incorrect > 0:
        st.subheader("間違えた単語リスト")
        for w in st.session_state.incorrect_words:
            st.write(f"- **{w}** : {st.session_state.word_dict[w]}")

    else:
        st.write("全ての単語を覚えました！おめでとうございます！🎉")

# 4. メイン画面
def main():
    st.sidebar.title("メニュー")
    option = st.sidebar.radio("選択してください", ("単語入力", "クイズ", "進捗ダッシュボード"))

    if option == "単語入力":
        input_words()
    elif option == "クイズ":
        quiz()
    elif option == "進捗ダッシュボード":
        progress_dashboard()

if __name__ == "__main__":
    main()

