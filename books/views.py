from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests 

def index(request):
    return render(request,'index.html')


def fetchapi(request,url):   

    overallval = request.session.get('overalllink')
    overallval.append(url)
    request.session['overalllink'] = overallval


    if "localhost" in url:
        url = url.replace("localhost:8005","skunkworks.ignitesol.com:8000")
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

def formatapidata(apidata):    
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

    context = {'bookdata': cachelist}

    return context


def fetchbooksscroll(request):  
    cache_nextlink = request.session.get('nextlink') 
    overallvallist = request.session.get('overalllink')
    print(overallvallist)
    if cache_nextlink in overallvallist:
        return JsonResponse(
            {"error": "Invalid request method", "message": "Only GET requests are allowed"},
            status=400  # Bad Request
        ) 

    apidata = fetchapi(request,cache_nextlink)     
    request.session['currentlink'] = cache_nextlink
    request.session['nextlink'] = apidata['next'] 

    apicontext = formatapidata(apidata)

    return JsonResponse(apicontext)


def category(request,generename):
    capitalized_generename = generename.capitalize() 
    url = f"http://skunkworks.ignitesol.com:8000/books/?topic={generename}"
    apidata = fetchapi(request,url)     
    request.session['currentlink'] = url
    request.session['nextlink'] = apidata['next']
    request.session['overalllink'] = [url]
    context = formatapidata(apidata)
    context["capitalized_generename"]=capitalized_generename

    return render(request,'category.html',context)
