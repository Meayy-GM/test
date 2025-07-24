import streamlit as st
import pandas as pd
from gingerit.gingerit import GingerIt
import re

st.set_page_config(page_title="Grammar Checker", layout="wide")
st.title("🔎 リアルタイム英文法チェッカー")

st.markdown("""
英語の文章を入力すると、リアルタイムで文法・スペルミスを検出して一覧表示します。  
Gingerit を使用して分析しています。
""")

user_text = st.text_area(
    "英文を入力してください：", 
    height=200, 
    placeholder="ここに英文を入力すると、すぐにチェック結果が表示されます。"
)

# Gingeritのインスタンスを一度だけ作成
@st.cache_resource
def get_parser():
    return GingerIt()

parser = get_parser()

def split_long_text(text, max_length=600):
    """長い文章を短いチャンクに分割"""
    if len(text) <= max_length:
        return [text]
    
    # 文で分割を試みる
    sentences = re.split(r'[.!?]+\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk + sentence) <= max_length:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def find_differences(original, corrected):
    """原文と修正文の違いを検出"""
    if original.strip() == corrected.strip():
        return []
    
    # 簡単な単語レベルの差分検出
    original_words = original.split()
    corrected_words = corrected.split()
    
    differences = []
    
    # 長さが異なる場合や大きく変わった場合
    if len(original_words) != len(corrected_words) or original != corrected:
        differences.append({
            "エラー箇所": "文章全体",
            "理由": "文法・語法・スペルの修正",
            "提案": "修正後の文章を確認してください"
        })
    
    return differences

if user_text.strip():
    try:
        with st.spinner("文法チェック中..."):
            # 長文の場合は分割して処理
            chunks = split_long_text(user_text)
            all_issues = []
            corrected_chunks = []
            
            for chunk in chunks:
                # Gingeritで解析
                result = parser.parse(chunk)
                corrected_chunk = result.get('result', chunk)
                corrected_chunks.append(corrected_chunk)
                
                # 元のGingeritのレスポンス構造を確認
                st.write("Debug - Gingerit response:", result)  # デバッグ用（本番では削除）
                
                # 修正があった場合の差分を検出
                if chunk != corrected_chunk:
                    differences = find_differences(chunk, corrected_chunk)
                    all_issues.extend(differences)
            
            corrected_text = ' '.join(corrected_chunks)
            
            # 結果表示
            if not all_issues:
                if user_text.strip() != corrected_text.strip():
                    st.warning("🚨 文章が修正されました。")
                    all_issues = [{
                        "エラー箇所": "文章",
                        "理由": "文法・スペルが改善されました",
                        "提案": "修正後の文章を確認してください"
                    }]
                else:
                    st.success("✅ 文法ミスは見つかりませんでした。")
            else:
                st.warning(f"🚨 修正が適用されました。")
            
            if all_issues:
                df = pd.DataFrame(all_issues)
                st.dataframe(df, use_container_width=True)
            
            # 修正済み文章を表示
            with st.expander("✏️ 修正後の文章を表示"):
                st.text_area("修正後:", value=corrected_text, height=150)
                
                # 元の文章も比較のために表示
                st.text_area("元の文章:", value=user_text, height=150)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.info("以下を確認してください:")
        st.info("1. インターネット接続が正常か")
        st.info("2. 入力文章の長さ（長すぎる場合は分割して入力）")
        st.info("3. 特殊文字が含まれていないか")

else:
    st.info("⬅ 上のテキストボックスに英語の文を入力してください。")

# 使用方法の説明
with st.expander("📖 使用方法"):
    st.markdown("""
    **使い方:**
    1. 上のテキストボックスに英語の文章を入力
    2. 自動的に文法・スペルチェックが実行されます
    3. エラーがある場合は一覧表示されます
    4. 修正後の文章は折りたたみメニューで確認できます
    
    **注意:**
    - インターネット接続が必要です
    - 長い文章は自動的に分割して処理されます
    - 処理に数秒かかる場合があります
    """)