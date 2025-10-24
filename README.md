# 🏨 Hotel Chatbot - AI-Powered Hotel Management System

A conversational hotel management system built with **LangGraph**, **FastAPI**, and **RAG** (Retrieval-Augmented Generation). Features role-based access control (RBAC) with 10 LangChain tools for guest and staff operations.

## ✨ Features

### 🤖 AI Agent Architecture
- **LangGraph** state machine for agent orchestration
- **ReAct-style** agent with tool calling
- **Conversation memory** and multi-turn interactions
- **Groq Mixtral** LLM for natural language understanding

### 🔐 Role-Based Access Control (RBAC)
- **Guest Role**: 6 tools (search, book, cancel, view bookings, room details, FAQ)
- **Staff Role**: 10 tools (all guest tools + admin operations)
- Tools loaded dynamically based on user role
- Enforced at agent-building level

### 📚 RAG-Powered FAQ System
- **ChromaDB** vector database for semantic search
- Hotel policies stored as embeddings
- Context-aware answers (no hallucinations)
- Local persistence (no cloud dependencies)

### 🛠️ 10 LangChain Tools

**Guest Tools (6):**
1. `search_rooms` - Search available rooms by type and price
2. `book_room` - Create new bookings with date validation
3. `cancel_booking` - Cancel existing bookings
4. `get_my_bookings` - View booking history
5. `get_room_details` - Get detailed room information
6. `answer_faq` - RAG-powered FAQ answering

**Staff Tools (4 additional):**
7. `get_all_bookings` - View all bookings in system
8. `get_todays_checkins` - Today's arrivals
9. `get_available_rooms_count` - Occupancy overview
10. `update_room_status` - Update room status

