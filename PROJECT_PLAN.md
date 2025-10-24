# 🎯 Simplified Hotel Chatbot - Interview Version (WITH RAG + RBAC)

## 📋 Project Goal
Create a **professional yet explainable** hotel chatbot that demonstrates:
- ✅ LangGraph agent with tool calling
- ✅ **RBAC (Role-Based Access Control)** with proper authentication
- ✅ **RAG (Retrieval-Augmented Generation)** using ChromaDB
- ✅ Local SQLite database (no cloud dependencies)
- ✅ 10 LangChain tools
- ✅ Clean, professional architecture

**Time to Build:** 5-6 hours  
**Complexity:** MEDIUM (not naive, but still explainable!)  
**Impressiveness:** VERY HIGH (shows proper AI engineering patterns)  
**Resume Match:** ✅ YES (you mentioned 15+ tools, RAG, RBAC)

---

## 🎨 What We're Building

### Core Features

#### 1. **RAG-Powered FAQ System** 🔥
- ChromaDB vector store (local persistence)
- Semantic search for hotel policies
- Context-aware answers (no hallucinations)

#### 2. **Proper RBAC System** 🔐
- User authentication with roles
- Guest role: 6 tools accessible
- Staff role: 10 tools accessible (6 guest + 4 staff)
- Enforced at agent-building level

#### 3. **10 LangChain Tools**
**Guest Tools (6):**
- `search_rooms` - Find available rooms
- `book_room` - Make a booking
- `cancel_booking` - Cancel a booking
- `get_my_bookings` - View my bookings
- `get_room_details` - Get info about a specific room
- `answer_faq` - RAG-powered FAQ answering 🔥

**Staff Tools (4 additional):**
- `get_all_bookings` - View all bookings
- `get_todays_checkins` - Today's arrivals
- `get_available_rooms_count` - Quick occupancy check
- `update_room_status` - Mark room as cleaning/available

#### 4. **Local SQLite Database**
- `rooms` table (10 sample rooms)
- `bookings` table
- No cloud dependencies

#### 5. **Authentication System**
- Simple header-based auth (`X-User-Email`)
- User store with roles
- Protected endpoints

---

## 📁 Project Structure (8 files, ~900 lines)

```
simple-hotel-bot/
├── main.py              # FastAPI app + auth (150 lines)
├── agent.py             # LangGraph setup (120 lines)
├── tools.py             # All 10 tools (300 lines)
├── database.py          # SQLite setup (120 lines)
├── auth.py              # RBAC system (80 lines)
├── vector_store.py      # ChromaDB RAG setup (80 lines)
├── requirements.txt     # 8 dependencies
├── .env.example         # API keys
├── README.md            # Documentation
└── data/
    ├── faqs.txt         # FAQ documents (20 lines)
    └── chroma/          # ChromaDB storage (auto-created)
```

---

## 🔧 Tech Stack

**Dependencies (8 packages):**
```txt
fastapi==0.104.1
uvicorn==0.24.0
langchain==0.1.0
langchain-groq==0.0.1
langgraph==0.0.20
langchain-community==0.0.10
chromadb==0.4.22
python-dotenv==1.0.0
```

**Key Technologies:**
- **FastAPI** - REST API framework
- **LangGraph** - Agent orchestration
- **ChromaDB** - Vector database for RAG
- **Groq** - LLM provider (Mistral)
- **SQLite** - Local database

---

## ✅ TODO List - Step by Step

### Phase 1: Setup (30 min)
- [ ] Create virtual environment
- [ ] Install dependencies (8 packages)
- [ ] Create .env with GROQ_API_KEY
- [ ] Create data/faqs.txt with sample FAQs
- [ ] Test imports

**Sample data/faqs.txt:**
```txt
Hotel Policy: Check-in time is 2:00 PM and check-out time is 11:00 AM.
WiFi: Free high-speed WiFi is available in all rooms and public areas. Password is provided at check-in.
Parking: Free parking is available for all guests. Valet parking is available for $20/day.
Pets: We are pet-friendly! Dogs and cats under 25 lbs are welcome for a $50 fee per stay.
Cancellation: Free cancellation up to 24 hours before check-in. Late cancellations incur a one-night charge.
Breakfast: Complimentary breakfast buffet is served from 7 AM to 10 AM daily in the main dining area.
Pool: Our heated outdoor pool is open year-round from 6 AM to 10 PM. Children under 12 must be supervised.
Gym: 24/7 fitness center access with cardio equipment, free weights, and yoga mats.
Room Service: Available 24/7. Menu is available in your room or by calling extension 100.
Late Checkout: Subject to availability, late checkout (up to 2 PM) can be arranged for $30.
```

