import requests
import json
import os

import pytesseract
from pytesseract import pytesseract, Output
import PIL
from PIL import Image
# import cv2

def createAreaWithinMap(url, desc, x1, y1, x2, y2):
    return f'<area shape="rect" coords="{x1},{y1},{x2},{y2}" href="{url}" alt="{desc}"/>'

def createHTMLFromMap(links, imgsrc):
    image_html = f'<img src="{imgsrc.replace("docs/", "")}" alt="alttext" usemap="#mapname">'

    area_htmls = [createAreaWithinMap(area["url"], area["desc"], area["x1"], area["y1"], area["x2"], area["y2"]) for area in links]
    
    # print('area htmls', area_htmls)

    map_html = """<map name="mapname">
    {}
    </map>""".format("\n".join(area_htmls))

    # return image_html + map_html
    return image_html + map_html

def produce_templated_html(img, input_filename, output_filename):
    print(f"parsing {img} and detailing it in {output_filename} (with base template {input_filename})...")
    image=Image.open(img) 

    d=pytesseract.image_to_data(image, output_type=Output.DICT)

    n_boxes = len(d['level'])
    links = []
    for i in range(n_boxes):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        prep_link = {
                "x1": x,
                "y1": y,
                "x2": x+w,
                "y2": y+h
            }

        if 'github' in d['text'][i]:
            links.append(dict(
                prep_link,
                url  = "https://github.com/TennisGazelle",
                desc = "github profile",
            ))
        elif 'twitter' in d['text'][i]:
            links.append(dict(
                prep_link,
                url  = "https://twitter.com/Tennis_Gazelle",
                desc =  "twitter profile",
            ))
        elif 'musescore' in d['text'][i]:
            links.append(dict(
                prep_link,
                url  = "https://musescore.com/user/4187496",
                desc =  "musescore profile",
            ))

    with open (input_filename, 'r') as input_file:
        with open(output_filename, 'w+') as output_file:
            lines = input_file.readlines()
            for l in lines:
                if 'IMAGE' in l:
                    output_file.write(createHTMLFromMap(links, img))
                else:
                    output_file.write(l)

def fetchImageFor(req, output_filename):
    print("fetching and posting to {}...".format(output_filename))
    image_url = "https://carbonara.now.sh/api/cook"

    # prep the payload
    with open ('carbon-config.json') as payload_f:
        payload=json.load(payload_f)
    payload['code']=req['code']

    post_reply = requests.post(image_url, json=payload)

    if post_reply.status_code > 299:
        print(post_reply.content)

    img_data = post_reply.content

    with open(output_filename, 'wb+') as handler:
        handler.write(img_data)

def getPayload(input_dir, input_filename):
    with open(os.path.join(input_dir, input_filename)) as in_f:
        payload=json.load(in_f)
    payload['code'] = json.dumps(payload['raw_json_code'], indent=3)
    return payload

def generateImages():
    input_dir="inputs/"

    for subdir, dirs, files in os.walk(input_dir):
        for input_file in files:
            if '.json' not in input_file:
                continue
            
            output_file = input_file.replace(".json", ".png")
            output_imagefile = os.path.join("docs/images/", input_file.replace(".json", ".png"))
            output_htmlfile = os.path.join("docs/", input_file.replace(".json", ".html"))


            print("generating {}...".format(output_imagefile))
            input_file_src = getPayload(input_dir, input_file)
            
            # print(json.dumps(input_file_src, indent=3))
            fetchImageFor(input_file_src, output_imagefile)

            produce_templated_html(output_imagefile, "index.mustache", output_htmlfile)

if __name__ == "__main__":
    generateImages()
    # test("outputs/sample-one-out.png")
    # produce_templated_html("outputs/sample-one-out.png")
