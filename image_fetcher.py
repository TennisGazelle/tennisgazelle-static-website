import requests
import json
import os

import pytesseract
from pytesseract import pytesseract
import PIL
from PIL import Image

def test(img):
    image=Image.open(img) 
    x1,y1,x2,y2=image.getbbox()
    width, height = image.size 

    print(image.size)
    print(x1,y1,x2,y2)  

    im1 = image.crop((x1, y1, x2, y2)) 
    # Shows the image in image viewer 
    im1.save("new.png")

    data=pytesseract.image_to_boxes(image)

    print(data)
    # character, left, bottom, right, top, page




def fetchImageFor(req, output_filename):
    print("fetching and posting to {}...".format(output_filename))
    image_url = "https://carbonara.now.sh/api/cook"

    req.pop('raw_json_code')

    post_reply = requests.post(image_url, json=req)

    if post_reply.status_code > 299:
        print(post_reply.content)

    img_data = post_reply.content

    with open(output_filename, 'wb') as handler:
        handler.write(img_data)

def getPayload(input_filename):
    with open('inputs/sample-one.json') as in_f:
        payload=json.load(in_f)
    payload['code'] = json.dumps(payload['raw_json_code'], indent=3)
    return payload


if __name__ == "__main__":
    # input_dir="inputs/"

    # for subdir, dirs, files in os.walk(input_dir):
    #     for input_file in files:
    #         output_file = input_file.replace(".json", "-out.png")

    #         print("loading {}...".format(input_file))
    #         home_page_src = getPayload(input_file)
            
    #         print(json.dumps(home_page_src, indent=3))
    #         fetchImageFor(home_page_src, os.path.join("outputs/", output_file))

    test("outputs/sample-one-out.png")