### 💾 Data Persistence
- **SQLite** database for rooms and bookings
- 10 sample rooms with varied pricing
- Booking conflict detection
- Local storage (no cloud setup needed)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API Key ([Get one here](https://console.groq.com/keys))

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd simple-hotel-bot
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=your_actual_groq_api_key_here
```

5. **Run the application:**

**Option A: With Streamlit UI (Recommended for Demo)**
```bash
# Start both servers automatically
python start_demo.py

# Or manually in separate terminals:
# Terminal 1:
python main.py

# Terminal 2:
streamlit run app.py
```

Streamlit App: **http://localhost:8501** 🎨

**Option B: API Only**
```bash
python main.py
```

The API will be available at: **http://localhost:8000**

API Documentation (Swagger UI): **http://localhost:8000/docs**

---

## 🎨 Streamlit Web Interface

We've built a beautiful web interface for easy demonstration!

### Features:
- � **Login Page** - Fixed credentials for guest/staff accounts
- 💬 **Real-time Chat** - Interactive conversation with the AI agent
- 👥 **Role-Based UI** - Different features based on user role
- 🛠️ **Agent Info** - See available tools in sidebar
- ⚡ **Quick Actions** - Pre-made prompts for common tasks

### Demo Credentials:
| User | Email | Password | Tools |
|------|-------|----------|-------|
| Guest | `guest@hotel.com` | `guest123` | 6 tools |
| Staff | `staff@hotel.com` | `staff123` | 10 tools |

### Quick Start:
```bash
# Start both servers
python start_demo.py

# Or use PowerShell script
.\start_demo.ps1

# Or manually
python main.py           # Terminal 1
streamlit run app.py     # Terminal 2
```

Then open: **http://localhost:8501**

See [STREAMLIT_README.md](STREAMLIT_README.md) for detailed Streamlit documentation.

---

## �📖 API Usage (For Direct API Access)

### Authentication
All endpoints (except `/rooms` and `/health`) require authentication via the `X-User-Email` header.

**Test Users:**
- `guest@hotel.com` - Guest role (6 tools)
- `staff@hotel.com` - Staff role (10 tools)

### Endpoints

#### 1. **POST /chat** - Main Chatbot Endpoint

Send messages to the AI agent. The agent will use role-specific tools to help.

**Request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: guest@hotel.com" \
  -d '{"message": "I want to book a room for next week"}'
```

**Response:**
```json
{
  "response": "I'd be happy to help you book a room! To proceed with your booking...",
  "role": "guest",
  "user_name": "Guest User"
}
```

#### 2. **GET /rooms** - List Available Rooms (Public)

Get all available rooms without authentication.

**Request:**
```bash
curl http://localhost:8000/rooms
```

**Response:**
```json
{
  "count": 8,
  "rooms": [
    {
      "id": 1,
      "room_number": "101",
      "room_type": "Single",
      "price_per_night": 80.0,
      "room_status": "available"
    },
    ...
  ]
}
```

#### 3. **GET /bookings** - Get User's Bookings

Get all bookings for the authenticated user.

**Request:**
```bash
curl http://localhost:8000/bookings \
  -H "X-User-Email: guest@hotel.com"
```

**Response:**
```json
{
  "user": "Guest User",
  "email": "guest@hotel.com",
  "count": 2,
  "bookings": [...]
}
```

#### 4. **GET /agent-info** - Get Agent Configuration

See what tools are available for your role.

**Request:**
```bash
curl http://localhost:8000/agent-info \
  -H "X-User-Email: staff@hotel.com"
```

**Response:**
```json
{
  "user": {
    "role": "staff",
    "name": "Staff Member"
  },
  "agent": {
    "role": "staff",
    "tools_count": 10,
    "tool_names": ["search_rooms", "book_room", ...]
  }
}
```

---

## 💬 Example Conversations

### Guest User Examples

**Search for rooms:**
```
User: "Show me available rooms under $200"
Bot: [Uses search_rooms tool]
     "Found 6 available rooms:
     🏨 Room 101 (Single) - $80/night
     🏨 Room 201 (Double) - $120/night
     ..."
```

**Book a room:**
```
User: "Book room 201 for me from 2024-12-20 to 2024-12-22"
Bot: [Uses book_room tool]
     "✅ Booking Confirmed!
     📋 Booking ID: 1
     🏨 Room: 201 (Double)
     📅 Check-in: 2024-12-20
     📅 Check-out: 2024-12-22
     🌙 Nights: 2
     💰 Total: $240.00"
```

**Ask about policies:**
```
User: "What time is check-in?"
Bot: [Uses answer_faq tool with RAG]
     "ℹ️ Based on our hotel policies:
     Hotel Policy: Check-in time is 2:00 PM and check-out time is 11:00 AM."
```

### Staff User Examples

**View all bookings:**
```
User: "Show me all bookings for today"
Bot: [Uses get_all_bookings tool - STAFF ONLY]
     "📋 All Bookings for 2024-12-20 (3 total):
     ✅ Booking #1
        👤 Guest: john@email.com
        🏨 Room: 201
     ..."
```

**Check today's arrivals:**
```
User: "Who's checking in today?"
Bot: [Uses get_todays_checkins tool - STAFF ONLY]
     "📋 Today's Check-ins (2024-12-20) - 2 arrival(s):
     🏨 Room 301
        👤 Guest: guest@hotel.com
     ..."
```

---

## 🏗️ Architecture

### System Flow
```
User Request → FastAPI → Authentication → Agent Builder
                                              ↓
                                    [Role-Based Tool Loading]
                                              ↓
                              ┌───────────────┴────────────────┐
                              │                                │
                         Guest Role                      Staff Role
                         (6 tools)                      (10 tools)
                              │                                │
                              └───────────┬────────────────────┘
                                          ↓
                                   LangGraph Agent
                                          ↓
                              ┌───────────┴──────────┐
                              │                      │
                         Master Node            Tool Node
                         (LLM Decision)        (Tool Execution)
                              │                      │
                              └──────────┬───────────┘
                                         ↓
                                   Response → User
```

### LangGraph State Machine
```
Entry → Master Node → Should Continue?
          ↑              ├─ Yes → Tools Node ─┐
          │              └─ No → END          │
          └────────────────────────────────────┘
```

### RAG Pipeline
```
User Question → Vector Store → Semantic Search → Top K Documents
                                                        ↓
                                                   Context
                                                        ↓
                                               LLM + Context
                                                        ↓
                                              Grounded Answer
```

---

## 📁 Project Structure

```
simple-hotel-bot/
├── main.py              # FastAPI application (150 lines)
├── agent.py             # LangGraph agent builder (120 lines)
├── tools.py             # 10 LangChain tools (300 lines)
├── database.py          # SQLite operations (120 lines)
├── auth.py              # RBAC system (80 lines)
├── vector_store.py      # ChromaDB RAG (80 lines)
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── PROJECT_PLAN.md      # Development plan
├── README.md            # This file
├── hotel.db             # SQLite database (auto-created)
└── data/
    ├── faqs.txt         # Hotel FAQ documents
    └── chroma/          # ChromaDB storage (auto-created)
```

**Total: ~850 lines of clean, documented code**

---

## 🔧 Tech Stack Details

| Technology | Purpose | Why? |
|------------|---------|------|
| **FastAPI** | REST API framework | Fast, modern, automatic docs |
| **LangGraph** | Agent orchestration | More control than LangChain agents |
| **ChromaDB** | Vector database | Local, lightweight, perfect for RAG |
| **Groq** | LLM provider | Fast inference, free tier |
| **SQLite** | Database | No setup, local, perfect for demo |
| **LangChain** | Tool framework | Standard for AI agents |

---

## 🎯 Key Design Decisions

### Why LangGraph over LangChain Agents?
- **More control**: Explicit state transitions
- **Debuggable**: Can see exact flow through nodes
- **Transparent**: No black-box ReAct logic
- **Conditional routing**: Custom logic for tool selection

### Why ChromaDB for RAG?
- **Local persistence**: No cloud dependencies
- **Easy setup**: Works out of the box
- **Good for demo**: Fast, reliable, explainable

### Why Header-Based Auth?
- **Simple**: No JWT complexity for demo
- **Clear**: Easy to test with curl/Postman
- **Interview-friendly**: Easy to explain
- **Production-ready approach**: Can upgrade to JWT later

### RBAC Enforcement
- **Framework-level**: Tools bound to LLM at agent creation
- **Not application-level**: LLM can't call tools it doesn't have
- **Secure**: No way to bypass role restrictions

---

## 🧪 Testing

### Test Guest Role (6 tools)

```bash
# Search rooms
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: guest@hotel.com" \
  -d '{"message": "Show me available rooms"}'

# Try to access staff tool (should fail gracefully)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: guest@hotel.com" \
  -d '{"message": "Show me all bookings in the system"}'
```

### Test Staff Role (10 tools)

```bash
# Access staff tool
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: staff@hotel.com" \
  -d '{"message": "Show me all bookings"}'

# Check today's check-ins
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: staff@hotel.com" \
  -d '{"message": "Who is checking in today?"}'
```

### Test RAG

```bash
# Ask FAQ question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: guest@hotel.com" \
  -d '{"message": "What are your wifi details?"}'
```

---

## 📊 Database Schema

### Rooms Table
```sql
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    room_number TEXT UNIQUE,
    room_type TEXT,
    price_per_night REAL,
    room_status TEXT DEFAULT 'available'
);
```

### Bookings Table
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    room_id INTEGER,
    room_number TEXT,
    guest_email TEXT,
    check_in_date TEXT,
    check_out_date TEXT,
    status TEXT DEFAULT 'confirmed',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```
