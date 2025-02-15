from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests 

# Home page view
def index(request):
    return render(request, 'index.html')

# Function to fetch data from an API
# It modifies the URL if it contains 'localhost' and stores the request in session
def fetchapi(request, url):   
    
    # Retrieve session variable 'overalllink' which keeps track of visited URLs
    overallval = request.session.get('overalllink', [])
    overallval.append(url)
    request.session['overalllink'] = overallval

    # Replace 'localhost' with the actual domain for external API calls
    if "localhost" in url:
        url = url.replace("localhost:8005", "skunkworks.ignitesol.com:8000")
    
    # Set headers to accept JSON response
    headers = {"Accept": "application/json"}

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the response was successful and return the JSON data
    if response.status_code == 200:
        return response.json()

# Function to get the preferred format link from available formats
def getpreferedlink(imgval):
    preferred_formats = ['text/html', 'text/html; charset=utf-8', 'text/plain', 'text/plain; charset=us-ascii', 'application/rdf+xml']    
    for fmt in preferred_formats:
        value = imgval.get(fmt)
        if value:
            return value  # Return the first available format link
    
    return None  # Return None if no preferred format exists

# Function to format API response data before passing to the frontend
def formatapidata(apidata):    
    apidataresult = apidata.get('results', [])  # Extract results from API response
    cachelist = []
    
    for data in apidataresult:
        imgval = data['formats']  # Extract available formats
        fulltitle = data['title']  # Extract book title
        srclink = getpreferedlink(imgval)  # Get the preferred source link
    
        # Format and append book details
        cachelist.append({
            'title': ' '.join(fulltitle.split(" ")[:5]),  # Truncate title to 5 words
            'fulltitle': fulltitle,
            'authors': data['authors'],
            "img": imgval.get('image/jpeg'),  # Get image URL if available
            "srclink": srclink  # Preferred source link
        })
    
    return {'bookdata': cachelist}  # Return formatted data

# Function to fetch books based on search query
def fetchbooksearch(request):
    if request.method == 'POST':
        form = request.POST 
        searchval = form.get('searchval')  # Get search input from form
        
        # Construct API URL with search query
        url = f"http://skunkworks.ignitesol.com:8000/books/?search={searchval}"
        
        apidata = fetchapi(request, url)  # Fetch data from API
        apicontext = formatapidata(apidata)  # Format data

        return JsonResponse(apicontext)  # Return data as JSON response

# Function to fetch additional books when scrolling (pagination)
def fetchbooksscroll(request):  
    
    cache_nextlink = request.session.get('nextlink')  # Get next page link from session
    overallvallist = request.session.get('overalllink', [])  # Get visited links list
    
    # Prevent duplicate fetch requests
    if cache_nextlink in overallvallist:
        return JsonResponse(
            {"error": "Invalid request method", "message": "Only GET requests are allowed"},
            status=400  # Bad Request
        ) 
    
    # Fetch next set of books from API
    apidata = fetchapi(request, cache_nextlink)     
    
    # Update session with new pagination details
    request.session['currentlink'] = cache_nextlink
    request.session['nextlink'] = apidata.get('next') 
    
    apicontext = formatapidata(apidata)  # Format API response
    return JsonResponse(apicontext)  # Return formatted data as JSON response

# Function to fetch books by category/topic
def category(request, generename):
    capitalized_generename = generename.capitalize()  # Capitalize category name for display
    
    # Construct API URL for category-based search
    url = f"http://skunkworks.ignitesol.com:8000/books/?topic={generename}"
    
    apidata = fetchapi(request, url)  # Fetch data from API
    
    # Update session with pagination and visited links
    request.session['currentlink'] = url
    request.session['nextlink'] = apidata.get('next')
    request.session['overalllink'] = [url]
    
    context = formatapidata(apidata)  # Format API response
    context["capitalized_generename"] = capitalized_generename  # Add category name to context
    
    return render(request, 'category.html', context)  # Render category page with data
