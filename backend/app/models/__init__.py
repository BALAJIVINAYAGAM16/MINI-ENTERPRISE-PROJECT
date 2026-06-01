# Import all models to register them with SQLAlchemy
from app.models.tenant import Tenant
from app.models.user import User
from app.models.task import Task
from app.models.approval import Approval
from app.models.approval_history import ApprovalHistory
from app.models.comments import Comment
from app.models.documents import Document
from app.models.notification import Notification
from app.models.activity_log import ActivityLog
from app.models.audit_log import AuditLog
from app.models.sla_rule import SLARule
from app.models.sla_tracking import SLATracking
from app.models.approval_escalation import ApprovalEscalation
from app.models.approval_delegation import ApprovalDelegation
from app.models.notification_preference import NotificationPreference
from app.models.subcription import Subscription

__all__ = [
    "Tenant",
    "User",
    "Task",
    "Approval",
    "ApprovalHistory",
    "Comment",
    "Document",
    "Notification",
    "ActivityLog",
    "AuditLog",
    "SLARule",
    "SLATracking",
    "ApprovalEscalation",
    "ApprovalDelegation",
    "NotificationPreference",
    "Subscription",
]
