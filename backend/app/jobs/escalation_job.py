# jobs/escalation_job.py

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sla_tracking import SLATracking
from app.models.sla_rule import SLARule
from app.models.approval_escalation import ApprovalEscalation
from app.models.approval import Approval


def run_escalation_job(db: Session):

    breached_records = db.query(
        SLATracking
    ).filter(
        SLATracking.status == "BREACHED"
    ).all()

    for record in breached_records:

        # Only approvals are escalated
        if record.module_name != "APPROVAL":
            continue

        approval = db.query(Approval).filter(
            Approval.id == record.record_id
        ).first()

        if not approval:
            continue

        # Skip if already escalated
        if approval.is_escalated:
            continue

        sla_rule = db.query(SLARule).filter(
            SLARule.id == record.sla_rule_id
        ).first()

        if not sla_rule:
            continue

        if not sla_rule.escalation_enabled:
            continue

        escalation = ApprovalEscalation(
            approval_id=approval.id,

            escalated_from=approval.current_escalation_to or approval.requested_by,

            # Example escalation target
            escalated_to=1,

            reason="Automatic SLA escalation",

            escalation_level=1,

            status="PENDING",

            escalated_at=datetime.utcnow()
        )

        db.add(escalation)

        approval.is_escalated = True

        approval.current_escalation_to = 1

        record.status = "ESCALATED"

    db.commit()

    print("Escalation job completed")
