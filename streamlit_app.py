import streamlit as st
import language_tool_python

# タイトル
st.title("📝 英文文法チェッカー")

# ユーザー入力
user_text = st.text_area("英文を入力してください", height=200, placeholder="ここに英語の長文を入力...")

# チェックボタン
if st.button("文法チェック"):
    if not user_text.strip():
        st.warning("文章を入力してください。")
    else:
        # LanguageToolを使用
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(user_text)

        # 結果表示
        if not matches:
            st.success("文法ミスは見つかりませんでした！")
        else:
            st.write(f"🔍 **{len(matches)} 件の文法/スペルの指摘があります。**")
            for i, match in enumerate(matches, 1):
                st.markdown(f"""
                **{i}. 問題のある文:**
                `{user_text[match.offset : match.offset + match.errorLength]}`

                **メッセージ:** {match.message}  
                **提案:** {", ".join(match.replacements) if match.replacements else "（提案なし）"}  
                """)

        # 修正済み文章の表示
        corrected_text = language_tool_python.utils.correct(user_text, matches)
        st.subheader("✏️ 修正提案文")
        st.code(corrected_text, language='markdown')
