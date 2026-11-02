"""
SARAS ATLAS — Digital Twin State Router.
Exposes multi-echelon network topology, fulfillment graph, and real-time inventory levels.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.domain.twin.state import DigitalTwinState

router = APIRouter(prefix="/twin", tags=["Digital Twin State"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/topology")
def get_topology(session: Session = Depends(get_db)):
    """Returns the multi-echelon enterprise network topology and fulfillment graph."""
    twin = DigitalTwinState(session=session)
    return twin.get_topology()


@router.get("/inventory-summary")
def get_inventory_summary(session: Session = Depends(get_db)):
    """Returns aggregated SKU inventory balances across warehouses and pipeline."""
    twin = DigitalTwinState(session=session)
    items = twin.get_inventory_summary()
    tot_on_hand = sum(i.get("total_on_hand", 0) for i in items)
    tot_available = sum(i.get("total_available", 0) for i in items)
    tot_in_transit = sum(i.get("total_in_transit", 0) for i in items)
    return {
        "total_skus": len(items),
        "total_on_hand_units": tot_on_hand,
        "total_available_units": tot_available,
        "total_in_transit_units": tot_in_transit,
        "items": items,
    }
