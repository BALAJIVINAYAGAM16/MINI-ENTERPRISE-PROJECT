from app.models.audit_log import AuditLog


def create_audit_log(
    db,
    user_id,
    module_name,
    action_type,
    record_id=None,
    old_data=None,
    new_data=None,
    ip_address=None,
    user_agent=None
):

    log = AuditLog(
        user_id=user_id,
        module_name=module_name,
        action_type=action_type,
        record_id=record_id,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip_address,
        user_agent=user_agent
    )

    db.add(log)
    db.commit()

    return log


def log_action(
    db,
    user_id,
    action,
    entity,
    entity_id=None,
    old_data=None,
    new_data=None,
    ip_address=None,
    user_agent=None
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        module_name=str(entity).upper() if entity else None,
        action_type=action,
        record_id=entity_id,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip_address,
        user_agent=user_agent
    )

    db.add(log)
    db.commit()

    return log


def get_audit_logs(db, user):
    query = db.query(AuditLog)

    if getattr(user, "role", None) != "admin":
        query = query.filter(AuditLog.user_id == user.id)

    return query.order_by(AuditLog.created_at.desc()).all()
