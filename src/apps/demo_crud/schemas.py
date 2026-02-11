from ninja import Schema
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ItemIn(Schema):
    name: str
    price: Decimal
    description: Optional[str] = None
    is_active: bool = True


class ItemOut(Schema):
    id: int
    name: str
    price: Decimal
    description: Optional[str]
    is_active: bool
    created_time: datetime
    updated_time: datetime
