# jobs/sla_monitor.py

from datetime import datetime

from app.models.sla_tracking import SLATracking
from app.models.approval import Approval
from app.models.task import Task


def monitor_sla_breaches(db):

    active_records = db.query(
        SLATracking
    ).filter(
        SLATracking.status == "ACTIVE"
    ).all()

    now = datetime.utcnow()

    for record in active_records:

        if now > record.due_time:

            record.status = "BREACHED"

            record.breach_reason = (
                "SLA due time exceeded"
            )

            if record.module_name == "TASK":
                task = db.query(Task).filter(Task.id == record.record_id).first()
                if task:
                    task.sla_status = "BREACHED"
                    task.is_sla_breached = True
                    task.sla_due_time = record.due_time

            if record.module_name == "APPROVAL":
                approval = db.query(Approval).filter(Approval.id == record.record_id).first()
                if approval:
                    approval.sla_status = "BREACHED"
                    approval.sla_due_time = record.due_time

    db.commit()
