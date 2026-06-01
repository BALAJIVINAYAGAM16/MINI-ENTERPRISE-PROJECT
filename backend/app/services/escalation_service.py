# services/escalation_service.py

from app.models.approval_escalation import ApprovalEscalation


def escalate_approval(
    db,
    approval_id,
    escalated_from,
    escalated_to,
    reason
):

    escalation = ApprovalEscalation(
        approval_id=approval_id,
        escalated_from=escalated_from,
        escalated_to=escalated_to,
        reason=reason,
        escalation_level=1,
        status="PENDING"
    )

    db.add(escalation)
    db.commit()
    db.refresh(escalation)

    return escalation