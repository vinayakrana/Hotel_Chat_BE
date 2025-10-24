# 🎨 Streamlit App - Visual Guide

## 📸 What You'll See

### 1. Login Page 🔐

```
┌─────────────────────────────────────────┐
│  🏨 Hotel Chatbot Login                 │
├─────────────────────────────────────────┤
│                                         │
│  Please login to continue  🟢 API Online│
│                                         │
│  Select User: [Guest User (GUEST) ▼]   │
│  Password:    [••••••••]                │
│                                         │
│  [🔐 Login]  [❓ Help]                  │
│                                         │
│  ────────────────────────────────────   │
│                                         │
│  📝 Demo Credentials                    │
│                                         │
│  Guest Accounts:          Staff:        │
│  guest@hotel.com          staff@hotel.com│
│  john@email.com           admin@hotel.com│
│  🔹 6 tools               🔸 10 tools    │
│                                         │
└─────────────────────────────────────────┘
```

**Features:**
- ✅ User dropdown with names and roles
- ✅ Password field
- ✅ API health indicator (green = online)
- ✅ Help button
- ✅ Demo credentials display

---

### 2. Chat Interface (Guest View) 👤

```
┌─────────────────────────────────────────────────────────────┐
│ 🏨 Hotel Chatbot    👤 Guest User (GUEST)      [🚪 Logout] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ SIDEBAR                    │  MAIN CHAT AREA                │
│ ───────────                │  ─────────────────              │
│                            │                                 │
│ 🤖 Agent Information       │  👤 User: Show me rooms         │
│ ┌────────────────┐         │     ↳ 10:23:45                 │
│ │ Role: GUEST    │         │                                 │
│ │ Tools: 6       │         │  🤖 Bot: Found 8 rooms...      │
│ └────────────────┘         │     ↳ 10:23:47                 │
│                            │                                 │
│ 🛠️ Available Tools         │  👤 User: Book room 201        │
│ ▼                          │     ↳ 10:24:12                 │
│ 1. search_rooms            │                                 │
│ 2. book_room               │  🤖 Bot: ✅ Booking Confirmed! │
│ 3. cancel_booking          │     Booking ID: 1               │
│ 4. get_my_bookings         │     Room: 201 (Double)         │
│ 5. get_room_details        │     ↳ 10:24:15                 │
│ 6. answer_faq              │                                 │
│                            │  ──────────────────────────     │
│ 💡 Quick Actions           │                                 │
│ [Show me available rooms]  │  [Type message...] [📤 Send]   │
│ [Rooms under $200?]        │                                 │
│ [What time is checkout?]   │                                 │
│ [Show my bookings]         │                                 │
│ [Tell me about WiFi]       │                                 │
│                            │                                 │
│ [🗑️ Clear Chat]            │                                 │
└────────────────────────────┴─────────────────────────────────┘
```

**Guest Features:**
- ✅ 6 tools in sidebar
- ✅ 5 guest-specific quick actions
- ✅ Chat history with timestamps
- ✅ User/Bot avatars
- ✅ Clear chat button

---

### 3. Chat Interface (Staff View) 👨‍💼

```
┌─────────────────────────────────────────────────────────────┐
│ 🏨 Hotel Chatbot    👨‍💼 Staff Member (STAFF)  [🚪 Logout] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ SIDEBAR                    │  MAIN CHAT AREA                │
│ ───────────                │  ─────────────────              │
│                            │                                 │
│ 🤖 Agent Information       │  👤 User: Show all bookings    │
│ ┌────────────────┐         │     ↳ 10:30:15                 │
│ │ Role: STAFF    │         │                                 │
│ │ Tools: 10      │         │  🤖 Bot: 📋 All Bookings (12): │
│ └────────────────┘         │     ✅ Booking #1              │
│                            │        Guest: john@email.com    │
│ 🛠️ Available Tools         │        Room: 201, ...          │
│ ▼                          │     ↳ 10:30:17                 │
│ 1. search_rooms            │                                 │
│ 2. book_room               │  👤 User: Update room 101 to   │
│ 3. cancel_booking          │          cleaning               │
│ 4. get_my_bookings         │     ↳ 10:31:05                 │
│ 5. get_room_details        │                                 │
│ 6. answer_faq              │  🤖 Bot: ✅ Room Status Updated│
│ 7. get_all_bookings ⭐     │     Room: 101                  │
│ 8. get_todays_checkins ⭐  │     Status: CLEANING           │
│ 9. get_available_...⭐     │     ↳ 10:31:07                 │
│ 10. update_room_status ⭐  │                                 │
│                            │  ──────────────────────────     │
│ 💡 Quick Actions           │                                 │
│ [Show me all bookings]     │  [Type message...] [📤 Send]   │
│ [Who's checking in today?] │                                 │
│ [Available rooms count?]   │                                 │
│ [Show available rooms]     │                                 │
│ [Update room 101 status]   │                                 │
│                            │                                 │
│ [🗑️ Clear Chat]            │                                 │
└────────────────────────────┴─────────────────────────────────┘
```

