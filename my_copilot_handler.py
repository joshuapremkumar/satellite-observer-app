# my_copilot_handler.py

from copilotkit.langgraph_agent import LangGraphAgent
from langgraph.graph import Graph, StateGraph # Import Graph and StateGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI # Import ChatOpenAI for the LLM
import os # Needed to access environment variables like OPENAI_API_KEY

class CopilotKit:
    def __init__(self, assistant_name, assistant_instructions):
        # 1. Initialize the Language Model (LLM)
        # Ensure OPENAI_API_KEY is set in your environment variables.
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7) # Recommended model. Change if needed.

        # 2. Define the LangGraph workflow
        # We'll use a simple Graph for now, which directly calls the LLM.
        workflow = Graph()

        # Define a node function that interacts with the LLM
        def call_llm(state: dict) -> dict:
            """
            A node in the graph that takes the current messages, adds the system message,
            and calls the LLM.
            """
            messages = state.get("messages", [])

            # Ensure the system message is at the beginning of the conversation history
            # and only added once.
            if not any(isinstance(msg, SystemMessage) for msg in messages):
                messages.insert(0, SystemMessage(content=assistant_instructions))

            # Invoke the LLM with the messages
            ai_response = self.llm.invoke(messages)

            # Return the updated state with the new AI message
            return {"messages": messages + [ai_response]}

        # 3. Add the LLM node to the graph
        workflow.add_node("llm_interaction_node", call_llm)

        # 4. Set the entry and finish points for this simple graph
        workflow.set_entry_point("llm_interaction_node")
        workflow.set_finish_point("llm_interaction_node")

        # 5. Compile the graph
        # This prepares the graph for execution.
        # For langgraph 0.3.20, Graph.compile() should be available.
        compiled_graph = workflow.compile()

        # 6. Initialize LangGraphAgent with the compiled graph
        self.agent = LangGraphAgent(
            name=assistant_name,
            graph=compiled_graph # Provide the compiled graph object
        )

    def chat(self, prompt):
        try:
            # The input to the agent's invoke method needs to match the graph's state
            messages_input = [HumanMessage(content=prompt)]

            # Invoke the LangGraphAgent with the user's prompt
            # The agent will execute the graph we defined
            response_state = self.agent.invoke({"messages": messages_input})

            # Extract the AI's response from the final state messages
            if isinstance(response_state, dict) and "messages" in response_state:
                for msg in reversed(response_state["messages"]):
                    if isinstance(msg, AIMessage): # Look for LangChain's AIMessage object
                        return msg.content # Return the content of the AI message
                    elif isinstance(msg, dict) and msg.get("role") == "assistant": # Fallback for plain dict messages
                         return msg.get("content", "No assistant content found.")
            # If no structured AI message is found, return the raw state for debugging
            return "No structured AI response found. Raw output from agent: " + str(response_state)

        except Exception as e:
            # Provide a clear error message if the chat interaction fails
            return f"Error interacting with CopilotKit agent during chat: {e}"