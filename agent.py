"""
LangGraph Agent with Role-Based Tool Access
Creates different agents based on user roles
"""
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, BaseMessage
import operator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import tools
from tools import (
    # Guest tools
    search_rooms,
    book_room,
    cancel_booking,
    get_my_bookings,
    get_room_details,
    answer_faq,
    # Staff tools
    get_all_bookings,
    get_todays_checkins,
    get_available_rooms_count,
    update_room_status
)

# Define state for our agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Import auth
from auth import get_user_role

# Initialize LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7
)


def get_tools_for_role(role: str):
    """
    Get tools based on user role (RBAC enforcement)
    
    Args:
        role: User role ('guest' or 'staff')
        
    Returns:
        List of tools available to the role
    """
    # Guest tools (6 tools)
    guest_tools = [
        search_rooms,
        book_room,
        cancel_booking,
        get_my_bookings,
        get_room_details,
        answer_faq
    ]
    
    # Staff gets all guest tools + 4 additional staff tools (10 total)
    staff_tools = guest_tools + [
        get_all_bookings,
        get_todays_checkins,
        get_available_rooms_count,
        update_room_status
    ]
    
    return staff_tools if role == "staff" else guest_tools


def get_system_prompt(role: str, user_name: str) -> str:
    """
    Get system prompt based on user role
    
    Args:
        role: User role
        user_name: User's name
        
    Returns:
        System prompt string
    """
    base_prompt = f"""You are a helpful hotel assistant chatbot. You are currently assisting {user_name} (Role: {role.upper()}).

Your capabilities:
- Search and provide information about available rooms
- Help with booking rooms (create new bookings)
- Cancel existing bookings
- Check booking status and history
- Answer questions about hotel policies and amenities

Important guidelines:
- Always be polite, professional, and helpful
- When booking rooms, always confirm dates and room details
- For cancellations, verify the booking ID
- When asked about policies, use the answer_faq tool to get accurate information
- If you're not sure about something, ask for clarification
- Always provide booking IDs after successful bookings
"""

    if role == "staff":
        base_prompt += """
Additional Staff Capabilities:
- View all bookings in the system
- Check today's check-ins and arrivals
- Monitor room availability across all room types
- Update room status (available, cleaning, occupied, maintenance)

Use these staff tools to help manage hotel operations efficiently.
"""
    
    return base_prompt


def create_agent_for_user(user_email: str):
    """
    Create a LangGraph agent with role-specific tools
    
    Args:
        user_email: User's email address
        
    Returns:
        Compiled LangGraph agent
    """
    from auth import get_user
    
    # Get user info
    user = get_user(user_email)
    if not user:
        # Default to guest role if user not found
        role = "guest"
        user_name = "Guest"
    else:
        role = user['role']
        user_name = user['name']
    
    # Get role-specific tools
    tools = get_tools_for_role(role)
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)
    
    # Get system prompt
    system_prompt = get_system_prompt(role, user_name)
    
    # Define master node (LLM decision maker)
    def master_node(state: AgentState):
        """
        Master node that decides what to do next
        Either calls a tool or responds to the user
        """
        messages = state["messages"]
        
        # Add system prompt as first message if not present
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
        
        # Get LLM response
        response = llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    # Define conditional edge function
    def should_continue(state: AgentState):
        """
        Determine if we should continue to tools or end
        """
        last_message = state["messages"][-1]
        
        # If there are tool calls, continue to tools node
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        
        # Otherwise, end the conversation
        return END
    
    # Build the graph
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("master", master_node)
    graph.add_node("tools", ToolNode(tools))
    
    # Set entry point
    graph.add_edge(START, "master")
    
    # Add edges
    graph.add_conditional_edges(
        "master",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # After tool execution, go back to master
    graph.add_edge("tools", "master")
    
    # Compile and return
    return graph.compile()


def get_agent_info(user_email: str) -> dict:
    """
    Get information about what agent would be created for a user
    Useful for debugging and testing
    
    Args:
        user_email: User's email
        
    Returns:
        Dict with role, tools count, and tool names
    """
    from auth import get_user
    
    user = get_user(user_email)
    if not user:
        role = "guest"
        user_name = "Guest"
    else:
        role = user['role']
        user_name = user['name']
    
    tools = get_tools_for_role(role)
    
    return {
        "user_name": user_name,
        "role": role,
        "tools_count": len(tools),
        "tool_names": [tool.name for tool in tools]
    }
