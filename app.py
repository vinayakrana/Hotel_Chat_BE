"""
Streamlit Demo Application for Hotel Chatbot
Features:
- Login page with fixed credentials
- Role-based chat interface
- Real-time agent responses
- Chat history
"""
import streamlit as st
import requests
from datetime import datetime
import json

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Fixed credentials for demo
DEMO_USERS = {
    "guest@hotel.com": {
        "password": "guest123",
        "role": "guest",
        "name": "Guest User"
    },
    "staff@hotel.com": {
        "password": "staff123",
        "role": "staff",
        "name": "Staff Member"
    },
    "john@email.com": {
        "password": "john123",
        "role": "guest",
        "name": "John Doe"
    },
    "admin@hotel.com": {
        "password": "admin123",
        "role": "staff",
        "name": "Admin User"
    }
}


def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'agent_info' not in st.session_state:
        st.session_state.agent_info = None


def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_agent_info(email):
    """Get agent configuration for user"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/agent-info",
            headers={"X-User-Email": email},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def send_message(email, message):
    """Send message to chatbot API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            headers={
                "Content-Type": "application/json",
                "X-User-Email": email
            },
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "response": f"Error: {response.status_code} - {response.text}",
                "role": "error",
                "user_name": "System"
            }
    except Exception as e:
        return {
            "response": f"Connection error: {str(e)}",
            "role": "error",
            "user_name": "System"
        }


def login_page():
    """Display login page"""
    st.title("🏨 Hotel Chatbot Login")
    st.markdown("---")
    
    # Check API health
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Please login to continue")
    with col2:
        if check_api_health():
            st.success("🟢 API Online")
        else:
            st.error("🔴 API Offline")
            st.warning("Please start the API server first:\n```python main.py```")
            return
    
    # Login form
    with st.form("login_form"):
        email = st.selectbox(
            "Select User",
            options=list(DEMO_USERS.keys()),
            format_func=lambda x: f"{DEMO_USERS[x]['name']} ({DEMO_USERS[x]['role'].upper()}) - {x}"
        )
        
        password = st.text_input("Password", type="password")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
        with col2:
            if st.form_submit_button("❓ Help", use_container_width=True):
                st.info("Use the credentials shown in the dropdown")
        
        if submit:
            if email in DEMO_USERS and password == DEMO_USERS[email]["password"]:
                # Successful login
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = DEMO_USERS[email]["name"]
                st.session_state.user_role = DEMO_USERS[email]["role"]
                st.session_state.chat_history = []
                
                # Get agent info
                st.session_state.agent_info = get_agent_info(email)
                
                st.success(f"✅ Welcome, {DEMO_USERS[email]['name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials!")
    
    # Demo credentials
    st.markdown("---")
    st.subheader("📝 Demo Credentials")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Guest Accounts:**")
        st.code("guest@hotel.com / guest123")
        st.code("john@email.com / john123")
        st.caption("🔹 Access: 6 tools (search, book, cancel, etc.)")
    
    with col2:
        st.markdown("**Staff Accounts:**")
        st.code("staff@hotel.com / staff123")
        st.code("admin@hotel.com / admin123")
        st.caption("🔸 Access: 10 tools (all guest + admin tools)")


def chat_page():
    """Display chat interface"""
    # Header
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.title("🏨 Hotel Chatbot")
    
    with col2:
        role_emoji = "👤" if st.session_state.user_role == "guest" else "👨‍💼"
        role_badge = f"{role_emoji} {st.session_state.user_name} ({st.session_state.user_role.upper()})"
        st.markdown(f"### {role_badge}")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.session_state.user_role = None
            st.session_state.chat_history = []
            st.session_state.agent_info = None
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar with agent info
    with st.sidebar:
        st.header("🤖 Agent Information")
        
        if st.session_state.agent_info:
            agent_data = st.session_state.agent_info.get("agent", {})
            
            st.metric("Role", agent_data.get("role", "unknown").upper())
            st.metric("Available Tools", agent_data.get("tools_count", 0))
            
            with st.expander("🛠️ Available Tools"):
                tools = agent_data.get("tool_names", [])
                for i, tool in enumerate(tools, 1):
                    st.write(f"{i}. `{tool}`")
        
        st.markdown("---")
        
        st.header("💡 Quick Actions")
        
        if st.session_state.user_role == "guest":
            quick_actions = [
                "Show me available rooms",
                "What rooms are under $200?",
                "What time is checkout?",
                "Show me my bookings",
                "Tell me about WiFi"
            ]
        else:
            quick_actions = [
                "Show me all bookings",
                "Who's checking in today?",
                "How many rooms are available?",
                "Show available rooms",
                "Update room 101 status to cleaning"
            ]
        
        for action in quick_actions:
            if st.button(action, key=action, use_container_width=True):
                # Add to chat history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": action,
                    "timestamp": datetime.now()
                })
                
                # Get response
                with st.spinner("🤔 Thinking..."):
                    response_data = send_message(st.session_state.user_email, action)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response_data.get("response", "No response"),
                        "timestamp": datetime.now()
                    })
                
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
                    st.caption(message["timestamp"].strftime("%H:%M:%S"))
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
                    st.caption(message["timestamp"].strftime("%H:%M:%S"))
    
    # Chat input
    st.markdown("---")
    
    # Use columns for better layout
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="Ask about rooms, bookings, or hotel policies...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 Send", use_container_width=True, type="primary")
    
    if send_button and user_input:
        # Add user message to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Get bot response
        with st.spinner("🤔 Thinking..."):
            response_data = send_message(st.session_state.user_email, user_input)
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response_data.get("response", "No response"),
                "timestamp": datetime.now()
            })
        
        # Clear input and refresh
        st.rerun()
    
    # Welcome message if no chat history
    if not st.session_state.chat_history:
        st.info("👋 Welcome! I'm your hotel assistant. How can I help you today?")
        
        if st.session_state.user_role == "guest":
            st.markdown("""
            **I can help you with:**
            - 🔍 Search for available rooms
            - 📅 Book a room
            - ❌ Cancel bookings
            - 📋 View your bookings
            - 🏨 Get room details
            - ❓ Answer questions about hotel policies
            """)
        else:
            st.markdown("""
            **I can help you with:**
            - 📊 View all bookings
            - 🚪 Check today's arrivals
            - 📈 Check room availability
            - 🔧 Update room status
            - Plus all guest features!
            """)


def main():
    """Main application"""
    # Page config
    st.set_page_config(
        page_title="Hotel Chatbot",
        page_icon="🏨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 8px;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Show appropriate page
    if not st.session_state.logged_in:
        login_page()
    else:
        chat_page()


if __name__ == "__main__":
    main()
