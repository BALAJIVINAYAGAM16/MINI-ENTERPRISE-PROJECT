from pydantic import BaseModel


class NotificationPreferenceUpdate(BaseModel):

    in_app_enabled: bool

    email_enabled: bool

    task_notifications: bool

    approval_notifications: bool

    escalation_notifications: bool

    document_notifications: bool