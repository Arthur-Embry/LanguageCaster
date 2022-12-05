from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai

#security key for openai
openai.api_key = "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"

class conclusion_params(BaseModel):
    version: Union[str, None] = "final paragraph concludes 200 words"
    title: Union[str, None] = "Blog Article"
    ctx: Union[str, None] = ""
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def conclusion_run(item: conclusion_params):
    
    #switch case
    if item.version == "sales pitch":
        prompt = item.ctx + "\n\nGive me a sales pitch for " + item.title + ":"
    elif item.version == "why I should care":
        prompt = item.ctx + "\n\nTell me why I should care about this article " + item.title + "?" 
    elif item.version == "should the world care":
        prompt = item.ctx + "\n\nWhy should the world care about this " + item.title + "?" 
    elif item.version == "final paragraph concludes personal":
        prompt = "Blog Article:\n\n" + item.ctx + "\n\nWrite a final paragraph to conclude the Blog Article with a personal touch:"
    elif item.version == "final paragraph concludes":
        prompt = "Blog Article:\n\n" + item.ctx + "Write a final paragraph to conclude the Blog Article:"
    elif item.version == "final paragraph concludes few":
        prompt = "Blog Article:\n\n" + item.ctx + "\n\nWrite a final paragraph to conclude the Blog Article in as few words as possible:"
    elif item.version == "final paragraph concludes 200 words":
        prompt = "Blog Article:\n\n" + item.ctx + "\n\nWrite a final paragraph, no more than 200 words, to conclude the Blog Article:"
    else:
        prompt = "Blog Article:\n\n" + item.ctx + "\n\nWrite a final paragraph, no more than 200 words, to conclude the Blog Article:"
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
        for i in gpt_iter:
            yield str(i.choices[0].text)
    return StreamingResponse(iterfile(), media_type="text/plain")


class introduction_params(BaseModel):
    title: Union[str, None] = "title query"
    ctx: Union[str, None] = ""
    delimeter: Union[str, None] = "###"
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

#TODO: finish implementation phase 2 of tree (validate <b> tags and trim)
def introduction_run(item: introduction_params):

    #yield response
    def iterfile():  #
        validation_stage=0
        while validation_stage!=3:
            if validation_stage==0:
                prompt = "Blog Article:\n\n" + item.ctx + "\n\nWrite a 3 sentence introduction to the above in the form\n1. A final sales pitch, no more than 200 words, to conclude the Blog Article\n2. A paragraph that answers the Blog Articles question " + item.title + "\n3. A lead on\n\nIntroduction:\n1. A final sales pitch, no more than 200 words, to conclude the Blog Article:"
                check_statement_1=""
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
                for i in gpt_iter:
                    check_statement_1+=str(i.choices[0].text)
                    yield str(i.choices[0].text)
                try:
                    intro_1= check_statement_1.split("2. A paragraph that answers the Blog Articles question " + item.title + ":")[0]
                    print(intro_1)
                    pre_intro_2= check_statement_1.split("2. A paragraph that answers the Blog Articles question " + item.title + ":")[1].split("3. A lead on:")[0]
                    print(pre_intro_2)
                    intro_3= check_statement_1.split("A paragraph that answers the Blog Articles question " + item.title + ":")[1].split("3. A lead on:")[1]
                    print(intro_3)
                    validation_stage=1
                    yield item.delimeter
                except:
                    pass
            elif validation_stage==1:
                check_statement_2=""
                prompt = "Version 1:\n\n<div class='v1>" + pre_intro_2 + "</div>\n\nVersion 2 (Version 1 with <b> tags surrounding a 3-5 word snippet answering the question " + item.title + "):\n\n<div class='v2'>"
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
                check_statement_2+="<div>"
                for i in gpt_iter:
                    check_statement_2+=str(i.choices[0].text)
                    yield str(i.choices[0].text)
                if "<b>" in check_statement_2 and "</b>" in check_statement_2:
                    intro_2=check_statement_2
                    validation_stage=2
                    yield item.delimeter
            elif validation_stage==2:
                yield "<div>"+intro_1+"</div>"+intro_2+"<div>"+intro_3+"</div>"
                validation_stage=3
    return StreamingResponse(iterfile(), media_type="text/plain")


class image_prompt_params(BaseModel):
    title: Union[str, None] = "Blog Article"
    appension: Union[str, None] = ", digital art"
    short: Union[bool, None] = True
    delimeter: Union[str, None] = "###"
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 50
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0


def image_prompt_run(item: image_prompt_params):
    if item.short:
        prompt = "Write a bulleted single keyword list for the article in the form\n-keyword\n-keyword\n-keyword\netc.\nFor example, if are given a article with the title " + item.title + ",\nThe bulleted keyword list would be\n\n-"
    else:
        prompt = "A great example of a popular and striking image related to the article " + item.title + " is a"
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
        short_temp=""
        for i in gpt_iter:
            short_temp+=str(i.choices[0].text)
            yield str(i.choices[0].text)
        if item.short:
            yield item.delimeter
            yield short_temp.split("-")[0].strip()
    return StreamingResponse(iterfile(), media_type="text/plain")