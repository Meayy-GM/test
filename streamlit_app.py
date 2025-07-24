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

if user_text.strip():
    try:
        # 長文の場合は分割して処理
        chunks = split_long_text(user_text)
        all_issues = []
        corrected_chunks = []
        
        offset = 0
        for chunk in chunks:
            result = parser.parse(chunk)
            corrected_chunks.append(result['result'])
            
            # エラー情報を抽出
            if 'corrections' in result:
                for correction in result['corrections']:
                    all_issues.append({
                        "エラー箇所": correction.get('text', ''),
                        "理由": correction.get('definition', '文法エラー'),
                        "提案": correction.get('correct', '（提案なし）')
                    })
            
            offset += len(chunk)
        
        corrected_text = ' '.join(corrected_chunks)
        
        if not all_issues:
            # 元の文章と修正後を比較して違いがあるかチェック
            if user_text.strip() != corrected_text.strip():
                st.warning("🚨 文章が修正されました。詳細な分析結果を確認してください。")
                all_issues = [{
                    "エラー箇所": "全体",
                    "理由": "文法・スペルの改善が適用されました",
                    "提案": "修正後の文章を確認してください"
                }]
            else:
                st.success("✅ 文法ミスは見つかりませんでした。")
        else:
            st.warning(f"🚨 {len(all_issues)} 件の文法・スペルミスが見つかりました。")

        if all_issues:
            df = pd.DataFrame(all_issues)
            st.dataframe(df, use_container_width=True)

        # 修正済み文章を折りたたみ表示
        if corrected_text != user_text:
            with st.expander("✏️ 修正後の文章を表示"):
                st.code(corrected_text, language='markdown')

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.info("長い文章の場合、複数回に分けて入力してみてください。")

else:
    st.info("⬅ 上のテキストボックスに英語の文を入力してください。")