from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import re

#security key for openai
openai.api_key = "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"


class title_params(BaseModel):
    delimiter: Union[str,None]="###",
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 50
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0


def title_run(item: title_params):
    gpt_iter = openai.Completion.create(
        engine=item.engine,
        prompt="3 great article/blog titles:\n1.",
        temperature=item.temperature,
        max_tokens=item.max_tokens,
        top_p=item.top_p,
        frequency_penalty=item.frequency_penalty,
        presence_penalty=item.presence_penalty,
        stream=True
    )
    #yield response
    def iterfile():  #
        titles="" 
        yield "1."
        for i in gpt_iter:
            titles+=str(i.choices[0].text)
            yield str(i.choices[0].text)
        yield item.delimiter
    
    return StreamingResponse(iterfile(), media_type="text/plain")


class header_params(BaseModel):
    title: Union[str,None]="Test Title"
    count: Union[int,None]=4
    delimiter: Union[str,None]="###",
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0


#TODO: add branches for output
def header_run(item: header_params):
    def iterfile():

        header_ref=""
        gpt_iter = openai.Completion.create(
            engine=item.engine,
            prompt="A quality lead-in sentence to start the essay \""+item.title+"\":",
            temperature=item.temperature,
            max_tokens=item.max_tokens,
            top_p=item.top_p,
            frequency_penalty=item.frequency_penalty,
            presence_penalty=item.presence_penalty,
            stream=True
        )
        for i in gpt_iter:
            header_ref+=str(i.choices[0].text)
            yield str(i.choices[0].text)
        yield item.delimiter
        gpt_iter = openai.Completion.create(
            engine=item.engine,
            prompt="A quality 6 sentence opening paragraph about the essay "+item.title+":\n\n" +header_ref,
            temperature=item.temperature,
            max_tokens=item.max_tokens,
            top_p=item.top_p,
            frequency_penalty=item.frequency_penalty,
            presence_penalty=item.presence_penalty,
            stream=True
        )
        for i in gpt_iter:
            header_ref+=str(i.choices[0].text)
            yield str(i.choices[0].text)
        gpt_iter = openai.Completion.create(
            engine=item.engine,
            prompt="A quality 6 sentence opening paragraph about the essay "+item.title+":\n\n" +header_ref,
            temperature=item.temperature,
            max_tokens=item.max_tokens,
            top_p=item.top_p,
            frequency_penalty=item.frequency_penalty,
            presence_penalty=item.presence_penalty,
            stream=True
        )
        for i in gpt_iter:
            header_ref+=str(i.choices[0].text)
            yield str(i.choices[0].text)
        yield item.delimiter
        gpt_iter = openai.Completion.create(
            engine=item.engine,
            prompt="The following is a topic overview:\n\n" +header_ref+"\n\n" + str(item.count) +" interesting questions about this topic are:\n\n1.",
            temperature=item.temperature,
            max_tokens=item.max_tokens,
            top_p=item.top_p,
            frequency_penalty=item.frequency_penalty,
            presence_penalty=item.presence_penalty,
            stream=True
        )
        yield "1."
        for i in gpt_iter:
            yield str(i.choices[0].text)
    
    return StreamingResponse(iterfile(), media_type="text/plain")




class subsection_params(BaseModel):
    header: Union[str,None]=""
    tense_word: Union[str,None]="we"
    notes:  Union[str,None]=""
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0
def subsection_run(item: subsection_params):
    def iterfile():

        subsection=""
        gpt_iter = openai.Completion.create(
            engine=item.engine,
            prompt="The following is a blog section: \n\n" + item.body + "\n\nTo continue the section with a new paragraph, one good sentence starter using the word " + item.tense_word + " is:",
            temperature=item.temperature,
            max_tokens=item.max_tokens,
            top_p=item.top_p,
            frequency_penalty=item.frequency_penalty,
            presence_penalty=item.presence_penalty,
            stream=True
        )
        for i in gpt_iter:
            subsection+=str(i.choices[0].text)
            yield str(i.choices[0].text)
        gpt_iter = openai.Completion.create(
            engine=item.engine,
            prompt="notes:\n" +item.notes + "body:\n" + item.header +"\n"+subsection,
            temperature=item.temperature,
            max_tokens=item.max_tokens,
            top_p=item.top_p,
            frequency_penalty=item.frequency_penalty,
            presence_penalty=item.presence_penalty,
            stream=True
        )
        for i in gpt_iter:
            subsection+=str(i.choices[0].text)
            yield str(i.choices[0].text)


    return StreamingResponse(iterfile(), media_type="text/plain")


"""                "Given the following context:\n" +
                body_text +
                '.\nThis is a quality 3 point concept list for "' +
                document.querySelector("#header" + String(i + 1)).innerText +
                '" section in the article "' +
                title.value +
                '":\n\n1.',"""
class bullet_points_params(BaseModel):
    current_paragraph: Union[str,None]=""
    body: Union[str,None]=""
    current_header: Union[str,None]=""
    title: Union[str,None]="Test Title"
    delimiter: Union[str,None]="###"
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0
def bullet_points_run(item: bullet_points_params):
    pass

"""            while (!lead_in.includes("</h3>") || lead_in.includes("Lead in") || lead_in.includes("lead in")) {
                lead_in = await call2(
                    current_body.innerText + '\n\n<div class="list lead in sentence">\n<h3>',
                    30,
                    current_body
                );
                current_body.innerHTML = replacement
            }
            lead_in = lead_in.split("</h3>")[0]
  
            list = ""
            while (list == "") {
                while (list.split("</li>").length < 3 || !list.includes("</ul>") || !list.includes("</li>")) {
                    list = await call2(
                        "notes:\n" +
                        document.querySelector("#notes_edit").innerText +
                        "body:\n" +
                        current_header.innerText +
                        "\n" + lead_in + "\n" +
                        current_body.innerText + "<ul><li>",
                        150,
                        current_body
                    );
                    current_body.innerHTML = replacement
                }
                res = ""
                list.split("</ul>")[0].split(/<li>|<\/li>/).filter(word => word.length > 3).forEach(e => res += "<li>" + e + "</li>")
                list = res
            }"""
class noted_bullets_params(BaseModel):
    current_paragraph: Union[str,None]=""
    body: Union[str,None]=""
    current_header: Union[str,None]=""
    title: Union[str,None]="Test Title"
    delimiter: Union[str,None]="###"
    notes: Union[str,None]=""
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0
def noted_bullet_run(item: noted_bullets_params):
    pass
