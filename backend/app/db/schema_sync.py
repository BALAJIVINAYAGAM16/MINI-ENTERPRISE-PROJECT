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

    if "tenants" in tables:
        tenant_columns = {column["name"] for column in inspector.get_columns("tenants")}
        missing_tenant_columns = {
            "name": "VARCHAR(255)",
            "slug": "VARCHAR(100)",
            "contact_email": "VARCHAR(255)",
            "phone": "VARCHAR(50)",
            "address": "VARCHAR(500)",
            "industry": "VARCHAR(100)",
            "status": "VARCHAR(20) DEFAULT 'ACTIVE'",
            "updated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_tenant_columns.items():
                if column_name not in tenant_columns:
                    connection.execute(text(f"ALTER TABLE tenants ADD COLUMN {column_name} {column_type}"))

    if "tenant_collaboration_settings" in tables:
        settings_columns = {
            column["name"] for column in inspector.get_columns("tenant_collaboration_settings")
        }
        missing_settings_columns = {
            "tenant_id": "INTEGER",
            "max_workspaces": "INTEGER DEFAULT 10",
            "max_channels_per_workspace": "INTEGER DEFAULT 50",
            "max_workspace_members": "INTEGER DEFAULT 500",
            "max_storage_mb": "INTEGER DEFAULT 1024",
            "workspace_enabled": "BOOLEAN DEFAULT TRUE",
            "channel_enabled": "BOOLEAN DEFAULT TRUE",
            "created_at": "TIMESTAMP",
            "updated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_settings_columns.items():
                if column_name not in settings_columns:
                    connection.execute(
                        text(f"ALTER TABLE tenant_collaboration_settings ADD COLUMN {column_name} {column_type}")
                    )

    if "tenant_onboarding" in tables:
        onboarding_columns = {column["name"] for column in inspector.get_columns("tenant_onboarding")}
        missing_onboarding_columns = {
            "tenant_id": "INTEGER",
            "admin_user_id": "INTEGER",
            "onboarding_status": "VARCHAR(20) DEFAULT 'PENDING'",
            "default_workspace_created": "BOOLEAN DEFAULT FALSE",
            "settings_created": "BOOLEAN DEFAULT FALSE",
            "completed_at": "TIMESTAMP",
            "created_at": "TIMESTAMP",
            "updated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_onboarding_columns.items():
                if column_name not in onboarding_columns:
                    connection.execute(text(f"ALTER TABLE tenant_onboarding ADD COLUMN {column_name} {column_type}"))

    if "tenant_collaboration_usage" in tables:
        usage_columns = {column["name"] for column in inspector.get_columns("tenant_collaboration_usage")}
        missing_usage_columns = {
            "tenant_id": "INTEGER",
            "workspace_count": "INTEGER DEFAULT 0",
            "channel_count": "INTEGER DEFAULT 0",
            "member_count": "INTEGER DEFAULT 0",
            "storage_used_mb": "INTEGER DEFAULT 0",
            "last_calculated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_usage_columns.items():
                if column_name not in usage_columns:
                    connection.execute(
                        text(f"ALTER TABLE tenant_collaboration_usage ADD COLUMN {column_name} {column_type}")
                    )

    if "workspaces" in tables:
        workspace_columns = {column["name"] for column in inspector.get_columns("workspaces")}
        missing_workspace_columns = {
            "tenant_id": "INTEGER",
            "name": "VARCHAR(255)",
            "slug": "VARCHAR(255)",
            "description": "TEXT",
            "avatar_url": "VARCHAR(500)",
            "visibility": "VARCHAR(20) DEFAULT 'PUBLIC'",
            "created_by": "INTEGER",
            "is_archived": "BOOLEAN DEFAULT FALSE",
            "created_at": "TIMESTAMP",
            "updated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_workspace_columns.items():
                if column_name not in workspace_columns:
                    connection.execute(text(f"ALTER TABLE workspaces ADD COLUMN {column_name} {column_type}"))

    if "channels" in tables:
        channel_columns = {column["name"] for column in inspector.get_columns("channels")}
        missing_channel_columns = {
            "tenant_id": "INTEGER",
            "workspace_id": "INTEGER",
            "name": "VARCHAR(255)",
            "description": "TEXT",
            "channel_type": "VARCHAR(30) DEFAULT 'PUBLIC'",
            "created_by": "INTEGER",
            "is_archived": "BOOLEAN DEFAULT FALSE",
            "created_at": "TIMESTAMP",
            "updated_at": "TIMESTAMP",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_channel_columns.items():
                if column_name not in channel_columns:
                    connection.execute(text(f"ALTER TABLE channels ADD COLUMN {column_name} {column_type}"))

    if "workspace_members" in tables:
        member_columns = {column["name"] for column in inspector.get_columns("workspace_members")}
        missing_member_columns = {
            "workspace_id": "INTEGER",
            "user_id": "INTEGER",
            "role": "VARCHAR(30) DEFAULT 'MEMBER'",
            "joined_at": "TIMESTAMP",
            "is_active": "BOOLEAN DEFAULT TRUE",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_member_columns.items():
                if column_name not in member_columns:
                    connection.execute(text(f"ALTER TABLE workspace_members ADD COLUMN {column_name} {column_type}"))

    if "channel_members" in tables:
        channel_member_columns = {column["name"] for column in inspector.get_columns("channel_members")}
        missing_channel_member_columns = {
            "channel_id": "INTEGER",
            "user_id": "INTEGER",
            "joined_at": "TIMESTAMP",
            "is_muted": "BOOLEAN DEFAULT FALSE",
            "last_read_message_id": "INTEGER",
        }
        with engine.begin() as connection:
            for column_name, column_type in missing_channel_member_columns.items():
                if column_name not in channel_member_columns:
                    connection.execute(text(f"ALTER TABLE channel_members ADD COLUMN {column_name} {column_type}"))
