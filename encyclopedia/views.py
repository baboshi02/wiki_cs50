from django.shortcuts import render
from markdown2 import Markdown
import random
from . import util


def index(request):   
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md_to_html(title):
    """
    Turns an md file to html file
    """
    markdowner=Markdown()
    content=util.get_entry(title)
    if content==None:
        return None
    else:
        return markdowner.convert(content)

def entry(request,title):
    result=md_to_html(title)
    if result==None:
        return render(request,"encyclopedia/error.html",{
            "title":"<h1>Error</h1>",
            "Body":"Page not found"
        })
    else:    
        return render(request,"encyclopedia/entry.html",{
            "entry":result,
            "title":title
    })
def search(request):
    """
    searches for a query if it is not found renders an error page
    """
    if request.method=="POST":
        entry_search=request.POST["q"]
        html_content=md_to_html(entry_search)
        if html_content is not None:
            return render(request,"encyclopedia/entry.html",{
            "title":entry_search,
            "entry":html_content
            })
        else:
            lists=util.list_entries()
            queries=[list for list in lists if entry_search.upper() in list.upper() ]
            return render(request,"encyclopedia/search_results.html",{
            "title":"Search results page",
            "queries":queries
            })
            
def new_page(request):
    return render(request,"encyclopedia/new_page.html")

def create_new_page(request):
    """
    creates new page
    """
    
    titles=[title.upper() for title in util.list_entries()]
    if request.method=="POST":
        title=request.POST["title"].upper()
        body=request.POST["body"]
        if title not in titles:
            util.save_entry(title,body)
            return render(request,"encyclopedia/index.html",{
                "entries": util.list_entries()
            })
        return render(request,"encyclopedia/error.html",{
        "title":"Error", 
        "Body":"<h1>Page already exists</h1>"
        })
    return render(request,"encyclopedia/index.html")

def edit(request):
    if request.method=="POST":
        title=request.POST["entry_title"]
        body=util.get_entry(title)
        return render(request,"encyclopedia/edit_page.html",{
            "title":title,
            "body":body
        })

def save_edit(request):
    if request.method=="POST":
        title=request.POST["title"]
        body=request.POST["body"]
        util.save_entry(title,body)
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random_page(request):
    entries=util.list_entries()
    title=random.choice(entries)
    body=md_to_html(title)
    return render(request,"encyclopedia/entry.html",{
            "entry":body,
            "title":title
    })