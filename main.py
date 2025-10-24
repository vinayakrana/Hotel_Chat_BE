"""
Hotel Chatbot FastAPI Application
Main API with authentication and role-based access
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from agent import create_agent_for_user, get_agent_info
from auth import get_user, get_user_role
from database import get_available_rooms, get_bookings_by_email, init_database

# Initialize database
init_database()

# Create FastAPI app
app = FastAPI(
    title="Hotel Chatbot API",
    description="AI-powered hotel management chatbot with RAG and RBAC",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# Request/Response Models
# ============================================

class ChatRequest(BaseModel):
    """Chat request from user"""
    message: str = Field(..., description="User's message to the chatbot")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "I want to book a room for next week"
            }
        }


class ChatResponse(BaseModel):
    """Chat response from bot"""
    response: str = Field(..., description="Bot's response message")
    role: str = Field(..., description="User's role (guest or staff)")
    user_name: str = Field(..., description="User's name")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "I'd be happy to help you book a room! Could you please provide...",
                "role": "guest",
                "user_name": "John Doe"
            }
        }


# ============================================
# Authentication Dependency
# ============================================

async def get_current_user(x_user_email: str = Header(..., description="User's email for authentication")):
    """
    Validate user from X-User-Email header
    
    Args:
        x_user_email: Email from header
        
    Returns:
        User dict
        
    Raises:
        HTTPException: If user not found
    """
    user = get_user(x_user_email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized: User '{x_user_email}' not found. Valid users: guest@hotel.com, staff@hotel.com"
        )
    return user


# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """API information and available endpoints"""
    return {
        "service": "Hotel Chatbot API",
        "version": "2.0.0",
        "features": [
            "RAG-powered FAQ answering with ChromaDB",
            "Role-Based Access Control (RBAC)",
            "10 LangChain tools (6 guest + 4 staff)",
            "LangGraph agent orchestration"
        ],
        "endpoints": {
            "POST /chat": "Main chatbot endpoint (requires X-User-Email header)",
            "GET /rooms": "List available rooms (public)",
            "GET /bookings": "Get user's bookings (requires X-User-Email header)",
            "GET /agent-info": "Get agent configuration for user (requires X-User-Email header)",
            "GET /health": "Health check"
        },
        "authentication": {
            "method": "Header-based",
            "header": "X-User-Email",
            "test_users": {
                "guest": "guest@hotel.com",
                "staff": "staff@hotel.com"
            }
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    x_user_email: str = Header(..., description="User email for authentication")
):
    """
    Main chat endpoint - sends message to role-based agent
    
    The agent will have access to different tools based on user role:
    - Guest: 6 tools (search, book, cancel, view bookings, room details, FAQ)
    - Staff: 10 tools (guest tools + view all bookings, check-ins, availability, update status)
    """
    try:
        # Authenticate user
        user = await get_current_user(x_user_email)
        
        # Create agent for this user's role
        agent = create_agent_for_user(x_user_email)
        
        # Invoke agent with user's message
        result = agent.invoke({
            "messages": [("user", request.message)]
        })
        
        # Extract response
        last_message = result["messages"][-1]
        response_text = last_message.content
        
        return ChatResponse(
            response=response_text,
            role=user["role"],
            user_name=user["name"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.get("/rooms")
async def list_rooms():
    """
    List all available rooms (public endpoint, no auth required)
    """
    try:
        rooms = get_available_rooms()
        return {
            "count": len(rooms),
            "rooms": rooms
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving rooms: {str(e)}")


@app.get("/bookings")
async def get_user_bookings(x_user_email: str = Header(...)):
    """
    Get all bookings for the authenticated user
    """
    try:
        user = await get_current_user(x_user_email)
        bookings = get_bookings_by_email(x_user_email)
        
        return {
            "user": user["name"],
            "email": x_user_email,
            "count": len(bookings),
            "bookings": bookings
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bookings: {str(e)}")


@app.get("/agent-info")
async def agent_info(x_user_email: str = Header(...)):
    """
    Get information about the agent that would be created for this user
    Useful for debugging and understanding RBAC
    """
    try:
        user = await get_current_user(x_user_email)
        info = get_agent_info(x_user_email)
        
        return {
            "user": user,
            "agent": info,
            "rbac": {
                "description": "Tools are loaded based on user role",
                "guest_tools": 6,
                "staff_tools": 10
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent info: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    # Check if Groq API key is set
    groq_key_set = bool(os.getenv("GROQ_API_KEY"))
    
    return {
        "status": "healthy" if groq_key_set else "degraded",
        "service": "hotel-chatbot",
        "version": "2.0.0",
        "checks": {
            "groq_api_key": "configured" if groq_key_set else "missing"
        }
    }


# ============================================
# Startup Event
# ============================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Starting Hotel Chatbot API...")
    print(f"✅ FastAPI app initialized")
    print(f"✅ Database initialized")
    
    # Import vector store to initialize it
    try:
        import vector_store
        print(f"✅ Vector store initialized")
    except Exception as e:
        print(f"⚠️  Vector store initialization warning: {e}")
    
    # Check Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  WARNING: GROQ_API_KEY not set in environment variables!")
        print("   Please create a .env file with your Groq API key")
    else:
        print(f"✅ Groq API key configured")
    
    print("\n" + "="*50)
    print("🎉 Hotel Chatbot API is ready!")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🔑 Test users:")
    print("   - guest@hotel.com (6 tools)")
    print("   - staff@hotel.com (10 tools)")
    print("="*50 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
