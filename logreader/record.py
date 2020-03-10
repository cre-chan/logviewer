import datetime

def getlogtime(log):
    log_time_microsec=int(log['__REALTIME_TIMESTAMP'])
    log_time_microsec=log_time_microsec/1e6
    return datetime.datetime.fromtimestamp(log_time_microsec)

def get_message(log):
    return log['MESSAGE']


class Log:

    def __init__(self,log_json):
        self.time=getlogtime(log_json)
        self.msg=get_message(log_json)

    def get_time(self):
        return self.time 

    def get_msg(self):
        return self.msg