import streamlit as st
import random

st.set_page_config(page_title="英単語クイズアプリ", layout="centered")

st.title("📘 英単語クイズアプリ")

# ---------------------------
# 初期化
# ---------------------------
if "word_dict" not in st.session_state:
    st.session_state.word_dict = {}

if "score" not in st.session_state:
    st.session_state.score = {"correct": 0, "total": 0}

# ---------------------------
# 出題方向の選択
# ---------------------------
st.sidebar.header("⚙️ 設定")
quiz_mode = st.sidebar.radio("出題形式", ["意味 → 英単語", "英単語 → 意味"])

# ---------------------------
# 単語入力
# ---------------------------
st.subheader("✍️ 英単語と意味の登録")
input_text = st.text_area("英単語,意味 の形式で1行ずつ入力してください（例：apple,りんご）", height=150)

if st.button("単語を保存"):
    if input_text.strip():
        lines = input_text.strip().split('\n')
        for line in lines:
            if ',' in line:
                word, meaning = line.split(',', 1)
                st.session_state.word_dict[word.strip()] = meaning.strip()
        st.success("単語を保存しました！")
    else:
        st.warning("入力が空です。")

# ---------------------------
# 単語がある場合はクイズを表示
# ---------------------------
if st.session_state.word_dict:
    st.subheader("🧠 クイズに挑戦！")

    word_dict = st.session_state.word_dict
    correct_word, correct_meaning = random.choice(list(word_dict.items()))
    num_options = min(4, len(word_dict))

    # 選択肢作成
    if quiz_mode == "意味 → 英単語":
        all_words = list(word_dict.keys())
        all_words.remove(correct_word)
        choices = random.sample(all_words, num_options - 1) + [correct_word]
        random.shuffle(choices)
        st.write(f"次の意味に合う英単語はどれ？：**{correct_meaning}**")
        selected = st.radio("選択肢", choices)
        correct_answer = correct_word

    else:
        all_meanings = list(word_dict.values())
        all_meanings.remove(correct_meaning)
        choices = random.sample(all_meanings, num_options - 1) + [correct_meaning]
        random.shuffle(choices)
        st.write(f"次の英単語の意味はどれ？：**{correct_word}**")
        selected = st.radio("選択肢", choices)
        correct_answer = correct_meaning

    if st._bottom("回答する"):
        st.session_state.score["total"] += 1
        if selected == correct_answer:
            st.session_state.score["correct"] += 1
            st.success("🎉 正解！")
        else:
            st.error(f"😢 不正解。正解は **{correct_answer}** です。")

# ---------------------------
# スコア表示とリセット
# ---------------------------
st.sidebar.markdown("---")
st.sidebar.header("📊 スコア")

correct = st.session_state.score["correct"]
total = st.session_state.score["total"]
accuracy = (correct / total * 100) if total > 0 else 0
st.sidebar.write(f"✅ 正解数: {correct}")
st.sidebar.write(f"📈 出題数: {total}")
st.sidebar.write(f"🎯 正答率: {accuracy:.1f}%")

if st.sidebar.button("🔄 スコアをリセット"):
    st.session_state.score = {"correct": 0, "total": 0}
    st.success("スコアをリセットしました。")

if st.sidebar.button("🗑 単語をすべて削除"):
    st.session_state.word_dict = {}
    st.success("単語リストをすべて削除しました。")


