from datetime import datetime, timedelta

from app.core.security import hash_password
from app.db.database import Base, SessionLocal, engine
from app.db.schema_sync import ensure_schema
from app.models import (
    ActivityLog,
    Approval,
    ApprovalDelegation,
    ApprovalEscalation,
    ApprovalHistory,
    AuditLog,
    Comment,
    Document,
    Notification,
    NotificationPreference,
    SLARule,
    SLATracking,
    Subscription,
    Task,
    Tenant,
    User,
)


PASSWORD = "Password@123"


def get_or_create(db, model, defaults=None, **filters):
    record = db.query(model).filter_by(**filters).first()
    if record:
        return record

    record = model(**{**(defaults or {}), **filters})
    db.add(record)
    db.flush()
    return record


def seed():
    Base.metadata.create_all(bind=engine)
    ensure_schema(engine)

    db = SessionLocal()
    now = datetime.utcnow()

    try:
        tenant = get_or_create(
            db,
            Tenant,
            organization_name="Acme Workflow Labs",
            domain="acme.test",
        )

        users = {
            "admin": get_or_create(
                db,
                User,
                email="admin@acme.test",
                defaults={
                    "name": "Asha Admin",
                    "role": "admin",
                    "tenant_id": tenant.id,
                    "hashed_password": hash_password(PASSWORD),
                },
            ),
            "manager": get_or_create(
                db,
                User,
                email="manager@acme.test",
                defaults={
                    "name": "Maya Manager",
                    "role": "manager",
                    "tenant_id": tenant.id,
                    "hashed_password": hash_password(PASSWORD),
                },
            ),
            "employee": get_or_create(
                db,
                User,
                email="employee@acme.test",
                defaults={
                    "name": "Evan Employee",
                    "role": "employee",
                    "tenant_id": tenant.id,
                    "hashed_password": hash_password(PASSWORD),
                },
            ),
            "auditor": get_or_create(
                db,
                User,
                email="auditor@acme.test",
                defaults={
                    "name": "Anika Auditor",
                    "role": "auditor",
                    "tenant_id": tenant.id,
                    "hashed_password": hash_password(PASSWORD),
                },
            ),
        }

        get_or_create(
            db,
            Subscription,
            tenant_id=tenant.id,
            defaults={
                "plan": "Gold",
                "credits": 10000,
                "billing_cycle_start": now - timedelta(days=5),
                "billing_cycle_end": now + timedelta(days=25),
            },
        )

        for user in users.values():
            get_or_create(
                db,
                NotificationPreference,
                user_id=user.id,
                defaults={
                    "in_app_enabled": True,
                    "email_enabled": user.role != "employee",
                    "task_notifications": True,
                    "approval_notifications": True,
                    "escalation_notifications": True,
                    "document_notifications": True,
                },
            )

        rules = [
            ("TASK", "high", 24, True, 6),
            ("TASK", "medium", 48, True, 12),
            ("TASK", "low", 72, False, None),
            ("APPROVAL", "medium", 12, True, 4),
            ("APPROVAL", "high", 6, True, 2),
        ]
        sla_rules = {}
        for module_name, priority, allowed_hours, escalation_enabled, escalation_after_hours in rules:
            sla_rules[(module_name, priority)] = get_or_create(
                db,
                SLARule,
                module_name=module_name,
                priority=priority,
                defaults={
                    "allowed_hours": allowed_hours,
                    "escalation_enabled": escalation_enabled,
                    "escalation_after_hours": escalation_after_hours,
                    "is_active": True,
                    "created_by": users["admin"].id,
                },
            )

        tasks = [
            {
                "title": "Prepare Q2 compliance pack",
                "description": "Collect evidence, review access logs, and upload the final pack.",
                "status": "in_progress",
                "priority": "high",
                "due_date": now + timedelta(days=1),
                "created_by_id": users["manager"].id,
                "assigned_to_id": users["employee"].id,
                "sla_status": "ACTIVE",
                "sla_due_time": now + timedelta(hours=20),
                "is_sla_breached": False,
            },
            {
                "title": "Review vendor onboarding checklist",
                "description": "Validate security and finance checklist before vendor activation.",
                "status": "review",
                "priority": "medium",
                "due_date": now + timedelta(days=2),
                "created_by_id": users["manager"].id,
                "assigned_to_id": users["employee"].id,
                "sla_status": "BREACHED",
                "sla_due_time": now - timedelta(hours=3),
                "is_sla_breached": True,
            },
            {
                "title": "Archive completed sprint documents",
                "description": "Move completed sprint artifacts into the shared project archive.",
                "status": "done",
                "priority": "low",
                "due_date": now + timedelta(days=5),
                "created_by_id": users["admin"].id,
                "assigned_to_id": users["employee"].id,
                "sla_status": "COMPLETED_WITHIN_SLA",
                "sla_due_time": now - timedelta(hours=8),
                "is_sla_breached": False,
            },
        ]

        seeded_tasks = []
        for data in tasks:
            task = get_or_create(db, Task, title=data["title"], defaults=data)
            seeded_tasks.append(task)

        approvals = [
            {
                "title": "Approve enterprise renewal",
                "description": "Renew Gold subscription and support package.",
                "requested_by": users["manager"].id,
                "status": "pending",
                "current_level": "admin",
                "sla_status": "ACTIVE",
                "sla_due_time": now + timedelta(hours=8),
                "is_escalated": False,
            },
            {
                "title": "Approve delayed access exception",
                "description": "Temporary access exception for audit remediation.",
                "requested_by": users["employee"].id,
                "status": "pending",
                "current_level": "manager",
                "sla_status": "BREACHED",
                "sla_due_time": now - timedelta(hours=2),
                "is_escalated": True,
                "current_escalation_to": users["admin"].id,
            },
        ]

        seeded_approvals = []
        for data in approvals:
            approval = get_or_create(db, Approval, title=data["title"], defaults=data)
            seeded_approvals.append(approval)

        tracking_rows = [
            ("TASK", seeded_tasks[0].id, sla_rules[("TASK", "high")].id, now - timedelta(hours=4), now + timedelta(hours=20), None, "ACTIVE", None),
            ("TASK", seeded_tasks[1].id, sla_rules[("TASK", "medium")].id, now - timedelta(hours=51), now - timedelta(hours=3), None, "BREACHED", "SLA due time exceeded"),
            ("TASK", seeded_tasks[2].id, sla_rules[("TASK", "low")].id, now - timedelta(days=3), now - timedelta(hours=8), now - timedelta(hours=10), "COMPLETED_WITHIN_SLA", None),
            ("APPROVAL", seeded_approvals[0].id, sla_rules[("APPROVAL", "medium")].id, now - timedelta(hours=4), now + timedelta(hours=8), None, "ACTIVE", None),
            ("APPROVAL", seeded_approvals[1].id, sla_rules[("APPROVAL", "medium")].id, now - timedelta(hours=14), now - timedelta(hours=2), None, "ESCALATED", "Approval exceeded SLA"),
        ]
        for module_name, record_id, rule_id, start_time, due_time, completed_time, status, breach_reason in tracking_rows:
            get_or_create(
                db,
                SLATracking,
                module_name=module_name,
                record_id=record_id,
                defaults={
                    "sla_rule_id": rule_id,
                    "start_time": start_time,
                    "due_time": due_time,
                    "completed_time": completed_time,
                    "status": status,
                    "breach_reason": breach_reason,
                },
            )

        get_or_create(
            db,
            ApprovalEscalation,
            approval_id=seeded_approvals[1].id,
            escalated_to=users["admin"].id,
            defaults={
                "escalated_from": users["manager"].id,
                "reason": "Approval breached the 12 hour SLA window.",
                "escalation_level": 1,
                "status": "PENDING",
            },
        )

        get_or_create(
            db,
            ApprovalDelegation,
            delegator_id=users["manager"].id,
            delegatee_id=users["admin"].id,
            defaults={
                "start_date": now - timedelta(days=1),
                "end_date": now + timedelta(days=4),
                "reason": "Manager unavailable during audit closure week.",
                "is_active": True,
            },
        )

        get_or_create(
            db,
            ApprovalHistory,
            approval_id=seeded_approvals[0].id,
            action_by=users["manager"].id,
            defaults={
                "action": "approve",
                "comment": "Manager review completed, pending admin approval.",
            },
        )

        get_or_create(
            db,
            Document,
            file_name="compliance-pack.pdf",
            task_id=seeded_tasks[0].id,
            defaults={
                "file_path": "uploads/documents/demo/compliance-pack.pdf",
                "version": 1,
                "uploaded_by": users["employee"].id,
            },
        )

        get_or_create(
            db,
            Comment,
            task_id=seeded_tasks[0].id,
            user_id=users["manager"].id,
            defaults={
                "content": "Please prioritize the access review section before end of day.",
                "is_internal": False,
            },
        )

        notifications = [
            (users["employee"].id, "High priority task SLA is due in 20 hours.", "task", "high"),
            (users["admin"].id, "Approval escalation pending review.", "escalation", "urgent"),
            (users["auditor"].id, "New audit log entries available.", "audit", "normal"),
        ]
        for user_id, message, notification_type, priority in notifications:
            get_or_create(
                db,
                Notification,
                user_id=user_id,
                message=message,
                defaults={
                    "notification_type": notification_type,
                    "priority": priority,
                    "is_read": False,
                },
            )

        activity_rows = [
            (users["manager"].id, "TASK_CREATED", "TASK", seeded_tasks[0].id),
            (users["employee"].id, "DOCUMENT_UPLOADED", "DOCUMENT", 1),
            (users["admin"].id, "APPROVAL_ESCALATED", "APPROVAL", seeded_approvals[1].id),
        ]
        for user_id, action, entity_type, entity_id in activity_rows:
            get_or_create(
                db,
                ActivityLog,
                user_id=user_id,
                action=action,
                entity_type=entity_type,
                entity_id=entity_id,
            )

        audit_rows = [
            (users["manager"].id, "TASK", "create", seeded_tasks[0].id, None, {"title": seeded_tasks[0].title}),
            (users["admin"].id, "APPROVAL", "escalate", seeded_approvals[1].id, {"is_escalated": False}, {"is_escalated": True}),
            (users["employee"].id, "DOCUMENT", "upload", seeded_tasks[0].id, None, {"file_name": "compliance-pack.pdf"}),
            (users["auditor"].id, "SLA", "view", None, None, {"filter": "breached"}),
        ]
        for user_id, module_name, action_type, record_id, old_data, new_data in audit_rows:
            get_or_create(
                db,
                AuditLog,
                user_id=user_id,
                module_name=module_name,
                action_type=action_type,
                record_id=record_id,
                defaults={
                    "action": action_type,
                    "entity": module_name,
                    "entity_id": record_id,
                    "old_data": old_data,
                    "new_data": new_data,
                    "ip_address": "127.0.0.1",
                    "user_agent": "Seed Script",
                },
            )

        db.commit()

        print("Seed data added successfully.")
        print("Demo login users:")
        for user in users.values():
            print(f"- {user.email} / {PASSWORD} ({user.role})")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