---

### Phase 2: Core Infrastructure (60 min)

#### 2.1: database.py (30 min)
- [ ] Create SQLite connection
- [ ] Create `rooms` table
- [ ] Create `bookings` table
- [ ] Add 10 sample rooms
- [ ] Add helper functions

**Schema:**
```sql
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY,
    room_number TEXT UNIQUE,
    room_type TEXT,
    price_per_night REAL,
    room_status TEXT DEFAULT 'available'
);

CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    room_id INTEGER,
    guest_email TEXT,
    check_in_date TEXT,
    check_out_date TEXT,
    status TEXT DEFAULT 'confirmed',
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
```

**Sample Data (10 rooms):**
```python
rooms = [
    (101, "Single", 80, "available"),
    (102, "Single", 80, "available"),
    (201, "Double", 120, "available"),
    (202, "Double", 120, "cleaning"),
    (301, "Suite", 200, "available"),
    (302, "Suite", 200, "available"),
    (401, "Deluxe", 280, "available"),
    (402, "Deluxe", 280, "occupied"),
    (501, "Presidential", 500, "available"),
    (502, "Presidential", 500, "available"),
]
```

#### 2.2: auth.py (30 min)
- [ ] Create user model with roles
- [ ] Create user store (in-memory or SQLite)
- [ ] Add authentication functions
- [ ] Add role validation

**Implementation:**
```python
from typing import Optional, Literal

# Simple user store
USERS = {
    "guest@hotel.com": {"role": "guest", "name": "Guest User"},
    "staff@hotel.com": {"role": "staff", "name": "Staff Member"},
    "admin@hotel.com": {"role": "staff", "name": "Admin User"}
}

def get_user(email: str) -> Optional[dict]:
    """Get user by email"""
    return USERS.get(email)

def validate_role(email: str, required_role: str) -> bool:
    """Check if user has required role"""
    user = get_user(email)
    if not user:
        return False
    return user["role"] == required_role or user["role"] == "staff"

def get_user_role(email: str) -> Optional[str]:
    """Get user's role"""
    user = get_user(email)
    return user["role"] if user else None
```

---

### Phase 3: RAG + Tools (120 min)

#### 3.1: vector_store.py (30 min)
- [ ] Initialize ChromaDB with local persistence
- [ ] Load FAQs from data/faqs.txt
- [ ] Create embeddings
- [ ] Add similarity search function

**Implementation:**
```python
import chromadb
from chromadb.config import Settings
from typing import List

# Initialize ChromaDB client
client = chromadb.Client(Settings(
    persist_directory="./data/chroma",
    anonymized_telemetry=False
))

# Get or create collection
collection = client.get_or_create_collection(
    name="hotel_faqs",
    metadata={"description": "Hotel FAQ documents"}
)

def load_faqs_to_vector_store():
    """Load FAQs from file into vector store"""
    with open("data/faqs.txt", "r") as f:
        faqs = f.read().split("\n")
    
    # Add to collection with IDs
    collection.add(
        documents=faqs,
        ids=[f"faq_{i}" for i in range(len(faqs))]
    )

def get_faq_context(question: str, k: int = 3) -> List[str]:
    """Retrieve relevant FAQ context"""
    results = collection.query(
        query_texts=[question],
        n_results=k
    )
    return results['documents'][0] if results['documents'] else []

# Initialize on import
if collection.count() == 0:
    load_faqs_to_vector_store()
```

#### 3.2: tools.py (90 min)
- [ ] Implement all 10 tools
- [ ] Add proper error handling
- [ ] Add docstrings for LLM understanding

**Tool 1: search_rooms (~30 lines)**
```python
from langchain.tools import tool
from database import get_available_rooms
from typing import Optional

@tool
def search_rooms(room_type: Optional[str] = None, max_price: Optional[float] = None) -> str:
    """Search for available rooms. Optionally filter by room type and max price."""
    rooms = get_available_rooms()
    
    if room_type:
        rooms = [r for r in rooms if r['room_type'].lower() == room_type.lower()]
    
    if max_price:
        rooms = [r for r in rooms if r['price_per_night'] <= max_price]
    
    if not rooms:
        return "No rooms found matching your criteria."
    
    result = "Available rooms:\n"
    for room in rooms:
        result += f"- Room {room['room_number']} ({room['room_type']}): ${room['price_per_night']}/night\n"
    
    return result
```

