from django.shortcuts import render
from django.http import Http404,HttpResponse, HttpRequest
from django.urls import reverse
from . import record
import json
import requests
from logqueryapi.views import logs_generic
# Create your views here.

def make_query(form):
    # get prams out of requests
    softname=form['soft_name']
    rev_display='reverse_order' in form
    restrict_num='enable_log_num' in form

    req=requests.get(
        'http://'+'localhost:8000'+reverse("logqueryapi:generic"),
        {"soft_name":softname}
    )

    # querier=logreader.BasicQuery()
    # querier=logreader.SoftQuery(querier,softname)
    # querier=querier if not rev_display else logreader.RevQuery(querier)
    # querier=logreader.RestrictQuery(querier,form['log_num']) if restrict_num else querier
    
    return json.loads(req.text)


def search(request):
    return render(request,"logreader/search.html")

def logs(request):
    # logs_json=make_query(request.GET)
    logs_json=json.loads(logs_generic(request).content)
    msg_list=map(lambda x: (lambda x:(x.get_time(),x.get_msg()))(record.Log(x)),logs_json) 
    return render(request,'logreader/logs.html',{"soft_name":request.GET['soft_name'],"log_list":msg_list})
