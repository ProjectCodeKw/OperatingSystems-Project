class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.at = arrival_time
        self.ft = arrival_time # save the value of the current finish time (not terminate time)
        self.bt = burst_time
        self.priority = priority
        self.wt = 0
        self.rt = 0 #response time = first excution - arraival time
        self.tat = 0