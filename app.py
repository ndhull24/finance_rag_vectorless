import streamlit as st
from src.answer import generate_answer

st.set_page_config(page_title="Finance RAG Assistant", page_icon="💸")

st.title("Finance RAG – Qwen2 1.5B Assistant")
st.write("Ask questions about your finance documents. Answers are grounded in your indexed corpus.")

question = st.text_area("Your question", placeholder="e.g., What is the capitalization threshold for fixed assets?")

k = st.slider("Number of context chunks (k)", min_value=3, max_value=15, value=8, step=1)

if st.button("Get answer") and question.strip():
    with st.spinner("Thinking..."):
        try:
            answer = generate_answer(question.strip(), k=k, max_new_tokens=256)
            st.subheader("Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")