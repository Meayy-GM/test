import streamlit as st
import pandas as pd
from textblob import TextBlob
import re

st.set_page_config(page_title="Grammar Checker", layout="wide")
st.title("🔎 リアルタイムスペルミスチェッカー")

st.markdown("""
英語の文章を入力すると、リアルタイムでスペルミスを検出して一覧表示します。  
TextBlob を使用して分析しています。
""")

user_text = st.text_area(
    "英文を入力してください：", 
    height=200, 
    placeholder="ここに英文を入力すると、すぐにチェック結果が表示されます。"
)

def check_with_textblob(text):
    """TextBlobを使用してスペルチェック"""
    blob = TextBlob(text)
    corrected = str(blob.correct())
    
    # 差分を検出
    original_words = text.split()
    corrected_words = corrected.split()
    
    issues = []
    
    # 単語レベルで比較
    for i, (orig, corr) in enumerate(zip(original_words, corrected_words)):
        if orig != corr:
            issues.append({
                "エラー箇所": orig,
                "理由": "スペルミス",
                "提案": corr
            })
    
    return corrected, issues

if user_text.strip():
    try:
        with st.spinner("スペルチェック中..."):
            corrected_text, issues = check_with_textblob(user_text)
            
            if not issues:
                if user_text.strip() != corrected_text.strip():
                    st.warning("🚨 文章が修正されました。")
                    issues = [{
                        "エラー箇所": "文章",
                        "理由": "スペル・語法が改善されました",
                        "提案": "修正後の文章を確認してください"
                    }]
                else:
                    st.success("✅ スペルミスは見つかりませんでした。")
            else:
                st.warning(f"🚨 {len(issues)} 件のスペルミスが見つかりました。")
            
            if issues:
                df = pd.DataFrame(issues)
                st.dataframe(df, use_container_width=True)
            
            # 修正済み文章を表示
            with st.expander("✏️ 修正後の文章を表示"):
                st.text_area("修正後:", value=corrected_text, height=150)
                st.text_area("元の文章:", value=user_text, height=150)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

else:
    st.info("⬅ 上のテキストボックスに英語の文を入力してください。")