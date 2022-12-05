from typing import Union
from pydantic import BaseModel


class foo_params(BaseModel):
    echo: Union[str,None]="hello world"
    param2: Union[str,None]="p2"
    paramint: Union[int,None]=0
    paramfloat: Union[float,None]=0.0

def foo_run(item: foo_params):
    return item.echo+str(item.paramint)+str(item.paramfloat)+item.param2

class bar_params(BaseModel):
    echo: Union[str,None]="hello double world"

def bar_run(item: bar_params):
    return item.echo+item.echo