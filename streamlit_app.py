import streamlit as st
import random
import re

st.set_page_config(page_title="長文英文記憶アプリ", layout="wide")
st.title("📘 長文英文記憶アプリ")

# セッション初期化
if 'long_texts' not in st.session_state:
    st.session_state.long_texts = []

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# 長文入力
st.header("1. 長文の英語を入力・保存")
long_input = st.text_area("覚えたい英語の長文を入力してください（例：メールや文章など）", height=200)

if st.button("💾 保存"):
    if long_input.strip():
        st.session_state.long_texts.append(long_input.strip())
        st.success("長文を保存しました！")
    else:
        st.warning("入力が空です。")

# 学習スタート
if st.session_state.long_texts:
    st.header("2. 学習メニューを選択")

    mode = st.radio("学習モードを選択", ["📚 フレーズ分割", "✏️ 穴埋め長文クイズ", "📖 全文シャドーイング"])

    selected_text = st.session_state.long_texts[st.session_state.current_index]

    if st.button("➡️ 次の文章に進む"):
        st.session_state.current_index = (st.session_state.current_index + 1) % len(st.session_state.long_texts)

    st.markdown("---")

    # 📚 フレーズ分割表示
    if mode == "📚 フレーズ分割":
        st.subheader("🔍 フレーズ分割（Chunking）で記憶")
        # シンプルな句読点・接続詞ベースの分割
        phrases = re.split(r'(,|;|\.|\band\b|\bbut\b)', selected_text)
        phrases = [p.strip() for p in phrases if p.strip() and p != ',']
        for i, phrase in enumerate(phrases):
            with st.expander(f"フレーズ {i+1}"):
                st.markdown(f"**{phrase}**")

    # ✏️ 穴埋めクイズ
    elif mode == "✏️ 穴埋め長文クイズ":
        st.subheader("📝 穴埋め長文クイズ")
        words = selected_text.split()
        num_blanks = max(1, len(words) // 8)  # 長さに応じて空欄数調整
        blank_indices = random.sample(range(len(words)), num_blanks)
        answers = {i: words[i] for i in blank_indices}

        quiz_text = " ".join("_____" if i in blank_indices else word for i, word in enumerate(words))
        st.markdown("**次の長文の空欄を埋めてください：**")
        st.write(quiz_text)

        user_answers = {}
        for idx in blank_indices:
            user_answers[idx] = st.text_input(f"空欄「{idx+1}番目の単語」", key=f"blank_{idx}")

        if st.button("✅ 答え合わせ"):
            correct = 0
            for idx in blank_indices:
                if user_answers[idx].strip().lower() == answers[idx].lower():
                    correct += 1
            st.info(f"{len(blank_indices)} 問中 {correct} 問正解！")
            if correct == len(blank_indices):
                st.success("完璧です！✨")
            else:
                for idx in blank_indices:
                    if user_answers[idx].strip().lower() != answers[idx].lower():
                        st.error(f"❌ {idx+1}番目の単語：正解は「{answers[idx]}」")

    # 📖 全文シャドーイング（将来拡張用）
    elif mode == "📖 全文シャドーイング":
        st.subheader("🎧 音読・シャドーイング練習（将来的に音声読み上げ対応）")
        st.markdown("**以下の文章を声に出して読んでみましょう。**")
        st.markdown(f"### {selected_text}")
        st.markdown("※ `pyttsx3` や `gTTS` などを使えば音声読み上げも追加できます")





