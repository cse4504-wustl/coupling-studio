from dataclasses import dataclass


@dataclass(frozen=True)
class ReturnReceipt:
    isbn: str
    days_late: int
    fine: float
    new_balance: float
