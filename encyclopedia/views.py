from django.http import HttpResponse
from django.shortcuts import redirect, render

from . import util
from django import forms
from markdown2 import Markdown
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    retrieved_content = util.get_entry(title)
    if retrieved_content is None:
        final_title = "ERROR 404"
        final_content = f"""
        <h1> Error 404 - Entry not found </h1> <br>
        <p> The title requested, <b>"{title}"</b> yielded no results.
        Please use the search function to look for the entry. </p>"""
    else:
        markdowner = Markdown()
        final_title = title
        final_content = markdowner.convert(retrieved_content)
    return render(request, "encyclopedia/entry.html", {
        "title": final_title,
        "content": final_content
    })

def new_entry(request):
    if request.method == "POST":
        form = request.POST
        title = form.get("title")
        content = form.get("content")
        if util.get_entry(title) is not None: #If this exists already...
            return existing_entry_error(request, title, content)
        else:
            util.save_entry(title, content)
            return redirect("index")
    else:
        return render(request, "encyclopedia/new_page.html", {
            "existing_entry": False
        })

def existing_entry_error(request, title, content):
    entry_content = util.get_entry(title)
    final_content = ""
    if(entry_content is None):
        final_content = "Something unexpected happened, it seems as if it was empty!"
    else:
        mkdwn = Markdown()
        final_content = mkdwn.convert(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "title": f"""Entry Save Error""",
        "content": f"""<h1>Error, entry <i>"{title}"</i> already exists </h1>
        <h4>The entry is saved with the following content:</h4><br><br>{final_content}"""
    })

def random_entry(request):
    entry_list = util.list_entries()
    entry_title = entry_list[random.randint(0, len(entry_list)-1)]
    return redirect('get_entry', title=entry_title)

def search_entry(request):
    form = request.GET
    entry_query = str(form.get("q"))
    entry_query_lower = entry_query.lower()
    #This line inspired by https://stackoverflow.com/a/1801676
    entry_list = util.list_entries()
    entry_list_lower = [x.lower() for x in entry_list] 
    if entry_query_lower in entry_list_lower:
        return redirect("get_entry", title=entry_query_lower)
    else:
        result_list = []
        for entry_title_lower, entry_title in list(zip(entry_list_lower, entry_list)):
            if entry_query_lower in entry_title_lower:
                result_list.append(entry_title)
        len_result_list = len(result_list)
        if (len_result_list == 0):
            result_instruction = f"""No results found for <i>"{entry_query}"</i>. Try a synonym or a word with similar meaning!"""
        else:
            result_instruction = f"""{len_result_list} result(s) found for term <i>"{entry_query}"</i>. """
        return render(request, "encyclopedia/search_results.html", {
            "entry_query":entry_query,
            "result_list":result_list,
            "result_instruction":result_instruction })

def edit_entry(request):
    if request.method == "POST":
        entry_title = request.POST.get("title")
        new_content = request.POST.get("content")
        util.save_entry(entry_title, new_content)
        return redirect("get_entry", title=entry_title)
    else:
        entry_title = request.GET.get("title")
        if entry_title not in util.list_entries():
            return not_found(request)
        else:
            entry_content = util.get_entry(entry_title)
            return render(request, "encyclopedia/new_page.html", {
                "existing_entry": True,
                "existing_entry_title": entry_title,
                "existing_entry_content": entry_content
            })

def not_found(request):
    return render(request, "encyclopedia/error404.html")