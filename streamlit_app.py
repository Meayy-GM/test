import streamlit as st
import pandas as pd
from transformers import pipeline
import torch
import re

st.set_page_config(page_title="Grammar Checker", layout="wide")
st.title("🔎 リアルタイム英文法チェッカー")

st.markdown("""
英語の文章を入力すると、リアルタイムで文法・スペルミスを検出して一覧表示します。  
Hugging Face Transformers を使用して分析しています。
""")

user_text = st.text_area(
    "英文を入力してください：", 
    height=200, 
    placeholder="ここに英文を入力すると、すぐにチェック結果が表示されます。"
)

# Transformersモデルを一度だけロード
@st.cache_resource
def load_grammar_model():
    try:
        # 文法修正用のモデル
        corrector = pipeline(
            "text2text-generation", 
            model="vennify/t5-base-grammar-correction",
            device=0 if torch.cuda.is_available() else -1
        )
        return corrector
    except Exception as e:
        st.error(f"モデル読み込みエラー: {str(e)}")
        return None

def split_text_into_chunks(text, max_length=400):
    """テキストを適切なサイズに分割"""
    if len(text) <= max_length:
        return [text]
    
    # 文で分割
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
    """原文と修正文の違いを見つける"""
    original_words = original.split()
    corrected_words = corrected.split()
    
    differences = []
    i, j = 0, 0
    
    while i < len(original_words) and j < len(corrected_words):
        if original_words[i] != corrected_words[j]:
            # 違いを発見
            original_phrase = original_words[i]
            corrected_phrase = corrected_words[j]
            
            # 複数単語の変更をキャッチ
            k = 1
            while (i + k < len(original_words) and 
                   j + k < len(corrected_words) and
                   ' '.join(original_words[i:i+k+1]) != ' '.join(corrected_words[j:j+k+1])):
                k += 1
            
            if k > 1:
                original_phrase = ' '.join(original_words[i:i+k])
                corrected_phrase = ' '.join(corrected_words[j:j+k])
                i += k
                j += k
            else:
                i += 1
                j += 1
            
            differences.append({
                "エラー箇所": original_phrase,
                "理由": "文法・スペル修正",
                "提案": corrected_phrase
            })
        else:
            i += 1
            j += 1
    
    return differences

# モデル読み込み
with st.spinner("モデルを読み込み中..."):
    corrector = load_grammar_model()

if user_text.strip() and corrector:
    with st.spinner("文法チェック中..."):
        try:
            # テキストを分割
            chunks = split_text_into_chunks(user_text)
            corrected_chunks = []
            all_differences = []
            
            for chunk in chunks:
                # 文法修正を実行
                result = corrector(f"grammar: {chunk}", max_length=len(chunk) + 100)
                corrected_chunk = result[0]['generated_text']
                corrected_chunks.append(corrected_chunk)
                
                # 違いを検出
                differences = find_differences(chunk, corrected_chunk)
                all_differences.extend(differences)
            
            corrected_text = ' '.join(corrected_chunks)
            
            if not all_differences:
                st.success("✅ 文法ミスは見つかりませんでした。")
            else:
                st.warning(f"🚨 {len(all_differences)} 件の文法・スペルミスが見つかりました。")
                
                df = pd.DataFrame(all_differences)
                st.dataframe(df, use_container_width=True)

            # 修正済み文章を折りたたみ表示
            if corrected_text.strip() != user_text.strip():
                with st.expander("✏️ 修正後の文章を表示"):
                    st.code(corrected_text, language='markdown')
        
        except Exception as e:
            st.error(f"処理エラー: {str(e)}")

elif user_text.strip() and not corrector:
    st.error("モデルの読み込みに失敗しました。ページを再読み込みしてください。")
else:
    st.info("⬅ 上のテキストボックスに英語の文を入力してください。")

# 必要なライブラリのインストール方法を表示
with st.expander("📋 必要なライブラリ"):
    st.code("""
pip install transformers torch pandas streamlit
    """, language='bash')