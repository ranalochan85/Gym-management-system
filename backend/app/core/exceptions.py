"""Custom exception classes."""

from fastapi import HTTPException, status


class GymException(Exception):
    """Base exception for gym management system."""
    pass


class UserNotFound(GymException):
    """Raised when user is not found."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")


class MemberNotFound(GymException):
    """Raised when member is not found."""
    def __init__(self, member_id: int):
        self.member_id = member_id
        super().__init__(f"Member with ID {member_id} not found")


class InvalidCredentials(GymException):
    """Raised when credentials are invalid."""
    def __init__(self):
        super().__init__("Invalid email or password")


class UserAlreadyExists(GymException):
    """Raised when user already exists."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InsufficientPermission(GymException):
    """Raised when user lacks required permissions."""
    def __init__(self):
        super().__init__("Insufficient permissions")


class InvalidInput(GymException):
    """Raised when input validation fails."""
    def __init__(self, message: str):
        super().__init__(message)


class PaymentFailed(GymException):
    """Raised when payment processing fails."""
    def __init__(self, reason: str = "Payment processing failed"):
        super().__init__(reason)


class MembershipExpired(GymException):
    """Raised when membership is expired."""
    def __init__(self, member_id: int):
        self.member_id = member_id
        super().__init__(f"Membership expired for member {member_id}")


class AttendanceAlreadyRecorded(GymException):
    """Raised when attendance already recorded."""
    def __init__(self, member_id: int):
        self.member_id = member_id
        super().__init__(f"Attendance already recorded for member {member_id}")


def http_exception_handler(status_code: int, detail: str) -> HTTPException:
    """Create an HTTP exception."""
    return HTTPException(status_code=status_code, detail=detail)
