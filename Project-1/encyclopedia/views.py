from asyncio.unix_events import _UnixDefaultEventLoopPolicy
from curses.ascii import HT
from http.client import HTTPResponse
from django.http import HttpResponseRedirect
import imp
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.urls import reverse

from . import util
from markdown2 import markdown
import random

class NewEntryForm (forms.Form):
    title =  forms.CharField(widget=forms.TextInput(attrs={'name':'title'}))
    contents = forms.CharField(widget=forms.Textarea(attrs={'name':'contents', 'style': 'height: 5em;'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["contents"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse('Invalid')
    else:
        if entry in util.list_entries():
            return render(request, "encyclopedia/entry.html", {
                "entry": entry, "text": markdown(util.get_entry(entry))
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry, "text": "<h1>" +  entry + " Not Found</h1>"
            })
            

def random_entry(request):
    entries = util.list_entries()
    selected = random.choice(entries)
    return entry(request, selected)

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title):
                return render(request, "encyclopedia/entry.html", {
                    "entry": title, "text": "<h1>" +  title + " Already Exists</h1>"
                })
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["contents"])
            return HttpResponseRedirect(reverse("entry", kwargs={'entry':title}))
        else:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry, "text": "<h1>" +  entry + " Is Invalid</h1>"
            })
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/new_entry.html", {
            "form": form
        })

def edit_entry(request, entry):
    form = NewEntryForm(initial={'title': entry, 'contents': util.get_entry(entry)})
    return render(request, "encyclopedia/edit_entry.html", {
        "form": form, "entry": entry
    })

def save_entry(request, entry):
    form = NewEntryForm(request.POST)
    if form.is_valid():
        util.save_entry(form.cleaned_data["title"], form.cleaned_data["contents"])
        return HttpResponseRedirect(reverse("entry", kwargs={'entry':entry}))
    else:
        return HttpResponse('Invalid')


def search(request):
    value = request.GET.get('q','')
    if util.get_entry(value) != None:
        return HttpResponseRedirect(reverse('entry', kwargs={'entry':value}))
    else:
        allEntries = util.list_entries()
        matching = [k for k in allEntries if value.upper() in k.upper()]
        # matching = list(filter(lambda entry: value.upper() in entry.upper, allEntries))
        return render(request, "encyclopedia/search.html", {
        "entries": matching, "value": value
    })

