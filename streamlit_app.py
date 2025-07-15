import streamlit as st
import language_tool_python

st.title("📝 英文文法チェッカー")

user_text = st.text_area(
    "英文を入力してください", 
    height=200, 
    placeholder="ここに英語の長文を入力してください..."
)

if st.button("文法チェック"):
    if not user_text.strip():
        st.warning("文章を入力してください。")
    else:
        # LanguageToolの英語用インスタンス作成
        tool = language_tool_python.LanguageTool('en-US')

        # チェック実行
        matches = tool.check(user_text)

        if not matches:
            st.success("🎉 文法ミスは見つかりませんでした！")
        else:
            st.write(f"🔍 **{len(matches)} 件の文法・スペルの問題を検出しました。**")

            for i, match in enumerate(matches, 1):
                # 問題のある文章の箇所を切り出し
                error_text = user_text[match.offset : match.offset + match.errorLength]

                st.markdown(f"""
                ### {i}. 問題のある文節
                > `{error_text}`

                **理由:** {match.message}  
                **提案される修正案:** {", ".join(match.replacements) if match.replacements else "（提案なし）"}
                ---
                """)

        # 修正後の文章
