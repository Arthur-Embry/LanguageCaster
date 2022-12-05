from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import re
import replicate
import os
import requests, json
from bs4 import BeautifulSoup

os.environ["REPLICATE_API_TOKEN"] = '94ee2fc285ee10a039362d6a7cf56797a2992664'
#security key for openai
openai.api_key = "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"

class image_search_params(BaseModel):
    domain: Union[str,None]="https://commons.wikimedia.org/",
    query: Union[str,None]="Hello, world!",
    tbm: Union[str,None]="isch",
    language: Union[str,None]="en",
    country: Union[str,None]="us",
    pagination: Union[str,None]="0"
    acceptlanguage: Union[str,None]="en-US,en;q=0.9"
    dnt: Union[str,None] = "1"
    secchua: Union[str,None] = '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"'
    secchuamobile: Union[str,None] = '?0'
    secchuaplatform: Union[str,None] = '"Windows"'
    secfetchdest: Union[str,None] = 'empty'
    useragent: Union[str,None] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
def image_search_run(item: image_search_params):

    headers = {
        'authority': 'www.google.com',
        "accept-language": item.acceptlanguage,
        "dnt": item.dnt,
        "sec-ch-ua": item.secchua,
        "sec-ch-ua-mobile": item.secchuamobile,
        "sec-ch-ua-platform": item.secchuaplatform,
        "sec-fetch-dest": item.secfetchdest,
        "User-Agent": item.useragent
    }

    params = {
        "q": item.query, # search query
        "tbm": "isch",                # image results
        "hl": item.language,                   # language of the search
        "gl": item.country,                   # country where search comes from
        "ijn": item.pagination                    # page number
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "lxml")
    google_images = []

    all_script_tags = soup.select("script")

    # # https://regex101.com/r/48UZhY/4
    matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
    
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)

    # https://regex101.com/r/VPz7f2/1
    matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

    # https://regex101.com/r/NnRg27/1
    matched_google_images_thumbnails = ", ".join(
        re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                   str(matched_google_image_data))).split(", ")

    thumbnails = [
        bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
    ]

    # removing previously matched thumbnails for easier full resolution image matches.
    removed_matched_google_images_thumbnails = re.sub(
        r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

    # https://regex101.com/r/fXjfb1/4
    # https://stackoverflow.com/a/19821774/15164646
    matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

    full_res_images = [
        bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
    ]
    
    for index, (metadata, thumbnail, original) in enumerate(zip(soup.select('.isv-r.PNCib.MSM1fd.BUooTd'), thumbnails, full_res_images), start=1):
        google_images.append({
            "title": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["title"],
            "link": metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")["href"],
            "source": metadata.select_one(".fxgdke").text,
            "thumbnail": thumbnail,
            "original": original
        })

    return google_images


class image_edit_params(BaseModel):
    image: Union[str,None]=""
    mask: Union[str,None]=""
    prompt: Union[str,None]="test cat"
    n: Union[int,None]=1
    size: Union[str,None]="1024x1024"
    response_format: Union[str,None]="url"
def image_edit_run(item: image_edit_params):
    res=openai.Image.create_edit(
        image=item.image,
        mask=item.mask,
        prompt=item.prompt,
        n=item.n,
        size=item.size,
        response_format=item.response_format
    )
    #return response
    return res

class open_diffuse_params(BaseModel):
    prompt: Union[str,None]="test cat"
    negative_prompt: Union[str,None]="test dog"
    width: Union[int,None]=512
    height: Union[int,None]=512
    init_image: Union[str,None]=""
    mask: Union[str,None]=""
    prompt_strength: Union[float,None]=0.5
    num_outputs: Union[int,None]=1
    num_inference_steps: Union[int,None]=100
    guidance_scale: Union[float,None]=0.5
    scheduler: Union[str,None]="K-LMS"
    seed: Union[int,None]=None

def open_diffuse_run(item: open_diffuse_params):
    model = replicate.models.get("cjwbw/stable-diffusion")
    output = model.predict(
        prompt=item.prompt,
        negative_prompt=item.negative_prompt,
        width=item.width,
        height=item.height,
        init_image=item.init_image,
        mask=item.mask,
        prompt_strength=item.prompt_strength,
        num_outputs=item.num_outputs,
        num_inference_steps=item.num_inference_steps,
        guidance_scale=item.guidance_scale,
        scheduler=item.scheduler,
        seed=item.seed
        )
    return output[0]

class text_inversion_params(BaseModel):
    image: Union[str,None]=""
    n: Union[int,None]=1
    size: Union[str,None]="1024x1024"
    response_format: Union[str,None]="url"

def text_inversion_run(item: text_inversion_params):
    res=openai.Image.create_variation(
        image=item.image,
        n=item.n,
        size=item.size,
        response_format=item.response_format
    )
    #return response
    return res


class interpolate_params(BaseModel):
    frame1: Union[str,None]=""
    frame2: Union[str,None]=""
    times_to_interpolate: Union[int,None]=4
def interpolate_run(item: interpolate_params):
    model = replicate.models.get("google-research/frame-interpolation")
    version = model.versions.get("4f88a16a13673a8b589c18866e540556170a5bcb2ccdc12de556e800e9456d3d")
    output = version.predict(frame1=item.frame1, frame2=item.frame2, times_to_interpolate=item.times_to_interpolate)
    return output


#TODO implement opencv functions for image manipulation
class split_params(BaseModel):
    division: Union[int,None]=2
    offset_x: Union[int,None]=0
    offset_y: Union[int,None]=0
    cv_guess="False"
    hex_upper: Union[str,None]=""
    hex_lower: Union[str,None]=""
    thrown_size: Union[int,None]=0
    thrown_deviation: Union[int,None]=0
def split_run(item: split_params):
    pass

class track_params(BaseModel):
    image: Union[str,None]=""
    target: Union[str,None]=""
    deviation: Union[int,None]=0
    cvtemplate: Union[str,None]=""
def track_run(item: track_params):
    pass