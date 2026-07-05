import sys
import os

# ---------------------------------------------------------
# 1. DYNAMIC PATH INJECTION
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# ---------------------------------------------------------
# 2. STANDARD IMPORTS
# ---------------------------------------------------------
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from tools.tool_registry import get_all_tools
from dotenv import load_dotenv
import operator

load_dotenv()

# 3. Simplified State
class ResearchState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_query: str

# 4. Initialize Groq
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0  
)

tools = [t for t in get_all_tools() if t.name != "report_generator"]
llm_with_tools = llm.bind_tools(tools)

# ---------------------------------------------------------
# 5. LINEAR NODES
# ---------------------------------------------------------
def planner(state: ResearchState):
    """NODE 1: Reads the query and fires off all necessary tools at once."""
    messages = state["messages"]
    system_prompt = (
        "ROLE: You are ARA-1, an autonomous financial research agent.\n"
        "TASK: Call the necessary tools to gather data for the user's query.\n"
        "You can batch multiple tools at once (e.g., call company_profile, financial_data, and web_search simultaneously)."
    )
    response = llm_with_tools.invoke([SystemMessage(content=system_prompt)] + messages)
    return {"messages": [response]}

def should_run_tools(state: ResearchState) -> str:
    """ROUTER: Checks if tools were requested. If not, skips to synthesis."""
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"🔧 ARA-1 Action -> Executing Tools: {[t['name'] for t in last_message.tool_calls]}")
        return "tools"
    return "synthesize"

def synthesizer(state: ResearchState):
    """NODE 3: Flattens tool outputs into clean text and writes the final report."""
    messages = state["messages"]
    
    context_text = ""
    for msg in messages:
        if msg.type == "human":
            context_text += f"Research Objective: {msg.content}\n\n"
        elif msg.type == "tool":
            context_text += f"[Source: {msg.name or 'Financial Tool'}] \nObservation Data:\n{msg.content}\n\n"
            
    system_prompt = (
        "ROLE: You are ARA-1, a senior investment research analyst at QuantumEdge Research.\n"
        "TASK: Review the gathered financial data observations below and compile a comprehensive, "
        "publication-grade investment research report. Use professional Markdown headers, clear sections, "
        "and analytical text. Ensure all specific metrics and numbers from the observations are explicitly included."
    )
    
    user_prompt = f"GATHERED OBSERVATIONS:\n{context_text}\n\nPlease generate the complete report now based strictly on these facts:"
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    print("\n✅ ARA-1 has successfully compiled the final report.")
    return {"messages": [response]}

# ---------------------------------------------------------
# 6. BUILD THE STRICT LINEAR GRAPH
# ---------------------------------------------------------
workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner)
workflow.add_node("tools", ToolNode(tools))
workflow.add_node("synthesize", synthesizer)

workflow.set_entry_point("planner")
workflow.add_conditional_edges("planner", should_run_tools, {"tools": "tools", "synthesize": "synthesize"})
workflow.add_edge("tools", "synthesize")
workflow.add_edge("synthesize", END)

research_agent = workflow.compile()