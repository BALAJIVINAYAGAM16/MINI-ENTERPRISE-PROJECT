# services/sla_service.py

from datetime import datetime, timedelta

from app.models.sla_tracking import SLATracking


def calculate_due_time(start_time, allowed_hours):
    return start_time + timedelta(hours=allowed_hours)


def create_sla_tracking(
    db,
    module_name,
    record_id,
    sla_rule
):

    start_time = datetime.utcnow()

    due_time = calculate_due_time(
        start_time,
        sla_rule.allowed_hours
    )

    tracking = SLATracking(
        module_name=module_name,
        record_id=record_id,
        sla_rule_id=sla_rule.id,
        start_time=start_time,
        due_time=due_time,
        status="ACTIVE"
    )

    db.add(tracking)
    db.commit()
    db.refresh(tracking)

    return tracking