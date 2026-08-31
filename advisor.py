import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="qwen/qwen3.8-27b",
    max_tokens=300,
    timeout=10
)


# ---------------- STATE ----------------
class AgentState(TypedDict):
    question: str
    metrics: dict
    context: str
    reasoning: str
    answer: str


# ---------------- NODE 1: Understand ----------------
def understand_node(state: AgentState) -> AgentState:
    question = state["question"][:500]
    metrics = state["metrics"]

    prompt = f"""You are analyzing a finance question.
Question: {question}
User finances: Income ₹{metrics['income']:.0f}, Spending ₹{metrics['spending']:.0f}, Balance ₹{metrics['balance']:.0f}, Savings Rate {metrics['savings_rate']:.1f}%

Identify in one line: what financial topic is this question about?"""

    response = llm.invoke([HumanMessage(content=prompt)])
    state["reasoning"] = f"Topic: {response.content}"
    return state


# ---------------- NODE 2: Reason with CoT ----------------
def cot_node(state: AgentState) -> AgentState:
    question = state["question"][:500]
    metrics = state["metrics"]
    context = state["context"]
    reasoning = state["reasoning"]

    cot_prompt = f"""You are a personal finance advisor. Think step by step before answering.

User's financial summary:
- Income: ₹{metrics['income']:.0f}
- Spending: ₹{metrics['spending']:.0f}
- Balance: ₹{metrics['balance']:.0f}
- Savings Rate: {metrics['savings_rate']:.1f}%

Relevant transactions:
{context}

{reasoning}

Question: {question}

Think step by step:
Step 1 - What does the user's financial data tell us?
Step 2 - What do the relevant transactions show?
Step 3 - What is the best advice based on steps 1 and 2?

Final Answer (2-3 sentences, friendly tone, use ₹):"""

    response = llm.invoke([HumanMessage(content=cot_prompt)])
    state["reasoning"] += f"\nCoT reasoning completed."
    state["answer"] = response.content
    return state


# ---------------- NODE 3: Validate ----------------
def validate_node(state: AgentState) -> AgentState:
    answer = state["answer"]
    if not answer or len(answer.strip()) < 10:
        state["answer"] = "I couldn't generate a proper response. Please try rephrasing your question."
    return state


# ---------------- BUILD GRAPH ----------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("understand", understand_node)
    graph.add_node("reason", cot_node)
    graph.add_node("validate", validate_node)

    graph.set_entry_point("understand")
    graph.add_edge("understand", "reason")
    graph.add_edge("reason", "validate")
    graph.add_edge("validate", END)

    return graph.compile()


finance_graph = build_graph()


# ---------------- MAIN ADVISOR FUNCTION ----------------
def advisor(user_input: str, metrics: dict, history: list, collection=None) -> str:
    context = ""
    if collection:
        from rag import retrieve
        context = retrieve(collection, user_input)

    state = AgentState(
        question=user_input,
        metrics=metrics,
        context=context,
        reasoning="",
        answer=""
    )

    result = finance_graph.invoke(state)
    return result["answer"]
