import os
import sys
import streamlit as st

# Ensure the root directory is accessible so we can import the agent
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from langchain_core.messages import HumanMessage
from agent.core import research_agent
from agent.disambiguation import DisambiguationEngine

st.set_page_config(page_title="ARA-1 Dashboard", layout="wide")
st.title("📊 ARA-1 Financial Research Analyst")

st.sidebar.header("Execution Controls")
st.sidebar.markdown("Welcome to the QuantumEdge Research Terminal.")

user_query = st.text_input("Enter your financial research query:", placeholder="e.g., Produce a complete investment research report on NVIDIA Corporation.")

if st.button("Run Research"):
    if user_query:
        st.info("Initiating ARA-1 Analysis...")
        
        # Disambiguation Phase
        disambiguator = DisambiguationEngine()
        processed_query = disambiguator.process_and_ground(user_query)
        actual_query = processed_query["grounded_query"]
        
        if processed_query.get("assumptions_logged"):
            st.warning("🧠 DISAMBIGUATION TRIGGERED:")
            for assumption in processed_query["assumptions_logged"]:
                st.write(f"-> {assumption}")
            st.write(f"**Grounded Query:** {actual_query}")
            
        inputs = {"messages": [HumanMessage(content=actual_query)], "research_query": actual_query}
        
        with st.spinner("Executing Tools and Synthesizing Report..."):
            try:
                for event in research_agent.stream(inputs, stream_mode="values"):
                    pass # Streamlit can also show tool calls if we want, but keeping it simple
                
                raw_content = event["messages"][-1].content
                if isinstance(raw_content, list) and len(raw_content) > 0 and 'text' in raw_content[0]:
                    final_report = raw_content[0]['text']
                else:
                    final_report = str(raw_content)
                    
                st.success("✅ Research Complete")
                st.markdown("---")
                st.markdown(final_report)
                
            except Exception as e:
                st.error(f"Execution stopped: {str(e)}")
    else:
        st.warning("Please enter a query to begin.")