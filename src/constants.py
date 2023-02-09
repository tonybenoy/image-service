import enum


class IMAGE_STATUS(enum.Enum):
    UNPROCESSED = 0
    PROCESSING = 1
    PROCESSED = 2
    FAILED = 3
