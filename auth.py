"""
RBAC (Role-Based Access Control) System
Manages user authentication and role permissions
"""
from typing import Optional, Dict

# Simple user store - in production, this would be a database
USERS = {
    "guest@hotel.com": {"role": "guest", "name": "Guest User"},
    "john@email.com": {"role": "guest", "name": "John Doe"},
    "staff@hotel.com": {"role": "staff", "name": "Staff Member"},
    "admin@hotel.com": {"role": "staff", "name": "Admin User"},
    "manager@hotel.com": {"role": "staff", "name": "Hotel Manager"}
}


def get_user(email: str) -> Optional[Dict[str, str]]:
    """
    Get user information by email
    
    Args:
        email: User's email address
        
    Returns:
        User dict with role and name, or None if not found
    """
    return USERS.get(email.lower())


def validate_role(email: str, required_role: str) -> bool:
    """
    Check if user has the required role
    
    Args:
        email: User's email address
        required_role: Required role ('guest' or 'staff')
        
    Returns:
        True if user has required role, False otherwise
    """
    user = get_user(email)
    if not user:
        return False
    
    # Staff role has access to everything
    if user["role"] == "staff":
        return True
    
    # Guest role only has guest access
    return user["role"] == required_role


def get_user_role(email: str) -> Optional[str]:
    """
    Get user's role
    
    Args:
        email: User's email address
        
    Returns:
        Role string ('guest' or 'staff'), or None if user not found
    """
    user = get_user(email)
    return user["role"] if user else None


def is_guest(email: str) -> bool:
    """Check if user is a guest"""
    return get_user_role(email) == "guest"


def is_staff(email: str) -> bool:
    """Check if user is staff"""
    return get_user_role(email) == "staff"
