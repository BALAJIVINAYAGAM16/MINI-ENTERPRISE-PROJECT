from app.models.approval_delegation import ApprovalDelegation


def create_delegation(
    db,
    payload,
    delegator_id
):

    delegation = ApprovalDelegation(
        delegator_id=delegator_id,
        delegatee_id=payload.delegatee_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason
    )

    db.add(delegation)
    db.commit()
    db.refresh(delegation)

    return delegation