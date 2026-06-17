"""Application models initialization."""

from app.models.user import User, UserSession, AuditLog
from app.models.member import Member, Membership, MembershipHistory
from app.models.trainer import Trainer, TrainerCertification, TrainerMemberAssignment, TrainerPerformance, TrainerSchedule
from app.models.staff import Staff, StaffSchedule, StaffPerformance
from app.models.branch import Gym, Branch, BranchTiming
from app.models.attendance import Attendance, QRCode, RFIDCard
from app.models.workout import Exercise, WorkoutPlan, WorkoutExercise, WorkoutSession, ExerciseLog, BodyProgress
from app.models.nutrition import DietPlan, Meal, NutritionTracking
from app.models.payment import Payment, Invoice, Receipt, Revenue, Expense
from app.models.inventory import Equipment, EquipmentMaintenance, InventoryItem, StockMovement
from app.models.notification import Notification, NotificationLog, NotificationTemplate
from app.models.class_model import GroupClass, ClassSchedule, ClassEnrollment, ClassAttendance

__all__ = [
    "User", "UserSession", "AuditLog",
    "Member", "Membership", "MembershipHistory",
    "Trainer", "TrainerCertification", "TrainerMemberAssignment", "TrainerPerformance", "TrainerSchedule",
    "Staff", "StaffSchedule", "StaffPerformance",
    "Gym", "Branch", "BranchTiming",
    "Attendance", "QRCode", "RFIDCard",
    "Exercise", "WorkoutPlan", "WorkoutExercise", "WorkoutSession", "ExerciseLog", "BodyProgress",
    "DietPlan", "Meal", "NutritionTracking",
    "Payment", "Invoice", "Receipt", "Revenue", "Expense",
    "Equipment", "EquipmentMaintenance", "InventoryItem", "StockMovement",
    "Notification", "NotificationLog", "NotificationTemplate",
    "GroupClass", "ClassSchedule", "ClassEnrollment", "ClassAttendance",
]
