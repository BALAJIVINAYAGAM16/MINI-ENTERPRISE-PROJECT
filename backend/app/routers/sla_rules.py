# routers/sla_rules.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.sla_rule import SLARule
from app.schemas.sla_rule import SLARuleCreate, SLARuleUpdate

router = APIRouter(
    prefix="/sla-rules",
    tags=["SLA Rules"]
)


@router.get("")
def list_sla_rules(db: Session = Depends(get_db)):
    return db.query(SLARule).all()


@router.post("")
def create_sla_rule(
    payload: SLARuleCreate,
    db: Session = Depends(get_db)
):
    rule = SLARule(**payload.model_dump())

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


@router.get("/{id}")
def get_sla_rule(id: int, db: Session = Depends(get_db)):
    rule = db.query(SLARule).filter(
        SLARule.id == id
    ).first()
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SLA rule not found")
    return rule


@router.put("/{id}")
def update_sla_rule(
    id: int,
    payload: SLARuleUpdate,
    db: Session = Depends(get_db)
):

    rule = db.query(SLARule).filter(
        SLARule.id == id
    ).first()

    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SLA rule not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, key, value)

    db.commit()

    return rule


@router.delete("/{id}")
def disable_sla_rule(
    id: int,
    db: Session = Depends(get_db)
):

    rule = db.query(SLARule).filter(
        SLARule.id == id
    ).first()

    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SLA rule not found")

    rule.is_active = False

    db.commit()

    return {"message": "SLA Rule disabled"}