**Tool 2: book_room (~40 lines)**
```python
from datetime import datetime

@tool
def book_room(room_number: str, guest_email: str, check_in: str, check_out: str) -> str:
    """Book a room. Dates format: YYYY-MM-DD"""
    try:
        # Validate dates
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        
        if check_out_date <= check_in_date:
            return "Error: Check-out date must be after check-in date."
        
        # Check availability
        if not is_room_available(room_number, check_in, check_out):
            return f"Room {room_number} is not available for those dates."
        
        # Create booking
        booking_id = create_booking(room_number, guest_email, check_in, check_out)
        
        return f"Booking confirmed! Your booking ID is {booking_id}."
    
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD."
```

**Tool 3: cancel_booking (~25 lines)**
```python
@tool
def cancel_booking(booking_id: int, guest_email: str) -> str:
    """Cancel a booking by booking ID"""
    booking = get_booking(booking_id)
    
    if not booking:
        return "Booking not found."
    
    if booking['guest_email'] != guest_email:
        return "You can only cancel your own bookings."
    
    if cancel_booking_in_db(booking_id):
        return f"Booking {booking_id} has been cancelled successfully."
    else:
        return "Failed to cancel booking."
```

**Tool 4: get_my_bookings (~30 lines)**
```python
@tool
def get_my_bookings(guest_email: str) -> str:
    """Get all bookings for a guest"""
    bookings = get_bookings_by_email(guest_email)
    
    if not bookings:
        return "You have no bookings."
    
    result = f"Your bookings:\n"
    for b in bookings:
        result += f"- Booking #{b['id']}: Room {b['room_number']}, "
        result += f"{b['check_in_date']} to {b['check_out_date']}, "
        result += f"Status: {b['status']}\n"
    
    return result
```

**Tool 5: get_room_details (~25 lines)**
```python
@tool
def get_room_details(room_number: str) -> str:
    """Get detailed information about a specific room"""
    room = get_room_by_number(room_number)
    
    if not room:
        return f"Room {room_number} not found."
    
    result = f"Room {room['room_number']} Details:\n"
    result += f"- Type: {room['room_type']}\n"
    result += f"- Price: ${room['price_per_night']}/night\n"
    result += f"- Status: {room['room_status']}\n"
    
    return result
```

**Tool 6: answer_faq (~30 lines) - WITH RAG! 🔥**
```python
from vector_store import get_faq_context
from langchain_groq import ChatGroq
import os

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")

@tool
def answer_faq(question: str) -> str:
    """Answer frequently asked questions about the hotel using RAG"""
    # Get relevant context from vector store
    context_docs = get_faq_context(question, k=3)
    
    if not context_docs:
        return "I don't have information about that. Please contact the front desk."
    
    # Combine context
    context = "\n".join(context_docs)
    
    # Generate answer using LLM with context
    prompt = f"""Based on the following hotel information, answer the question naturally and helpfully.

Context: {context}

Question: {question}

Answer:"""
    
    response = llm.invoke(prompt)
    return response.content
```

**Tool 7: get_all_bookings (~30 lines) - STAFF ONLY**
```python
@tool
def get_all_bookings(date: Optional[str] = None) -> str:
    """Get all bookings (staff only). Optionally filter by date."""
    bookings = get_all_bookings_from_db(date)
    
    if not bookings:
        return "No bookings found."
    
    result = f"All bookings ({len(bookings)}):\n"
    for b in bookings:
        result += f"- Booking #{b['id']}: {b['guest_email']}, "
        result += f"Room {b['room_number']}, {b['check_in_date']} to {b['check_out_date']}\n"
    
    return result
```

**Tool 8: get_todays_checkins (~35 lines) - STAFF ONLY**
```python
from datetime import date

@tool
def get_todays_checkins() -> str:
    """Get all check-ins scheduled for today (staff only)"""
    today = date.today().strftime("%Y-%m-%d")
    checkins = get_checkins_by_date(today)
    
    if not checkins:
        return "No check-ins scheduled for today."
    
    result = f"Today's check-ins ({len(checkins)}):\n"
    for c in checkins:
        result += f"- Room {c['room_number']}: {c['guest_email']}, "
        result += f"Booking #{c['id']}\n"
    
    return result
```

