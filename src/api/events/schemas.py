import sqlmodel
from pydantic import BaseModel
from typing import List, Optional
from timescaledb import TimescaleModel
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, tzinfo
from sqlalchemy import DateTime

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventSchema(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    page : Optional[str] = ""
    description : Optional[str] = ""
    created_at : datetime = Field(default_factory=get_utc_now, sa_type=DateTime(timezone=True), nullable=False)
    updated_at : datetime = Field(default_factory=get_utc_now, sa_column_kwargs={"onupdate": get_utc_now}, sa_type=DateTime(timezone=True), nullable=False)


class EventListSchema(SQLModel):
    results : List[EventSchema]
    count : int


class EventCreateSchema(SQLModel):
    page : str
    description : Optional[str] = Field(default="")

class EventUpdateSchema(SQLModel):
    description : Optional[str] = Field(default="")


