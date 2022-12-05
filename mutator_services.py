from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import re

#security key for openai
openai.api_key = "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"

class listfull_params(BaseModel):
    text: Union[str,None]="filler"
def listfull_run(item: listfull_params):
    pass

class listless_params(BaseModel):
    text: Union[str,None]="filler"
def listless_run(item: listless_params):
    pass

class anchor_params(BaseModel):
    text: Union[str,None]="filler"
def anchor_run(item: anchor_params):
    pass
