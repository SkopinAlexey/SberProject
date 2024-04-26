from pydantic import BaseModel

class Building(BaseModel):

    objId: int
    shortAddr: str
    objCommercNm: str

    def __str__(self):
        return str(self.objId) + ' ' + self.shortAddr + ' ' + self.objCommercNm