**Staff Features:**
- ✅ **10 tools** (4 staff-only marked with ⭐)
- ✅ 5 staff-specific quick actions
- ✅ Access to admin operations
- ✅ All guest features included

---

## 🎯 User Flow

### Guest User Flow:
```
1. Login as guest@hotel.com
   ↓
2. See 6 tools in sidebar
   ↓
3. Click "Show me available rooms"
   ↓
4. Bot lists available rooms
   ↓
5. Type "Book room 201 for 2024-12-20"
   ↓
6. Bot confirms booking with ID
   ↓
7. Click "Show my bookings"
   ↓
8. Bot shows user's bookings
```

### Staff User Flow:
```
1. Login as staff@hotel.com
   ↓
2. See 10 tools in sidebar (more than guest)
   ↓
3. Click "Show me all bookings"
   ↓
4. Bot shows ALL bookings (staff-only)
   ↓
5. Click "Who's checking in today?"
   ↓
6. Bot shows today's arrivals
   ↓
7. Type "Update room 101 status to cleaning"
   ↓
8. Bot confirms room status update
```

---

## 🎨 UI Components

### Header Bar
```
┌──────────────────────────────────────────────────────┐
│ 🏨 Hotel Chatbot    👤 User Name (ROLE)   [Logout] │
└──────────────────────────────────────────────────────┘
```

### Sidebar Components
```
┌─────────────────────┐
│ 🤖 Agent Information│
│ ┌─────────────────┐ │
│ │ Role: GUEST     │ │
│ │ Tools: 6        │ │
│ └─────────────────┘ │
│                     │
│ 🛠️ Available Tools  │
│ [Expandable List]   │
│                     │
│ 💡 Quick Actions    │
│ [Action Button 1]   │
│ [Action Button 2]   │
│ [Action Button 3]   │
│                     │
│ [🗑️ Clear Chat]     │
└─────────────────────┘
```

### Chat Message
```
┌──────────────────────────────────┐
│ 👤 User Message                  │
│    ↳ 10:23:45                    │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│ 🤖 Bot Response                  │
│    ↳ 10:23:47                    │
└──────────────────────────────────┘
```

### Message Input
```
┌────────────────────────────────────┬──────┐
│ Type your message...               │ 📤   │
└────────────────────────────────────┴──────┘
```

---

## 💡 Tips for Demo

### 1. **Show Login First**
- Point out the user dropdown
- Show different roles available
- Demonstrate API health check

### 2. **Guest Demo (2 minutes)**
- Login as guest
- Point out 6 tools in sidebar
- Click a quick action
- Try booking a room
- Show chat history

### 3. **Role Comparison (1 minute)**
- Logout
- Login as staff
- **Point out 10 tools now** (vs 6 for guest)
- Show staff-only quick actions
- Highlight the difference

### 4. **Staff Demo (2 minutes)**
- Click "Show all bookings" (staff only!)
- Try "Who's checking in today?"
- Update a room status
- Show how guest tools still work

### 5. **RAG Demo (1 minute)**
- Ask "What time is checkout?"
- Ask "Tell me about WiFi"
- Explain semantic search happening

---

## 🎤 Interview Talking Points

### For Streamlit App:

**"I built a full-stack demo"**
> "I created a Streamlit frontend on top of the FastAPI backend. It has a login page with role-based authentication and a chat interface that adapts based on the user's role."

**"Role-based UI"**
> "The sidebar shows different tools and quick actions depending on whether you're logged in as a guest or staff member. Guests see 6 tools, staff see 10."

**"Session management"**
> "I use Streamlit's session state to manage user authentication, chat history, and agent configuration across page refreshes."

**"Real-time interaction"**
> "Messages are sent to the FastAPI backend, processed by the LangGraph agent with role-specific tools, and responses are displayed in real-time with timestamps."

**"Quick actions"**
> "I added pre-configured buttons for common tasks. These are role-specific - guests get booking-related actions, staff get admin operations."

---

## 🚀 Running the Demo

### Quick Start
```bash
cd simple-hotel-bot
python start_demo.py
```

### Manual Start
```bash
# Terminal 1
python main.py

# Terminal 2
streamlit run app.py
```

### PowerShell (Windows)
```powershell
.\start_demo.ps1
```

---

## 📊 Feature Comparison

| Feature | API Only | API + Streamlit |
|---------|----------|-----------------|
| Authentication | Header-based | Login page ✨ |
| Chat Interface | curl/Postman | Beautiful UI ✨ |
| Tool Visibility | API docs | Sidebar list ✨ |
| Quick Actions | Manual typing | Click buttons ✨ |
| Chat History | None | Persistent ✨ |
| Role Demo | Hard to show | Visual diff ✨ |
| Interview Demo | Technical | User-friendly ✨ |

---

## 🎉 Why This is Impressive

1. ✅ **Full-stack** - Backend API + Frontend UI
2. ✅ **Professional** - Login, auth, session management
3. ✅ **Interactive** - Real-time chat experience
4. ✅ **Role-aware** - UI adapts to user role
5. ✅ **Demo-ready** - Can show live in interviews
6. ✅ **User-friendly** - Non-technical people can use it

---

**Perfect for interviews and demonstrations!** 🎉
