from typing import TypedDict
from langgraph.graph import StateGraph, END
from rag import (retrieve_chunks,build_context,generate_from_context,)

# Graph State
class GraphState(TypedDict):
    question: str
    matches: list
    context: str
    answer: str

# Retrieve Node
def retrieve_node(state: GraphState):
    matches = retrieve_chunks(state["question"])
    context = build_context(matches)
    return {
        "matches": matches,
        "context": context,}

# Generate Node
def generate_node(state: GraphState):
    answer = generate_from_context(
        state["question"],
        state["context"],)
    return {
        "answer": answer,
    }


# Build Graph
builder = StateGraph(GraphState)
builder.add_node("retrieve",retrieve_node)
builder.add_node("generate",generate_node)
builder.set_entry_point("retrieve")
builder.add_edge("retrieve","generate")
builder.add_edge("generate",END)
graph = builder.compile()


# Run Graph
if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (type 'exit' to quit): ")
        if question.lower() == "exit":
            break
        result = graph.invoke(
            {
                "question": question
            })

        print("\nAnswer")
        print("=" * 60)
        print(result["answer"])
        print("\nSources")
        print("=" * 60)

        for match in result["matches"]:
            print(
                f"Page {match['metadata']['page']} "
                f"(Score: {match['score']:.4f})")