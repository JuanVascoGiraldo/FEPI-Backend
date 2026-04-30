from enum import IntEnum


class OrderStatus(IntEnum):
    OPEN = 1        # order is being built by the waiter
    IN_PROCESS = 2  # at least one item is being prepared
    READY = 3       # all items delivered; waiting for payment
    PAYING = 4      # payment in progress (partial payments allowed)
    PAID = 5        # fully settled
    CANCELLED = 6   # cancelled before any payment
