from fastapi.responses import StreamingResponse
from typing import Union, List
from pydantic import BaseModel
import openai
import re
#security key for openai
openai.api_key = "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"

### throws error TODO: fix special types
"""
class paragraph_params(BaseModel):
    headers=Union[List[str],None]=["header1","header2","header3","header4"],
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 50
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

#TODO: check list is valid with post/get frameworks
def paragraph_run(item: paragraph_params):
    print(item.list)
    prompt="Blog Title: " + item.title + "\n\nBlog Point: "
    
    for i in range(len(item.headers)):
        prompt+="\n"+str(i+1)+") " + item.headers[i]
    prompt+="\n\nFor each Blog Point write a concise paragraph (3-5 sentences max).\n\n1) " + item.headers[0] + ":"
    gpt_iter = openai.Completion.create(
        engine=item.engine,
        prompt=prompt,
        temperature=item.temperature,
        max_tokens=item.max_tokens,
        top_p=item.top_p,
        frequency_penalty=item.frequency_penalty,
        presence_penalty=item.presence_penalty,
        stream=True
    )
    #yield response
    def iterfile():  #
        yield "1) " + item.headers[0] + ":"
        for i in gpt_iter:
            yield str(i.choices[0].text)
        
    return StreamingResponse(iterfile(), media_type="text/plain")
"""

class story_params(BaseModel):
    target_header: Union[str,None]="header1",
    target_paragraph: Union[str,None]="paragraph1",
    title: Union[str,None]="Test Title",
    contents: Union[str,None]="paragraph1",
    tense_word: Union[str,None]="we",
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 50
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def story_run(item: story_params):
    gpt_iter = openai.Completion.create(
        engine=item.engine,
        prompt="Given the subject is : " + item.title + ", rewrite the Blog Point: \n\n" + item.target_header +"\n\n"+item.target_paragraph+ "\n\n above as a personal story using: " + item.tense_word + ".",
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

#TODO: create opinion function