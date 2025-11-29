from fastapi import HTTPException, Depends
from jwt_auth.jwt_handler import get_current_user


async def get_current_admin(current_user: dict = Depends(get_current_user)):
    """
    Dependency to verify that the current user has admin role.
    
    Args:
        current_user: User dict from get_current_user dependency
        
    Returns:
        dict: Current user if they are an admin
        
    Raises:
        HTTPException: 403 if user is not an admin
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access forbidden. Admin privileges required."
        )
    return current_user
