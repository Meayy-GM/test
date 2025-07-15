import streamlit as st
import language_tool_python
import pandas as pd

st.set_page_config(page_title="Grammar Checker", layout="wide")
st.title("🔎 リアルタイム英文法チェッカー")

st.markdown("""
英語の文章を入力すると、リアルタイムで文法・スペルミスを検出して一覧表示します。  
LanguageTool を使用して分析しています。
""")

user_text = st.text_area(
    "英文を入力してください：", 
    height=200, 
    placeholder="ここに英文を入力すると、すぐにチェック結果が表示されます。"
)

# 入力がある場合のみ処理
if user_text.strip():
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(user_text)

    if not matches:
        st.success("✅ 文法ミスは見つかりませんでした。")
    else:
        st.warning(f"🚨 {len(matches)} 件の文法・スペルミスが見つかりました。")

        # 表示用データの作成
        issues = []
        for match in matches:
            issues.append({
                "エラー箇所": user_text[match.offset : match.offset + match.errorLength],
                "理由": match.message,
                "提案": ", ".join(match.replacements) if match.replacements else "（提案なし）"
            })

        df = pd.DataFrame(issues)
        st.dataframe(df, use_container_width=True)

        # 修正済み文章を折りたたみ表示
        corrected = language_tool_python.utils.correct(user_text, matches)
        with st.expander("✏️ 修正後の文章を表示"):
            st.code(corrected, language='markdown')
else:
    st.info("⬅ 上のテキストボックスに英語の文を入力してください。")
