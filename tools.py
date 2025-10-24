"""
LangChain Tools for Hotel Management
10 tools: 6 for guests, 4 additional for staff
"""
from langchain.tools import tool
from typing import Optional
from datetime import datetime, date
import os

# Import database functions
from database import (
    get_available_rooms,
    get_room_by_number,
    is_room_available,
    create_booking,
    get_booking,
    cancel_booking_in_db,
    get_bookings_by_email,
    get_all_bookings_from_db,
    get_checkins_by_date,
    get_room_availability_counts,
    update_room_status_in_db
)

# Import vector store for RAG
from vector_store import get_faq_context


# ============================================
# GUEST TOOLS (6)
# ============================================

@tool
def search_rooms(room_type: Optional[str] = None, max_price: Optional[float] = None) -> str:
    """
    Search for available rooms. Optionally filter by room type (Single, Double, Suite, Deluxe, Presidential) 
    and maximum price per night.
    
    Args:
        room_type: Type of room to search for (optional)
        max_price: Maximum price per night (optional)
    
    Returns:
        String with available rooms and their details
    """
    try:
        rooms = get_available_rooms()
        
        # Apply filters
        if room_type:
            rooms = [r for r in rooms if r['room_type'].lower() == room_type.lower()]
        
        if max_price:
            rooms = [r for r in rooms if r['price_per_night'] <= max_price]
        
        if not rooms:
            return "No rooms found matching your criteria. Try adjusting your search parameters."
        
        result = f"Found {len(rooms)} available room(s):\n\n"
        for room in rooms:
            result += f"🏨 Room {room['room_number']} ({room['room_type']})\n"
            result += f"   💰 ${room['price_per_night']:.2f} per night\n"
            result += f"   ✅ Status: {room['room_status']}\n\n"
        
        return result.strip()
    
    except Exception as e:
        return f"Error searching rooms: {str(e)}"


@tool
def book_room(room_number: str, guest_email: str, check_in: str, check_out: str) -> str:
    """
    Book a hotel room for a guest. Validates dates and checks availability.
    
    Args:
        room_number: Room number to book (e.g., "101", "201")
        guest_email: Guest's email address
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
    
    Returns:
        Booking confirmation with booking ID or error message
    """
    try:
        # Validate date format
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            return "❌ Error: Invalid date format. Please use YYYY-MM-DD format (e.g., 2024-12-25)"
        
        # Validate date logic
        if check_out_date <= check_in_date:
            return "❌ Error: Check-out date must be after check-in date."
        
        # Check if dates are in the future
        today = datetime.now().date()
        if check_in_date.date() < today:
            return "❌ Error: Check-in date cannot be in the past."
        
        # Check if room exists
        room = get_room_by_number(room_number)
        if not room:
            return f"❌ Error: Room {room_number} does not exist."
        
        # Check availability
        if not is_room_available(room_number, check_in, check_out):
            return f"❌ Room {room_number} is not available for those dates. Please try different dates or another room."
        
        # Create booking
        booking_id = create_booking(room_number, guest_email, check_in, check_out)
        
        # Calculate nights and total
        nights = (check_out_date - check_in_date).days
        total_price = nights * room['price_per_night']
        
        result = f"✅ Booking Confirmed!\n\n"
        result += f"📋 Booking ID: {booking_id}\n"
        result += f"🏨 Room: {room_number} ({room['room_type']})\n"
        result += f"📧 Guest: {guest_email}\n"
        result += f"📅 Check-in: {check_in}\n"
        result += f"📅 Check-out: {check_out}\n"
        result += f"🌙 Nights: {nights}\n"
        result += f"💰 Total: ${total_price:.2f}\n\n"
        result += f"Please save your booking ID for future reference."
        
        return result
    
    except Exception as e:
        return f"❌ Error creating booking: {str(e)}"


