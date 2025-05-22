import streamlit as st

st.title("自己紹介")

st.write('まずは名前を教えて')

user_name = st.text_input("名前を入力してください")

st.header("あなたの名前は"+str(user_name)+"です")

