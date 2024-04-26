from pydantic import BaseModel

class Developer(BaseModel):

    id: int
    devInn: str
    name: str

    def __str__(self):
        return self.devInn + ' ' + self.name