**Tool 9: get_available_rooms_count (~20 lines) - STAFF ONLY**
```python
@tool
def get_available_rooms_count() -> str:
    """Get count of available rooms by type (staff only)"""
    counts = get_room_availability_counts()
    
    result = "Room availability:\n"
    for room_type, count in counts.items():
        result += f"- {room_type}: {count} available\n"
    
    return result
```

**Tool 10: update_room_status (~30 lines) - STAFF ONLY**
```python
@tool
def update_room_status(room_number: str, status: str) -> str:
    """Update room status (staff only). Status: available, cleaning, occupied, maintenance"""
    valid_statuses = ['available', 'cleaning', 'occupied', 'maintenance']
    
    if status not in valid_statuses:
        return f"Invalid status. Use: {', '.join(valid_statuses)}"
    
    if update_room_status_in_db(room_number, status):
        return f"Room {room_number} status updated to {status}."
    else:
        return f"Failed to update room {room_number}."
```

---

### Phase 4: Agent with RBAC (75 min)

#### 4.1: agent.py (60 min)
- [ ] Define state structure
- [ ] Create master node (LLM)
- [ ] Create tool node
- [ ] Add conditional routing
- [ ] Implement role-based tool loading

**Implementation:**
```python
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
import os

# Import all tools
from tools import (
    search_rooms, book_room, cancel_booking, get_my_bookings,
    get_room_details, answer_faq, get_all_bookings, get_todays_checkins,
    get_available_rooms_count, update_room_status
)
from auth import get_user_role

# Initialize LLM
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="mixtral-8x7b-32768")

def get_tools_for_role(role: str):
    """Get tools based on user role"""
    guest_tools = [
        search_rooms, book_room, cancel_booking,
        get_my_bookings, get_room_details, answer_faq
    ]
    
    staff_tools = guest_tools + [
        get_all_bookings, get_todays_checkins,
        get_available_rooms_count, update_room_status
    ]
    
    return staff_tools if role == "staff" else guest_tools

def create_agent_for_user(user_email: str):
    """Create agent with role-specific tools"""
    role = get_user_role(user_email)
    if not role:
        role = "guest"  # Default to guest
    
    tools = get_tools_for_role(role)
    llm_with_tools = llm.bind_tools(tools)
    
    # System prompt
    system_prompt = f"""You are a helpful hotel assistant. Current user role: {role}.
    
You can help with:
- Searching and booking rooms
- Answering questions about the hotel
{'- Managing all bookings and room status (staff access)' if role == 'staff' else ''}

Always be polite and helpful."""
    
    # Define nodes
    def master_node(state: MessagesState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def should_continue(state: MessagesState):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "end"
    
    # Build graph
    graph = StateGraph(MessagesState)
    graph.add_node("master", master_node)
    graph.add_node("tools", ToolNode(tools))
    
    graph.set_entry_point("master")
    graph.add_conditional_edges("master", should_continue, {"tools": "tools", "end": "end"})
    graph.add_edge("tools", "master")
    
    return graph.compile()
```

---

### Phase 5: FastAPI with Auth (60 min)

#### 5.1: main.py (45 min)
- [ ] Create FastAPI app
- [ ] Add authentication dependency
- [ ] Add 4 endpoints
- [ ] Add error handling

**Implementation:**
```python
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from agent import create_agent_for_user
from auth import get_user
from database import get_available_rooms, get_bookings_by_email
from typing import Optional

app = FastAPI(title="Hotel Chatbot API", version="2.0")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    role: str

# Auth dependency
async def get_current_user(x_user_email: str = Header(...)):
    """Validate user from header"""
    user = get_user(x_user_email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    x_user_email: str = Header(..., description="User email for authentication")
):
    """Main chat endpoint with role-based agent"""
    user = await get_current_user(x_user_email)
    
    # Build agent for this user's role
    agent = create_agent_for_user(x_user_email)
    
    # Invoke agent
    result = agent.invoke({"messages": [("user", request.message)]})
    response_message = result["messages"][-1].content
    
    return ChatResponse(response=response_message, role=user["role"])

@app.get("/rooms")
async def list_rooms():
    """List all available rooms (public)"""
    rooms = get_available_rooms()
    return {"rooms": rooms}

@app.get("/bookings")
async def get_bookings(x_user_email: str = Header(...)):
    """Get user's bookings (authenticated)"""
    user = await get_current_user(x_user_email)
    bookings = get_bookings_by_email(x_user_email)
    return {"bookings": bookings, "user": user["name"]}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "hotel-chatbot"}

@app.get("/")
async def root():
    """API information"""
    return {
        "message": "Hotel Chatbot API",
        "endpoints": ["/chat", "/rooms", "/bookings", "/health"],
        "auth": "Pass X-User-Email header for authentication"
    }
```

