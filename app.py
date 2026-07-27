import streamlit as st
from graph import graph

st.set_page_config(
    page_title="Agentic AI RAG Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Agentic AI RAG Chatbot")
st.write("Ask questions about the Agentic AI eBook.")

question = st.text_input(
    "Enter your question:"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()
    with st.spinner("Searching and generating answer..."):
        result = graph.invoke(
            {
                "question": question
            }
        )
    st.subheader("Answer")
    st.write(result["answer"])
    st.subheader("Sources")
    if result["matches"]:
        for match in result["matches"]:
            with st.expander(
                f"📄 Page {match['metadata']['page']} | "
                f"⭐ Score: {match['score']:.4f}"):
                st.write(match["metadata"]["text"])
    else:
        st.info("No relevant document sections were found.")