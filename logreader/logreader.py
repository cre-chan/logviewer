import subprocess
import json
import logviewer.settings as settings
from os import environ


passwd=environ['USER_PASSWD']+'\n'


class Querier():
    def __init__(self):
        raise NotImplementedError

    def get_opts(self):
        """

        """
        raise NotImplementedError

    def query_journal(self,opt):
        raise NotImplementedError

    def query(self):
        return self.query_journal(self.get_opts())

class BasicQuery(Querier):
    def __init__(self):
        pass 

    def query_journal(self,opt):
        cmd=["sudo","-S","journalctl"]+opt

        if settings.DEBUG:
            print(cmd)  

        journal=subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf-8",
            input=passwd
        )
        journal=journal.stdout
        return list(map(lambda x:json.loads(x), journal.splitlines()))

    def get_opts(self):
        return ['-o','json']

class RevQuery(Querier):
    def __init__(self,query):
        """
        do not use custom options. Reverse result using rev so as to avoid journalctl bug
        when using -r and -n flags together
        """
        self.get_opts=lambda :query.get_opts()
        self.query_journal= lambda opts: list(reversed(query.query_journal(opts)))


class SoftQuery(Querier):
    def __init__(self,query,name):
        self.get_opts=lambda : query.get_opts()+['-u',name]
        self.query_journal=lambda opt: query.query_journal(opt)

class RestrictQuery(Querier):
    def __init__(self:Querier,query:Querier,n):
        self.get_opts=lambda : query.get_opts()+['-n',str(n)]
        self.query_journal=lambda opt: query.query_journal(opt)

def rev_opt():
    """
    reverse the output order, display recent logs first
    """
    return ['-r']

def software_opt(name):
    """
    choose the software's name to inspect
    """
    return ['-u',name]

def number_opt(n):
    """
    limit the maximum number of logs to display
    """
    return ['-n',str(n)]