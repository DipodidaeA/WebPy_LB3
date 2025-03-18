from fastapi import Query
from pydantic import BaseModel

class DTO(BaseModel):
    id: int = Query(ge=0)
    name: str = Query(min_length=3, max_length=10)
    dd: int =  Query(ge=0, lt=32)
    mm: int = Query(ge=0, lt=13)
    yyyy: int = Query(ge=1950, lt=2027)
    morning: int = Query(ge=-50, lt=51)
    noon: int = Query(ge=-50, lt=51)
    night: int = Query(ge=-50, lt=51)