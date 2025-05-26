from pydantic import BaseModel

class Progress(BaseModel):
    trust: int = 0
    number_of_cases_won: int = 0
    number_of_lost_cases: int = 0