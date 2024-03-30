
class PreemptivePriority:
    def __init__(self, processes:list):
        self.processes = processes
        self.avg_rt = 0
        self.avg_wt = 0
        self.avg_tat = 0
        self.grant_chart = []

    def simulate_pp(self):
        current_time = 0
        waiting_queue = []
        temp_q = []
        prev_process = None
        process_completed = 0

        while True:
            temp_q = [p for p in self.processes if p.at == current_time and p not in waiting_queue]
            waiting_queue.extend(temp_q)

            #get highest priority
            running_p = waiting_queue[0]
            running_p_index  = 0 
            
            for p in waiting_queue[1:len(waiting_queue)]:
                if p.priority < running_p.priority:
                    #context switch will happen:
                    # change current running process
                    running_p = p
                    running_p_index = waiting_queue.index(p)
                    
            
            # subtract the BT from the running process
            self.processes[self.processes.index(running_p)].bt -= 1

            #increment waiting time for all none running processes
            for process in waiting_queue:
                if process != running_p:
                    self.processes[self.processes.index(process)].wt += 1

            # remove the process if the burst time is 0
            if waiting_queue[running_p_index].bt == 0:
                waiting_queue.remove(running_p)
                process_completed+= 1

                # set finish time:
                running_p.ft = current_time

                # set the TAT 
                running_p.tat = running_p.ft - running_p.at + 1
                

            if current_time == 0:
                # no prev process
                # store the prev process so we dont print it in a row multiple times
                prev_process = running_p

                #get response time:
                if running_p.rt == 0 and f'P{running_p}' not in self.grant_chart:
                    # response time is calculated for the first burst 
                    running_p.rt = current_time - running_p.at

                #store the process in prev so we check again for context switch
                prev_process = running_p 
                
                #run the process:
                self.grant_chart.append(f'P{running_p.pid}')

            elif prev_process != running_p:
                # context switch happend, processes have changed

                #get response time:
                if running_p.rt == 0 and f'P{running_p}' not in self.grant_chart:
                    # response time is calculated for the first burst only
                    running_p.rt = current_time - running_p.at

                prev_process = running_p #store the process in prev so we check again for context switch
                
                #run the process:
                self.grant_chart.append(f'P{running_p.pid}')

            #increment the time
            current_time += 1

            #check if the all the processes have ran:
            if process_completed == len(self.processes):
                #print(f"\nAll processes have finished, Time needed: {current_time} ms")
                return
            
    def calculate_average(self):
        n = len(self.processes)

        # get avg response time
        for p in self.processes:
            # like we assumed if rt is -1 then it is actually 0 so no need to sum it
            self.avg_rt += p.rt

        self.avg_rt = self.avg_rt/n

        # get average waiting time
        for p in self.processes:
            self.avg_wt += p.wt

        self.avg_wt = self.avg_wt/n

        # get average TAT
        for p in self.processes:
            self.avg_tat += p.tat

        self.avg_tat = self.avg_tat/n
        



