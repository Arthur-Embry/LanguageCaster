from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import requests
from bs4 import BeautifulSoup
#security key for openai
openai.api_key = "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"


class gpt_params(BaseModel):
    engine: Union[str,None]="text-davinci-003",
    prompt: Union[str,None]="",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 50
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def gpt_run(item: gpt_params):
    
    gpt_iter = openai.Completion.create(
        engine=item.engine,
        prompt=item.prompt,
        temperature=item.temperature,
        max_tokens=item.max_tokens,
        top_p=item.top_p,
        frequency_penalty=item.frequency_penalty,
        presence_penalty=item.presence_penalty,
        stream=True
    )
    #yield response
    def iterfile():  # 
        for i in gpt_iter:
            yield str(i.choices[0].text)
    return StreamingResponse(iterfile(), media_type="text/plain")



class diffuse_params(BaseModel):
    prompt: Union[str,None]="digital art"
    n: Union[int,None] = 1
    size: Union[str,None] = "1024x1024"
    response_format: Union[str,None] = "b64_json"

def diffuse_run(item: diffuse_params):

    #default engine
    res=openai.Image.create(
        prompt=item.prompt,
        n=item.n,
        size=item.size,
        response_format=item.response_format
    )
    #return response
    return res



class proxy_params(BaseModel):
    url: Union[str,None]=""
    acceptlanguage: Union[str,None]="en-US,en;q=0.9"
    dnt: Union[str,None] = "1"
    secchua: Union[str,None] = '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"'
    secchuamobile: Union[str,None] = '?0'
    secchuaplatform: Union[str,None] = '"Windows"'
    secfetchdest: Union[str,None] = 'empty'
    useragent: Union[str,None] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'

def proxy_run(item: proxy_params):

    #set headers
    req_headers = {
    'accept-language':item.acceptlanguage,
    'dnt':item.dnt,
    'sec-ch-ua':item.secchua,
    'sec-ch-ua-mobile':item.secchuamobile,
    'sec-ch-ua-platform':item.secchuaplatform,
    'sec-fetch-dest':item.secfetchdest,
    'user-agent':item.useragent
    }

    #get and parse
    req = requests.get(item.url, headers=req_headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    #return response
    return soup.html.prettify()