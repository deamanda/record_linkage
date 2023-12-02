from pydantic import BaseModel


class MatchedCount(BaseModel):
    matched: int | None
    not_matched: int | None
    deferred: int | None
    total_matching: int | None
    accuracy: float | None
