"""Application constants and enums."""

from enum import Enum


class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    MANAGER = "manager"
    TRAINER = "trainer"
    STAFF = "staff"
    MEMBER = "member"


class MembershipStatus(str, Enum):
    """Membership status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FROZEN = "frozen"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class MembershipType(str, Enum):
    """Membership types."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    HALF_YEARLY = "half_yearly"
    YEARLY = "yearly"
    DAILY_PASS = "daily_pass"


class AttendanceStatus(str, Enum):
    """Attendance status."""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    LEFT_EARLY = "left_early"


class PaymentStatus(str, Enum):
    """Payment status."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Payment methods."""
    CASH = "cash"
    CARD = "card"
    STRIPE = "stripe"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"


class ExpenseCategory(str, Enum):
    """Expense categories."""
    SALARY = "salary"
    UTILITIES = "utilities"
    RENT = "rent"
    MAINTENANCE = "maintenance"
    EQUIPMENT = "equipment"
    SUPPLIES = "supplies"
    OTHER = "other"


class NotificationType(str, Enum):
    """Notification types."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class DifficultyLevel(str, Enum):
    """Difficulty levels for workouts."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class WorkoutType(str, Enum):
    """Workout types."""
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    HIIT = "hiit"
    YOGA = "yoga"
    PILATES = "pilates"
    SPORTS = "sports"


class MuscleGroup(str, Enum):
    """Muscle groups."""
    CHEST = "chest"
    BACK = "back"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    FOREARMS = "forearms"
    LEGS = "legs"
    GLUTES = "glutes"
    CORE = "core"
    CARDIO = "cardio"


# Default values
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
DEFAULT_LIMIT = 10

# Rate limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 60  # seconds

# File upload
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"]

# Password
MIN_PASSWORD_LENGTH = 8

# JWT
TOKEN_TYPE = "Bearer"
