from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Union
from pydantic import BaseModel
import openai
import classifier_services
import creator_services
import generator_services
import image_services
import main_services
import mutator_services
import proxy_services
import search_services
#security key for openai
openai.api_key = "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"

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/operatordocs", response_class=HTMLResponse)
async def read_docs():
    with open('static/index.html') as f:
        lines = f.readlines()
        print(lines)
    return ''.join(lines)

def expose(endpoint,service):
    #import the service and define the function and parameters
    service_import=__import__(service+'_services')
    function_import=service_import.__dict__[endpoint+'_run']
    function_params=service_import.__dict__[endpoint+'_params']
    
    #define the post methods for the endpoint
    @app.post("/"+endpoint)
    def endpoint_post(item: function_params):
        #catch special case of default parameters changing from string to tuple
        for i in item:
            if type(i[1])==tuple:
                setattr(item, i[0].split("=")[0], i[1][0])
        return function_import(item)

    #add temporary storage and fields to iterate over class
    get_conversion=""
    get_builder=""
    fields=function_params.__dict__['__fields__']
    #iterate over template class
    for i in fields:
        name=fields[i].name
        type_spec=str(fields[i].type_).split("'")[1].split("'")[0]
        default=fields[i].default
        #catch special case of default parameters changing from string to tuple, and add """ to string parameters
        if type(default)==tuple:
            default=default[0]
        if type_spec == "str":
            default="\"\"\""+default+"\"\"\""
        #build function list
        get_conversion+=f"""{name}: Union[{type_spec}, None] = {default},"""
        #build item class from function list
        get_builder+=f"""item.{name} = {name}\n    """
    #trim trailing comma
    get_conversion=get_conversion[:-1]
    #execute the function to expose the get method
    exec(f"""@app.get("/{endpoint}")
def {endpoint}_get({get_conversion}):
    item = __import__('{service}_services').__dict__['{endpoint}_params']
    {get_builder}
    return {service}_services.{endpoint}_run(item)""")

@app.get("/")
def read_root():
    return {"Hello": "World"}


expose("introduction","classifier")
expose("conclusion","classifier")
expose("image_prompt","classifier")

### throws error TODO: fix special types
#expose("paragraph","creator")
expose("story","creator")

expose("title","generator")
expose("header","generator")
expose("subsection","generator")
expose("bullet_points","generator")
expose("noted_bullets","generator")

expose("image_search","image")
expose("image_edit","image")
expose("open_diffuse","image")
expose("text_inversion","image")
expose("interpolate","image")
#TODO implement opencv functions
#expose("split","image")
#expose("track","image")

expose("gpt","main")
expose("diffuse","main")
expose("proxy","main")

expose("listfull","mutator")
expose("listless","mutator")
expose("anchor","mutator")

expose("proxy_links","proxy")
expose("proxy_paragraphs","proxy")
expose("proxy_chromium","proxy")
expose("html_reduction","proxy")

expose("fact_reduction","search")
expose("sort","search")