@tool
def cancel_booking(booking_id: int, guest_email: str) -> str:
    """
    Cancel a booking. Only the guest who made the booking can cancel it.
    
    Args:
        booking_id: The booking ID to cancel
        guest_email: Guest's email address (for verification)
    
    Returns:
        Confirmation message or error
    """
    try:
        # Get booking
        booking = get_booking(booking_id)
        
        if not booking:
            return f"❌ Error: Booking #{booking_id} not found."
        
        # Check if booking already cancelled
        if booking['status'] == 'cancelled':
            return f"ℹ️ Booking #{booking_id} is already cancelled."
        
        # Verify guest email
        if booking['guest_email'] != guest_email:
            return "❌ Error: You can only cancel your own bookings."
        
        # Cancel booking
        if cancel_booking_in_db(booking_id):
            result = f"✅ Booking Cancelled Successfully\n\n"
            result += f"📋 Booking ID: {booking_id}\n"
            result += f"🏨 Room: {booking['room_number']}\n"
            result += f"📅 Was scheduled: {booking['check_in_date']} to {booking['check_out_date']}\n\n"
            result += f"Your booking has been cancelled. If you were charged, a refund will be processed according to our cancellation policy."
            return result
        else:
            return f"❌ Error: Failed to cancel booking #{booking_id}."
    
    except Exception as e:
        return f"❌ Error cancelling booking: {str(e)}"


@tool
def get_my_bookings(guest_email: str) -> str:
    """
    Get all bookings for a specific guest.
    
    Args:
        guest_email: Guest's email address
    
    Returns:
        List of all bookings for the guest
    """
    try:
        bookings = get_bookings_by_email(guest_email)
        
        if not bookings:
            return f"📋 You have no bookings on record for {guest_email}."
        
        result = f"📋 Your Bookings ({len(bookings)} total):\n\n"
        
        for booking in bookings:
            status_emoji = "✅" if booking['status'] == 'confirmed' else "❌"
            result += f"{status_emoji} Booking #{booking['id']}\n"
            result += f"   🏨 Room: {booking['room_number']}\n"
            result += f"   📅 {booking['check_in_date']} to {booking['check_out_date']}\n"
            result += f"   Status: {booking['status'].upper()}\n\n"
        
        return result.strip()
    
    except Exception as e:
        return f"❌ Error retrieving bookings: {str(e)}"


@tool
def get_room_details(room_number: str) -> str:
    """
    Get detailed information about a specific room.
    
    Args:
        room_number: Room number to get details for
    
    Returns:
        Detailed room information
    """
    try:
        room = get_room_by_number(room_number)
        
        if not room:
            return f"❌ Room {room_number} not found."
        
        result = f"🏨 Room {room['room_number']} Details\n\n"
        result += f"🛏️  Type: {room['room_type']}\n"
        result += f"💰 Price: ${room['price_per_night']:.2f} per night\n"
        result += f"📊 Status: {room['room_status'].upper()}\n\n"
        
        # Add room type descriptions
        descriptions = {
            "Single": "Perfect for solo travelers. Includes one queen bed, work desk, and ensuite bathroom.",
            "Double": "Ideal for couples or friends. Features two double beds, sitting area, and city view.",
            "Suite": "Spacious suite with separate living area, king bed, minibar, and premium amenities.",
            "Deluxe": "Luxury room with king bed, sofa, premium linens, and stunning views.",
            "Presidential": "Ultimate luxury with separate bedroom, living room, dining area, and butler service."
        }
        
        if room['room_type'] in descriptions:
            result += f"📝 Description:\n{descriptions[room['room_type']]}\n"
        
        return result
    
    except Exception as e:
        return f"❌ Error retrieving room details: {str(e)}"


@tool
def answer_faq(question: str) -> str:
    """
    Answer frequently asked questions about the hotel using RAG (Retrieval-Augmented Generation).
    This tool searches our knowledge base for relevant information.
    
    Args:
        question: The question to answer
    
    Returns:
        Answer based on hotel FAQ knowledge base
    """
    try:
        # Get relevant context from vector store
        context_docs = get_faq_context(question, k=3)
        
        if not context_docs:
            return "I don't have specific information about that in our FAQ database. Please contact the front desk at extension 100 or email info@hotel.com for assistance."
        
        # Combine context
        context = "\n".join(context_docs)
        
        # For now, return the most relevant context
        # In production, you'd use an LLM to generate a natural answer
        result = f"ℹ️ Based on our hotel policies:\n\n"
        result += f"{context_docs[0]}\n"
        
        if len(context_docs) > 1:
            result += f"\n📚 Related information:\n"
            for i, doc in enumerate(context_docs[1:], 1):
                result += f"{i}. {doc[:100]}...\n"
        
        return result
    
    except Exception as e:
        return f"❌ Error answering question: {str(e)}"


