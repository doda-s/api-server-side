from pydantic import BaseModel

class UserProgress(BaseModel):
    trust: int
    number_of_cases_won: int
    number_of_lost_cases: int