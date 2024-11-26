from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional

class VoidStringValidation(BaseModel):
    @field_validator("*", mode='before')
    def empty_str_to_none(cls, value):
        if value == "":
            return None
        return value

class MessageModel(VoidStringValidation):
    sourceSystem: str
    publicationTime: str
    sessionId: str
    messageId: str
    messageText: str
    messageWithContext: Optional[str] = None

    
class SessionModel(VoidStringValidation):
    sessionId: str
