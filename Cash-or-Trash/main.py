from flask import Flask, render_template, url_for, request, redirect
import requests
import json
import base64
import os

app = Flask(__name__)

#@app.route("/") #defines the URL’s path component

# decorator. 
# This function defines what should be executed 
# if the defined URL endpoint is requested by a user
#def index():
#    return "Congratulations, it's a web app!"
@app.route("/", methods=['POST', 'GET'])
def index():
    title = "Trash or Cash"
    background_image_url = 'static/bg.jpeg'
    return render_template("template.html", title=title, background_image_url = background_image_url)

def image_fun(image_file):
    url = "https://vision.googleapis.com/v1/images:annotate"

    # Define the image file you want to use

    # Read the image file into memory
    with open(image_file, "rb") as image:
        image_content = base64.b64encode(image.read()).decode("utf-8")

    # Define the API key
    api_key = "AIzaSyDDEL9KxRm6ZOogckNUul3cLgwmi8WJaOM"

    # Define the request headers
    headers = {
        "Content-Type": "application/json",
    }

    # Define the request payload
    payload = {
        "requests": [
            {
                "image": {
                    "content": image_content
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION",
                        "maxResults": 10
                    }
                ]
            }
        ]
    }

    # Send the request to the API
    response = requests.post(url, headers=headers, json=payload, params={"key": api_key})

    # Print the response
    #print(json.loads(response.text))

    # API response
    response_json = response.json()

    lst_complete = []

    # Extract labels from API response
    labels = response_json["responses"][0]["labelAnnotations"]
    for label in labels:
        lst_complete.append(label["description"])
        #fixed list for non-recyles

    lst_non_recyclable = ['Plastic wrap', 'Paint', 'Packaging and labeling', 'Porcelain', 'Chair']

    #Master list for every item - should be dynamic
    #lst_complete = ['Plastic','Tin','Paint']

    _cnt = 0

    for i in range(0,len(lst_complete)):
        if lst_complete[i] in lst_non_recyclable:
            _cnt = _cnt+1

    return _cnt


@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["image"]
    path = os.path.join("/tmp/", image.filename)
    image.save(path)
    file_path = "/tmp/" + image.filename
    if image_fun(file_path) == 0:
        return redirect('/recycle')
    else:
        return redirect('/trash')

@app.route('/recycle')
def cash():
    title = "Recycle"
    image_url = "/static/recycle2.png"
    return render_template('recycable.html', title=title, image_url=image_url)


@app.route('/trash')
def trash():
    title = "Trash"
    image_url = "/static/trash2.png"
    return render_template('recycable.html', title=title, image_url=image_url)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

