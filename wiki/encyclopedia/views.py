from django.shortcuts import render, redirect
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry_page(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html")
    else:
        content_entry = markdown2.markdown(util.get_entry(title)) 
        return render(request, "encyclopedia/entry_page.html", {
            "title" : title,
            "content" : content_entry 
        })
def search_page(request):
        entry_name = request.GET.get("q", " ").strip()
        for ent_ in util.list_entries():
            if entry_name.lower() == ent_.lower():
                return redirect("entry-page", title=entry_name)
          
        list_of_ent = [ent for ent in util.list_entries() if entry_name.lower() in ent.lower()]
        return render(request, "encyclopedia/search.html", {
                "lists_of_ent" : list_of_ent
        }) 
def create_newpage(request):
    if request.method == "POST":
         entry_title = request.POST.get("title")
         entry_content = request.POST.get("content")
         if entry_title in util.list_entries():
            return render(request, "editing_entries/createpage.html", {
                "error_message" : "the page already exist"
            })
         else:
             util.save_entry(entry_title, entry_content)
             return redirect("entry-page", title=entry_title)

    return render(request, "editing_entries/createpage.html",)
        
def random_page(request):
    random_choice = random.choice(util.list_entries())
    return redirect('entry-page', title=random_choice)

def edit_page(request, title):
    if request.method == "POST":
        content_md = request.POST.get('content').replace('\r\n', '\n')
        util.save_entry(title, content_md)
        return redirect('entry-page', title=title)
    content = util.get_entry(title)
    return render(request, "editing_entries/editpage.html", {
        'content' : content,
        'title' : title
    })
    