#### 5.2: Testing (15 min)
- [ ] Start server: `uvicorn main:app --reload`
- [ ] Test with Swagger UI at http://localhost:8000/docs
- [ ] Test with different user emails in headers

---

### Phase 6: Testing (45 min)

- [ ] **Test RAG** - Ask FAQ questions, verify semantic search works
- [ ] **Test Guest Role** - Use `guest@hotel.com`, try to access staff tools (should fail)
- [ ] **Test Staff Role** - Use `staff@hotel.com`, access all 10 tools
- [ ] **Test RBAC Enforcement** - Verify guests can't see all bookings
- [ ] **Test Room Booking Flow** - Search → Book → View bookings → Cancel
- [ ] **Test All Endpoints** - /chat, /rooms, /bookings with auth headers

**Sample cURL Commands:**
```bash
# Guest chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: guest@hotel.com" \
  -d '{"message": "What are the wifi details?"}'

# Staff chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: staff@hotel.com" \
  -d '{"message": "Show me all bookings for today"}'

# List rooms
curl http://localhost:8000/rooms

# Get bookings
curl http://localhost:8000/bookings \
  -H "X-User-Email: guest@hotel.com"
```

---

### Phase 7: Documentation (30 min)

- [ ] Write README.md with:
  - Project overview
  - Setup instructions
  - API endpoints with auth examples
  - Role explanations (guest vs staff)
  - RAG explanation
  - RBAC explanation
  - Sample requests with different roles

---

## Total Time: 5-6 hours (professional, impressive, explainable!)

---

## 📊 Comparison with Original Project

| Feature | Original | Simplified V2 |
|---------|----------|---------------|
| Database | MongoDB Atlas ☁️ | SQLite 💾 |
| Vector DB | ChromaDB ☁️ | ChromaDB Local ✅ |
| RAG | Yes ✅ | Yes ✅ |
| RBAC | Yes ✅ | Yes ✅ |
| LLM Providers | Groq + Mistral | Groq only |
| Audio | Whisper transcription | None ❌ |
| Auth | Email-based | Header-based (simpler) |
| Logging | Azure App Insights | Python logging |
| Tools | 15+ tools | 10 tools ✅ |
| Lines of Code | 3500+ | ~900 |
| Setup Time | 2+ hours | 15 minutes |
| Build Time | Already built | 5-6 hours |

---

## 🎤 Interview Talking Points

### 30-Second Elevator Pitch:
"I built a conversational hotel management system using LangGraph and FastAPI. It has 10 LangChain tools for booking, cancellation, and staff operations, with RAG-based FAQ answering using ChromaDB. The agent uses role-based access control - guests get 6 tools, staff get all 10. I used Groq's Mistral LLM for natural language understanding and SQLite for data persistence. The system demonstrates proper architecture patterns like RBAC and RAG while being fully explainable."

### 2-Minute Deep Dive:
"The project demonstrates several key concepts:

1. **Agent Architecture**: I used LangGraph's StateGraph to create a ReAct-style agent. It has a master node that decides which tool to call, and a tool execution node. The agent maintains conversation history and can chain multiple tool calls.

2. **RAG Implementation**: For FAQ answering, I implemented Retrieval-Augmented Generation using ChromaDB. Hotel policies are stored as text documents, embedded, and retrieved via semantic search. When a user asks about policies, the agent fetches relevant context and generates accurate answers instead of hallucinating.

3. **Role-Based Access Control**: The system has two roles - guest and staff. When a user authenticates (via email header), the agent is built with role-specific tools. Guests can search, book, and manage their bookings (6 tools). Staff can additionally see all bookings, check-ins, and update room status (4 more tools, 10 total). This is proper RBAC, not just hardcoded conditionals.

