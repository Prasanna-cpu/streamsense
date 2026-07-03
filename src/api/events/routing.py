
from fastapi import APIRouter, FastAPI, Depends, Query, HTTPException
from sqlmodel import select, Session
from .schemas import EventListSchema, EventSchema, EventCreateSchema, EventUpdateSchema, get_utc_now
from ..db.session import get_session
from ..db.config import DATABASE_URL
router = APIRouter()

@router.get("/", response_model=EventListSchema)
async def read_events(session : Session = Depends(get_session)) -> EventListSchema:
    query = select(EventSchema).order_by(EventSchema.id.desc()).limit(10)
    results = session.exec(query).all()
    return EventListSchema(results=results, count=len(results))


@router.get("/{event_id}", response_model=EventSchema)
async def get_event(event_id : int, session : Session = Depends(get_session)) -> EventSchema:
    query = select(EventSchema).where(EventSchema.id == event_id)
    result = session.exec(query).one()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result

@router.post("/create", response_model=EventSchema)
async def create_event(payload : EventCreateSchema, session : Session = Depends(get_session)) -> EventSchema:
    data = payload.model_dump()
    obj = EventSchema.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.put("/update/{event_id}", response_model=EventSchema)
async def update_event(event_id : int, payload : EventUpdateSchema, session : Session = Depends(get_session)) -> EventSchema:
    query = select(EventSchema).where(EventSchema.id == event_id)
    obj = session.exec(query).one()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    data = payload.model_dump()
    for k , v in data.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


