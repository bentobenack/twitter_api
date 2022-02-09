
#Python
from datetime import datetime

#Pydantic
from pydantic import BaseModel
from pydantic import Field


class IDMixin(BaseModel):
    """
    ID Schema Mixin
    This Mixin is used to add a unique ID field to a schema.
    """
    
    id: int = Field(..., description="Unique ID pf document.")
    

class TimestampMixin(BaseModel):
    """
    Timestamp Mixin
    
    This Mixin is used to add to Field to a schema:
        - created_at
        - updated_at
    """
    
    created_at: datetime = Field(
        default=None, 
        description="The time the document was created."
    )
    updated_at: datetime = Field(
        default=None, 
        description="The last update of the document."
    )