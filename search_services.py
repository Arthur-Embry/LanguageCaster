import requests
import re
from typing import Union
from pydantic import BaseModel
headers = {"Authorization": "Bearer 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"}


class fact_reduction_params(BaseModel):
    url: Union[str,None]=""
    text: Union[str,None]=""
    factor: Union[int,None]=1

def fact_reduction_run(item: fact_reduction_params):
    def query_facts(payload):
        try:
            response = requests.post("https://api-inference.huggingface.co/models/bigscience/bloom", headers=headers, json=payload)
            print("Testing..." + response.text)

            return response.json()
        except Exception as e:
            print(e)
            print(response)
            return response.text

    facts=[]
    #split content into chunks of 10 sentences
    sentences = item.text.split(".")
    chunks = [sentences[i:i+item.factor] for i in range(0, len(sentences), item.factor)]

    #query each chunk for a summary
    i=0
    for chunk in chunks:
        i+=1
        output = query_facts({
            "inputs": ".".join(chunk)+"\nTL;DR (Single Sentence):"
        })[0]['generated_text'].split("TL;DR (Single Sentence):")[1]

        #while .?! not in output, keep querying
        while len(re.split('[.!?]',output))<2:
            output = query_facts({
                "inputs": ".".join(chunk)+"\nTL;DR (Single Sentence):"+output
            })[0]['generated_text'].split("TL;DR (Single Sentence):")[1]

        print(re.split('[.!?]',output)[0])
        facts.append(re.split('[.!?]',output)[0])
    return {"url":item.url,"facts":facts,"text":item.text}


class sort_params(BaseModel):
    content: Union[str,None]=""
    quantity: Union[int,None]=1
    search_q: Union[str,None]=""
def sort_run(item: sort_params):
    def query_sort(payload):
        response = requests.post("https://api-inference.huggingface.co/models/facebook/bart-large-mnli", headers=headers, json=payload)
        return response.json()

    output = query_sort({
        "inputs": item.search_q,
        "parameters": {"candidate_labels": item.content},
    })
    return({"labels":output["labels"][0:item.quantity],"scores":output["scores"][0:item.quantity]})
