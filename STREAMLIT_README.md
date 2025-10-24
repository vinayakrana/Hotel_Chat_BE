# 🎨 Streamlit Demo Application

A beautiful web interface for the Hotel Chatbot with login and role-based chat.

## ✨ Features

- 🔐 **Login Page** - Fixed credentials for demo users
- 💬 **Chat Interface** - Real-time conversations with the AI agent
- 👥 **Role-Based Access** - Different tools for guests and staff
- 🛠️ **Agent Info Sidebar** - See available tools for your role
- ⚡ **Quick Actions** - Pre-made prompts for common tasks
- 📜 **Chat History** - View conversation history
- 🎨 **Modern UI** - Clean, professional design

---

## 🚀 Quick Start

### 1. Install Streamlit Dependencies

If you haven't already installed dependencies:
```bash
pip install -r requirements.txt
```

### 2. Start the API Server

In one terminal:
```bash
python main.py
```

The API should be running at `http://localhost:8000`

### 3. Start the Streamlit App

In another terminal:
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 👥 Demo Credentials

### Guest Accounts (6 tools)
```
Email: guest@hotel.com
Password: guest123

Email: john@email.com  
Password: john123
```

**Guest Capabilities:**
- 🔍 Search rooms
- 📅 Book rooms
- ❌ Cancel bookings
- 📋 View their bookings
- 🏨 Get room details
- ❓ Ask FAQs

### Staff Accounts (10 tools)
```
Email: staff@hotel.com
Password: staff123

Email: admin@hotel.com
Password: admin123
```

**Staff Capabilities:**
- All guest features +
- 📊 View all bookings
- 🚪 Check today's check-ins
- 📈 Check room availability
- 🔧 Update room status

---

## 🎯 How to Use

### 1. **Login**
- Select a user from the dropdown
- Enter the password (shown in dropdown)
- Click "🔐 Login"

### 2. **Chat**
- Type your message in the input box
- Or click a quick action button in the sidebar
- The agent will respond based on your role

### 3. **View Agent Info**
- Check the sidebar to see available tools
- Different tools appear based on your role

### 4. **Try Different Roles**
- Logout and login as different users
- See how the agent behaves differently

---

## 💡 Example Conversations

### As Guest:
```
You: "Show me available rooms under $200"
Bot: [Lists rooms with prices]

You: "Book room 201 for 2024-12-20 to 2024-12-22"
Bot: [Creates booking and shows confirmation]

You: "What time is checkout?"
Bot: [Uses RAG to answer from FAQ]
```

### As Staff:
```
You: "Show me all bookings"
Bot: [Lists all bookings in system]

You: "Who's checking in today?"
Bot: [Shows today's arrivals]

You: "Update room 101 status to cleaning"
Bot: [Updates room status]
```

---

## 🎨 Features Overview

### Login Page
- User selection dropdown
- Password input
- API health check indicator
- Demo credentials display

### Chat Interface
- Real-time messaging
- Chat history with timestamps
- User/Bot avatars
- Message input with send button

### Sidebar
- Agent information (role, tool count)
- Available tools list
- Quick action buttons
- Clear chat button

---

## 🔧 Architecture

```
Streamlit App (Port 8501)
       ↓
   HTTP Requests
       ↓
FastAPI Server (Port 8000)
       ↓
LangGraph Agent
       ↓
Tools (based on role)
```

---

## 🐛 Troubleshooting

### "API Offline" Error
**Problem:** Red dot showing API is offline

**Solution:** Make sure the FastAPI server is running:
```bash
python main.py
```

### "Connection Error"
**Problem:** Can't connect to API

**Solutions:**
1. Check if API is running: `http://localhost:8000/health`
2. Check if port 8000 is not blocked
3. Restart the API server

### Streamlit Won't Start
**Problem:** `streamlit: command not found`

**Solution:** Install streamlit:
```bash
pip install streamlit
```

### Chat Not Responding
**Problem:** Messages not getting responses

**Solutions:**
1. Check API logs for errors
2. Verify Groq API key is set in .env
3. Check if ChromaDB initialized properly

---

## 📱 UI Components

### Header
- Title
- User badge with role
- Logout button

### Sidebar
- Agent configuration
- Available tools
- Quick actions
- Clear chat

### Main Area
- Chat history
- Message input
- Send button
- Welcome message

---

## 🎯 Quick Actions

### Guest Quick Actions:
- "Show me available rooms"
- "What rooms are under $200?"
- "What time is checkout?"
- "Show me my bookings"
- "Tell me about WiFi"

### Staff Quick Actions:
- "Show me all bookings"
- "Who's checking in today?"
- "How many rooms are available?"
- "Show available rooms"
- "Update room 101 status to cleaning"

---

## 🚀 Running Both Servers

### Option 1: Two Terminals (Recommended)

**Terminal 1 - API:**
```bash
cd simple-hotel-bot
python main.py
```

**Terminal 2 - Streamlit:**
```bash
cd simple-hotel-bot
streamlit run app.py
```

### Option 2: Using Background Process (Windows)

```powershell
# Start API in background
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden

# Start Streamlit
streamlit run app.py
```

---

## 📊 Session State Management

The app uses Streamlit's session state to track:
- `logged_in` - Authentication status
- `user_email` - Current user's email
- `user_name` - Current user's name
- `user_role` - Current user's role (guest/staff)
- `chat_history` - List of all messages
- `agent_info` - Agent configuration data

---

## 🎨 Customization

### Change Colors
Edit the CSS in `app.py`:
```python
st.markdown("""
    <style>
    .stButton>button {
        background-color: #your-color;
    }
    </style>
""", unsafe_allow_html=True)
```

### Add More Quick Actions
Edit the `quick_actions` list in `chat_page()`:
```python
quick_actions = [
    "Your custom action here",
    "Another action",
]
```

### Change Page Layout
Modify `st.set_page_config()`:
```python
st.set_page_config(
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

---

## 📝 Tips for Demo

1. **Start with Guest Login** - Show basic features first
2. **Try Quick Actions** - Demonstrate common use cases
3. **Switch to Staff** - Show role-based access control
4. **Show Sidebar** - Point out available tools difference
5. **Try RAG** - Ask policy questions to show semantic search

---

## 🎉 Interview Talking Points

When demonstrating this app:

1. **"Built a full-stack demo"** - FastAPI backend + Streamlit frontend
2. **"Role-based UI"** - Different quick actions for different roles
3. **"Real-time chat"** - Instant responses from LangGraph agent
4. **"Session management"** - Streamlit state for user sessions
5. **"Professional UI"** - Clean, modern interface

---

**Enjoy your interactive hotel chatbot demo!** 🎉
