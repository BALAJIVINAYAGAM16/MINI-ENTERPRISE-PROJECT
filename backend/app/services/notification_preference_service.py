def update_notification_preferences(
    db,
    preference,
    payload
):

    for key, value in payload.dict().items():
        setattr(preference, key, value)

    db.commit()
    db.refresh(preference)

    return preference