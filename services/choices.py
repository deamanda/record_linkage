from enum import Enum


class MatchingStatus(str, Enum):
    """Selecting a filter for matched products"""

    option1 = "not matched"
    option2 = "matched"
    option3 = "deferred"


class DealerPriceStatus(str, Enum):
    """Selecting a filter for dealer products"""

    option1 = "not matched"
    option2 = "matched"
    option3 = "deferred"
    option4 = "not processed"


class SortedField(str, Enum):
    option1 = "ascending time"
    option2 = "descending time"
    option3 = "ascending price"
    option4 = "descending price"
