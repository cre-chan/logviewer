from django.shortcuts import render
from django.http import Http404
from . import logreader
from . import record
# Create your views here.


def search(request):
    return render(request,"logreader/search.html")

def logs(request):
    # get prams out of requests
    softname=request.POST['soft_name']
    rev_display='reverse_order' in request.POST
    restrict_num='enable_log_num' in request.POST

    # print(rev_display)
    querier=logreader.BasicQuery()
    querier=logreader.SoftQuery(querier,softname)
    # softname_opt=logreader.software_opt(softname)
    querier=querier if not rev_display else logreader.RevQuery(querier)
    # rev_opt=logreader.rev_opt() if rev_display else []
    querier=logreader.RestrictQuery(querier,request.POST['log_num']) if restrict_num else querier


    # print(softname_opt)
    # logs_json=logreader.query_journal(softname_opt+rev_opt+log_num_opt)
    logs_json=querier.query()
    print(len(logs_json))

    msg_list=map(lambda x: (lambda x:(x.get_time(),x.get_msg()))(record.Log(x)),logs_json)
    return render(request,'logreader/logs.html',{"soft_name":softname,"log_list":msg_list})