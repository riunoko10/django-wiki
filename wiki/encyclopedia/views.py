import random
from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

class SearchForm(forms.Form):
    query = forms.CharField(label="Search")


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
    })

def entries(request, title:str):
    return render(request, "encyclopedia/entry.html", {
        "entry": Markdown().convert(util.get_entry(title)),
        "title": title,
        "form": SearchForm()
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            entries = util.list_entries()
            results = [entry for entry in entries if query.lower() == entry.lower()]
            if len(results) == 1:
                title = results[0]
                return render(request, "encyclopedia/entry.html", {
                    "entry": util.get_entry(title),
                    "title": title, 
                    "form": SearchForm()
                    })
            results = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "results": results,
                "form": SearchForm()
            })

def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/newPage.html", {
                    "message": "Page already exists.",
                    "search": SearchForm(),
                    "newForm": NewPageForm()
                })
            content = "# " + title + "\n" + form.cleaned_data["content"] 
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": util.get_entry(title),
                "title": title,
                "form": SearchForm()
            })
    return render(request, "encyclopedia/newPage.html", {
        "newForm": NewPageForm(),
        "search": SearchForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"] 
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": Markdown().convert(util.get_entry(title)),
                "title": title,
                "form": SearchForm()
            })
    entry = util.get_entry(title)
    form = EditForm(initial={'content': entry})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "editForm": form,
        "search": SearchForm(),
        
    })

def rand(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "entry": Markdown().convert(util.get_entry(title)),
        "title": title,
        "form": SearchForm()
    })