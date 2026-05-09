import streamlit as st
from src.answer import generate_answer

st.set_page_config(page_title="Finance RAG Assistant", page_icon="💸")

st.title("Finance RAG – Qwen2 0.5B Assistant")
st.write("Ask questions about your finance documents. Answers are grounded in your indexed corpus.")

question = st.text_area("Your question", placeholder="e.g., What is the capitalization threshold for fixed assets?")
k = st.slider("Number of context chunks (k)", min_value=3, max_value=15, value=8, step=1)

if st.button("Get answer") and question.strip():
    with st.spinner("Thinking..."):
        answer, metrics = generate_answer(question.strip(), k=k, max_new_tokens=128)

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total time (s)", f"{metrics['total_time']:.2f}")
    col2.metric("Retrieval (s)", f"{metrics['retrieval_time']:.2f}")
    col3.metric("Generation (s)", f"{metrics['generation_time']:.2f}")

    col4, col5 = st.columns(2)
    col4.metric("Context chunks", metrics["num_context_chunks"])
    col5.metric("Context length (chars)", metrics["context_chars"])