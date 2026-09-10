import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from fcot import FinancialCoTEngine

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="qwen/qwen3.8-27b",
    max_tokens=300,
    timeout=10
)

# MemorySaver for persistent cross-session context
memory = MemorySaver()


# ---------------- STATE ----------------
class AgentState(TypedDict):
    question: str
    metrics: dict
    context: str
    topic: str
    fcot_prompt: str
    answer: str
    should_retry: bool


# ---------------- NODE 1: Understand (ReAct - Reason) ----------------
def understand_node(state: AgentState) -> AgentState:
    question = state["question"][:500]
    metrics = state["metrics"]

    prompt = f"""Identify the financial topic of this question in 5 words or less.
Question: {question}
Finances: Income ₹{metrics['income']:.0f}, Spending ₹{metrics['spending']:.0f}, Savings Rate {metrics['savings_rate']:.1f}%
Topic:"""

    response = llm.invoke([HumanMessage(content=prompt)])
    state["topic"] = response.content.strip()
    return state


# ---------------- NODE 2: F-CoT Reasoning (ReAct - Act) ----------------
def fcot_node(state: AgentState) -> AgentState:
    engine = FinancialCoTEngine(state["metrics"], state["context"])
    state["fcot_prompt"] = engine.build_prompt(state["question"][:500])
    return state


# ---------------- NODE 3: Generate Answer (ReAct - Observe) ----------------
def generate_node(state: AgentState) -> AgentState:
    response = llm.invoke([HumanMessage(content=state["fcot_prompt"])])
    state["answer"] = response.content
    state["should_retry"] = False
    return state


# ---------------- NODE 4: Validate ----------------
def validate_node(state: AgentState) -> AgentState:
    if not state["answer"] or len(state["answer"].strip()) < 10:
        state["should_retry"] = True
    return state


# ---------------- CONDITIONAL EDGE (ReAct loop) ----------------
def should_retry(state: AgentState) -> str:
    if state.get("should_retry"):
        return "generate"
    return END


# ---------------- BUILD REACT GRAPH ----------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("understand", understand_node)
    graph.add_node("fcot", fcot_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)

    graph.set_entry_point("understand")
    graph.add_edge("understand", "fcot")
    graph.add_edge("fcot", "generate")
    graph.add_edge("generate", "validate")
    graph.add_conditional_edges("validate", should_retry)

    return graph.compile(checkpointer=memory)


finance_graph = build_graph()


# ---------------- MAIN ADVISOR FUNCTION ----------------
def advisor(user_input: str, metrics: dict, history: list, collection=None, session_id: str = "default") -> str:
    context = ""
    if collection:
        from rag import retrieve
        context = retrieve(collection, user_input)

    state = AgentState(
        question=user_input,
        metrics=metrics,
        context=context,
        topic="",
        fcot_prompt="",
        answer="",
        should_retry=False
    )

    # MemorySaver uses thread_id for persistent cross-session context
    config = {"configurable": {"thread_id": session_id}}
    result = finance_graph.invoke(state, config=config)
    return result["answer"]
