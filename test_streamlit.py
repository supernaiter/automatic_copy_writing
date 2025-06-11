import streamlit as st

st.title("テストアプリ")
st.write("Streamlit Cloud デプロイテスト成功！")
 
if st.button("テストボタン"):
    st.success("ボタンが動作しています") 