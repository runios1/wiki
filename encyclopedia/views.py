from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.storage import default_storage
from django.forms.utils import ErrorList
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import math
import random
from markdown2 import Markdown

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())

markdown=Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown.convert(util.get_entry(title)),
        "title": title
    })
def search(request):
    if request.method=='GET':
        query=(request.GET)["q"]
        if util.get_entry(query):
            return render(request, "encyclopedia/entry.html", {
            "entry": util.get_entry(query),
            "title": query
        })
        else:
            return render(request, "encyclopedia/search.html", {
                "results": filter(lambda entry : query.lower() in entry.lower(),util.list_entries()),
                "query": query
        })
def createNew(request):
    if request.method=='POST':
        form=NewEntryForm(request.POST)
        if form.is_valid():
            title=request.POST["title"]
            filename = f"entries/{title}.md"
            if default_storage.exists(filename):
                return render(request,"encyclopedia/error.html")
            else:
                util.save_entry(title,request.POST["content"])
                return HttpResponseRedirect(reverse('entry',args=[title]))
        else:
            return render(request, "encyclopedia/createNew.html", {
            "form": form
        })
    return render(request, "encyclopedia/createNew.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    if request.method=='POST':
        form=NewEntryForm(request.POST)
        if form.is_valid():
            filename = f"entries/{title}.md"
            default_storage.delete(filename)

            util.save_entry(request.POST["title"],request.POST["content"])
            return HttpResponseRedirect(reverse('entry',args=[title]))
        else:
            return render(request, "encyclopedia/edit.html", {
                "entry": util.get_entry(title),
                "title": title,
                "form": form
            })
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(title),
        "title": title,
        "form": NewEntryForm({"title": title, "content": util.get_entry(title)})
    })
def randomPage(request):
    entries=util.list_entries()
    entry=entries[math.floor(random.randrange(len(entries)))]
    return HttpResponseRedirect(reverse("entry",args=[entry]))