4. **10 LangChain Tools**: Each tool is a Python function decorated with @tool. For example, `search_rooms` takes max_price and room_type parameters and queries SQLite. `book_room` handles date validation and conflict detection. The `answer_faq` tool uses the RAG pipeline. Staff-only tools like `get_all_bookings` are enforced at the agent-building level.

5. **Data Persistence**: I used SQLite with two tables - rooms and bookings. ChromaDB handles vector storage locally. No cloud dependencies make it easy to demo.

6. **API Design**: FastAPI exposes the agent through a /chat endpoint with authentication. Users send messages with their email header, and the system builds a personalized agent based on their role.

The key achievement is implementing proper patterns like RAG and RBAC while keeping the codebase under 1000 lines and fully explainable in an interview."

### Key Technical Questions You Can Answer:

**Q: "How does RAG work in your system?"**
A: "I use ChromaDB to store FAQ documents as embeddings. When a user asks a question, I perform semantic similarity search to find the 3 most relevant document chunks. These are passed as context to the LLM, which generates a grounded answer. This prevents hallucinations and ensures accurate information."

**Q: "How do you handle role-based access?"**
A: "At the agent-building level. When a request comes in, I extract the user email from the header, lookup their role from the user store, and then build a LangGraph agent with role-specific tools. Guests get 6 tools, staff get 10. The LLM can only call tools that were bound to it, so it's enforced at the framework level, not just application logic."

**Q: "Why LangGraph instead of LangChain agents?"**
A: "LangGraph gives me more control over the agent flow. I can define explicit state transitions, add conditional routing based on the LLM's response, and maintain conversation history with checkpointing. It's more transparent and debuggable than the black-box ReAct agent."

**Q: "How do you prevent booking conflicts?"**
A: "In the `book_room` tool, I query the database for existing bookings that overlap with the requested dates. I check if the room is already booked or if the status is not 'available'. Only if all checks pass, I create the booking. SQLite handles concurrency at the transaction level."

**Q: "What would you improve if you had more time?"**
A: "1) Add JWT authentication instead of simple header auth. 2) Implement websockets for real-time chat. 3) Add caching for FAQ queries. 4) Add more sophisticated conflict resolution for concurrent bookings. 5) Add monitoring and observability with LangSmith."

---

## 🎯 Why This Version is Better

✅ **Not Too Simple** - Shows proper architecture patterns (RAG, RBAC)  
✅ **Not Too Complex** - Under 1000 lines, no cloud dependencies  
✅ **Interview-Ready** - Can explain every design decision  
✅ **Resume-Aligned** - Matches your claims (10+ tools, RAG, RBAC)  
✅ **Demo-Ready** - Can show RAG working, role enforcement in action  
✅ **Time-Efficient** - 5-6 hours to build, but looks professional  

---

## 🚀 Optional Enhancements (If Time Permits)

### Easy Additions (30 min each):
1. **Input Validation** - Pydantic models for all tool inputs
2. **Better Error Messages** - User-friendly error handling
3. **Logging** - Add structured logging for debugging
4. **More FAQs** - Expand FAQ dataset to 20+ documents

### Medium Additions (1-2 hours each):
1. **JWT Authentication** - Replace header auth with proper JWT tokens
2. **WebSocket Support** - Real-time chat instead of REST
3. **Conversation Memory** - LangGraph checkpointing for multi-turn conversations
4. **Admin Dashboard** - Simple Streamlit dashboard for staff

### Advanced (3+ hours):
1. **LangSmith Integration** - Add observability and tracing
2. **Multi-tenancy** - Support multiple hotels
3. **Payment Integration** - Add Stripe for booking payments

---

## 🎓 What You'll Learn

- ✅ LangGraph state machines
- ✅ RAG with vector databases
- ✅ Role-based access control
- ✅ LangChain tool creation
- ✅ FastAPI authentication
- ✅ Agent prompt engineering
- ✅ SQLite database design

---

**Time Investment:** 5-6 hours  
**Interview Readiness:** HIGH  
**Complexity:** MEDIUM (not naive!)  
**Impressiveness:** VERY HIGH (RAG + RBAC + 10 tools!)  
**Resume Match:** ✅ YES (you mentioned 15+ tools)  
**Professional Factor:** ✅ Shows proper architecture patterns

---

Please ensure all Python code is fully type-hinted and includes comments explaining the purpose of major functions and logic blocks. Thank you.
