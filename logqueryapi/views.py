from django.shortcuts import render
from django.http import HttpResponse
import json
from . import logreader

def make_query(form):
    # get prams out of requests
    softname=form['soft_name']
    rev_display='reverse_order' in form
    restrict_num='enable_log_num' in form

    # print(rev_display)
    querier=logreader.BasicQuery()
    querier=logreader.SoftQuery(querier,softname)
    # softname_opt=logreader.software_opt(softname)
    querier=querier if not rev_display else logreader.RevQuery(querier)
    # rev_opt=logreader.rev_opt() if rev_display else []
    querier=logreader.RestrictQuery(querier,form['log_num']) if restrict_num else querier


    # print(softname_opt)
    # logs_json=logreader.query_journal(softname_opt+rev_opt+log_num_opt)
    
    return querier.query()

# Create your views here.
def logs_generic(request):
    lst=make_query(request.GET)
    return HttpResponse(json.dumps(lst),charset='utf-8')