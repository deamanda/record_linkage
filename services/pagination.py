import math

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    size: int
    total_pages: int


def pagination(page, size, value):
    offset_min = (page - 1) * size
    offset_max = page * size
    paginated_value = value[offset_min:offset_max]
    pagination_info = {
        "page": page,
        "size": size,
        "total_pages": math.ceil(len(value) / size),
    }
    return {"pagination": pagination_info, "data": paginated_value}
