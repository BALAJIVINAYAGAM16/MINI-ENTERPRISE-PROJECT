from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_schema(engine: Engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if "tasks" not in tables:
        return

    task_columns = {column["name"] for column in inspector.get_columns("tasks")}
    missing_task_columns = {
        "updated_by": "INTEGER",
        "sla_status": "VARCHAR",
        "sla_due_time": "TIMESTAMP",
        "is_sla_breached": "BOOLEAN DEFAULT FALSE",
    }
    with engine.begin() as connection:
        for column_name, column_type in missing_task_columns.items():
            if column_name not in task_columns:
                connection.execute(text(f"ALTER TABLE tasks ADD COLUMN {column_name} {column_type}"))

    if "approvals" in tables:
        approval_columns = {column["name"] for column in inspector.get_columns("approvals")}
        missing_approval_columns = {
            "sla_status": "VARCHAR",
            "sla_due_time": "TIMESTAMP",
            "is_escalated": "BOOLEAN DEFAULT FALSE",
            "current_escalation_to": "INTEGER",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_approval_columns.items():
                if column_name not in approval_columns:
                    connection.execute(text(f"ALTER TABLE approvals ADD COLUMN {column_name} {column_type}"))

    if "notifications" in tables:
        notification_columns = {column["name"] for column in inspector.get_columns("notifications")}
        missing_notification_columns = {
            "notification_type": "VARCHAR",
            "priority": "VARCHAR",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_notification_columns.items():
                if column_name not in notification_columns:
                    connection.execute(text(f"ALTER TABLE notifications ADD COLUMN {column_name} {column_type}"))

    if "users" in tables:
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        missing_user_columns = {
            "refresh_token_hash": "VARCHAR",
            "refresh_token_expires_at": "TIMESTAMP",
            "password_reset_token_hash": "VARCHAR",
            "password_reset_expires_at": "TIMESTAMP",
            "tenant_id": "INTEGER",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_user_columns.items():
                if column_name not in user_columns:
                    connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))

    if "audit_logs" in tables:
        audit_columns = {column["name"] for column in inspector.get_columns("audit_logs")}
        missing_audit_columns = {
            "action": "VARCHAR",
            "entity": "VARCHAR",
            "entity_id": "INTEGER",
            "timestamp": "TIMESTAMP",
            "module_name": "VARCHAR(100)",
            "action_type": "VARCHAR(100)",
            "record_id": "INTEGER",
            "old_data": "JSON",
            "new_data": "JSON",
            "ip_address": "VARCHAR(255)",
            "user_agent": "VARCHAR(500)",
            "created_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_audit_columns.items():
                if column_name not in audit_columns:
                    connection.execute(text(f"ALTER TABLE audit_logs ADD COLUMN {column_name} {column_type}"))

    # Subscriptions table enhancements
    if "subscriptions" in tables:
        sub_columns = {column["name"] for column in inspector.get_columns("subscriptions")}
        missing_sub_columns = {
            "billing_cycle_start": "TIMESTAMP",
            "billing_cycle_end": "TIMESTAMP",
            "is_active": "BOOLEAN",
            "updated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_sub_columns.items():
                if column_name not in sub_columns:
                    connection.execute(text(f"ALTER TABLE subscriptions ADD COLUMN {column_name} {column_type}"))
