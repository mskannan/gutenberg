from django.shortcuts import render,redirect
import requests 

def index(request):
    return render(request,'index.html')


def fetchapi(generename): 

    url = f"http://skunkworks.ignitesol.com:8000/books/?topic={generename}"

    # Set headers to accept JSON response
    headers = {
        "Accept": "application/json"
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data 


def category(request,generename):
    capitalized_generename = generename.capitalize() 
    apidata = fetchapi(generename) 
    apidataresult = apidata['results']
    cachelist = []
    for data in apidataresult:
        imgval = data['formats']
        fulltitle = data['title']
        cachelist.append({
            'title': ' '.join(fulltitle.split(" ")[:5]),
            'fulltitle':fulltitle,
            'authors': data['authors'],
            "img": imgval.get('image/jpeg')
        })
    context = {'bookdata': cachelist,"capitalized_generename":capitalized_generename}
    return render(request,'category.html',context)