# ============================================
# STAFF TOOLS (4 additional)
# ============================================

@tool
def get_all_bookings(date_filter: Optional[str] = None) -> str:
    """
    Get all bookings in the system (STAFF ONLY).
    Optionally filter by check-in or check-out date.
    
    Args:
        date_filter: Optional date in YYYY-MM-DD format to filter bookings
    
    Returns:
        List of all bookings
    """
    try:
        bookings = get_all_bookings_from_db(date_filter)
        
        if not bookings:
            filter_msg = f" for {date_filter}" if date_filter else ""
            return f"📋 No bookings found{filter_msg}."
        
        filter_msg = f" for {date_filter}" if date_filter else ""
        result = f"📋 All Bookings{filter_msg} ({len(bookings)} total):\n\n"
        
        for booking in bookings:
            result += f"✅ Booking #{booking['id']}\n"
            result += f"   👤 Guest: {booking['guest_email']}\n"
            result += f"   🏨 Room: {booking['room_number']}\n"
            result += f"   📅 {booking['check_in_date']} to {booking['check_out_date']}\n"
            result += f"   Status: {booking['status'].upper()}\n\n"
        
        return result.strip()
    
    except Exception as e:
        return f"❌ Error retrieving bookings: {str(e)}"


@tool
def get_todays_checkins() -> str:
    """
    Get all check-ins scheduled for today (STAFF ONLY).
    Useful for front desk staff to prepare for arrivals.
    
    Returns:
        List of today's check-ins
    """
    try:
        today = date.today().strftime("%Y-%m-%d")
        checkins = get_checkins_by_date(today)
        
        if not checkins:
            return f"📋 No check-ins scheduled for today ({today})."
        
        result = f"📋 Today's Check-ins ({today}) - {len(checkins)} arrival(s):\n\n"
        
        for checkin in checkins:
            result += f"🏨 Room {checkin['room_number']}\n"
            result += f"   👤 Guest: {checkin['guest_email']}\n"
            result += f"   📋 Booking ID: {checkin['id']}\n"
            result += f"   📅 Check-out: {checkin['check_out_date']}\n\n"
        
        result += f"💡 Tip: Ensure rooms are ready and welcome packets are prepared."
        
        return result
    
    except Exception as e:
        return f"❌ Error retrieving check-ins: {str(e)}"


@tool
def get_available_rooms_count() -> str:
    """
    Get count of available rooms by type (STAFF ONLY).
    Quick overview of occupancy status.
    
    Returns:
        Count of available rooms by category
    """
    try:
        counts = get_room_availability_counts()
        
        if not counts:
            return "⚠️ No available rooms at the moment."
        
        result = "📊 Room Availability Overview:\n\n"
        
        total = 0
        for room_type, count in sorted(counts.items()):
            result += f"🛏️  {room_type}: {count} available\n"
            total += count
        
        result += f"\n✅ Total Available: {total} rooms"
        
        return result
    
    except Exception as e:
        return f"❌ Error retrieving availability: {str(e)}"


@tool
def update_room_status(room_number: str, status: str) -> str:
    """
    Update the status of a room (STAFF ONLY).
    Valid statuses: available, cleaning, occupied, maintenance
    
    Args:
        room_number: Room number to update
        status: New status (available, cleaning, occupied, maintenance)
    
    Returns:
        Confirmation message
    """
    try:
        valid_statuses = ['available', 'cleaning', 'occupied', 'maintenance']
        
        if status.lower() not in valid_statuses:
            return f"❌ Error: Invalid status '{status}'. Valid options: {', '.join(valid_statuses)}"
        
        # Check if room exists
        room = get_room_by_number(room_number)
        if not room:
            return f"❌ Error: Room {room_number} not found."
        
        # Update status
        if update_room_status_in_db(room_number, status.lower()):
            result = f"✅ Room Status Updated\n\n"
            result += f"🏨 Room: {room_number}\n"
            result += f"📊 Previous Status: {room['room_status']}\n"
            result += f"📊 New Status: {status.upper()}\n"
            return result
        else:
            return f"❌ Error: Failed to update room {room_number}."
    
    except Exception as e:
        return f"❌ Error updating room status: {str(e)}"
