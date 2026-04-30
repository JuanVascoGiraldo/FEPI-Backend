from enum import IntEnum


class OrderItemStatus(IntEnum):
    PENDING = 1     # ordered, waiting to be prepared
    PREPARING = 2   # kitchen is working on it
    READY = 3       # ready to be served
    DELIVERED = 4   # delivered to the table
    CANCELLED = 5   # cancelled before preparation
