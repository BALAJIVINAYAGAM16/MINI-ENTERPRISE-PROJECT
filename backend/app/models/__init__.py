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
from app.models.subscription import Subscription
from app.models.tenant_onboarding import TenantOnboarding
from app.models.tenant_collaboration import TenantCollaborationSettings, TenantCollaborationUsage
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.channel import Channel
from app.models.channel_member import ChannelMember
from app.models.workspace_message import WorkspaceMessage
from app.models.channel_message import ChannelMessage
from app.models.task_document import TaskDocument
from app.models.approval_document import ApprovalDocument

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
    "TenantOnboarding",
    "TenantCollaborationSettings",
    "TenantCollaborationUsage",
    "Workspace",
    "WorkspaceMember",
    "Channel",
    "ChannelMember",
    "WorkspaceMessage",
    "ChannelMessage",
    "TaskDocument",
    "ApprovalDocument",
]
