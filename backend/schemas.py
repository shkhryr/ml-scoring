from pydantic import BaseModel


class Account(BaseModel):
    client_id: int
    gender: str
    age: str
    marital_status: str
    job_position: str
    credit_sum: str
    credit_month: int
    tariff_id: str
    score_shk: str
    education: str
    living_region: str
    monthly_income: int
    credit_count: str
    overdue_credit_count: int


class Result(BaseModel):
    client_id: int
    percentage: float
    response: str


