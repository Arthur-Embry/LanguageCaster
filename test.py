from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
from typing import Callable

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def expose(endpoint,service):
    service_import=__import__(service+'_services')
    function_import=service_import.__dict__[endpoint+'_run']
    function_params=service_import.__dict__[endpoint+'_params']
    
    print(function_params)
    @app.post("/"+endpoint)
    def endpoint_post(item: function_params):
        for i in item:
            if type(i[1])==tuple:
                setattr(item, i[0].split("=")[0], i[1][0])
        return function_import(item)

    @app.get("/"+endpoint)
    def endpoint_get(item: function_params):
        for i in item:
            if type(i[1])==tuple:
                setattr(item, i[0].split("=")[0], i[1][0])
        return function_import(item)
expose("foo","testing")
expose("bar","testing")

service="testing"
endpoint="foo"
service_import=__import__(service+'_services')
function_import=service_import.__dict__[endpoint+'_run']
function_params=service_import.__dict__[endpoint+'_params']
"""
out_par=list()
for i in function_params.__dict__['__fields__']:
    name=function_params.__dict__['__fields__'][i].name
    type_spec=function_params.__dict__['__fields__'][i].type_
    default=function_params.__dict__['__fields__'][i].default
    inject={name: type_spec}
    out_par.append(*inject)
print(*out_par)

test=(item_id: str, needy: str, skip: int = 0, limit: Union[int, None] = None)"""

foo=Callable[[int, int],int]
print(foo)