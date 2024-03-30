class Custom:
    def __init__(self, processes:list, quantum:int):
        self.processes = processes
        self.avg_rt = 0
        self.avg_wt = 0
        self.avg_tat = 0
        self.grant_chart = []
        self.q1 = processes.copy() #PP (priority = 1)
        self.q2 = [] #RR q=4 (priority = 2)
        self.q3 = [] #FCFS (priority = 3)
        self.current_time = 0
        self.process_completed = 0 
        self.quantum = quantum
        

    def demote(self, demoted_p:object, demote_to:str):
        if demote_to == "Q2":
            #remove process from Q1
            self.q1.remove(demoted_p)
            # add to Q2
            self.q2.append(demoted_p)
        elif demote_to == "Q3":
            #remove process from Q2
            self.q2.remove(demoted_p)
            # add to Q3
            self.q3.append(demoted_p)

    def preemprtive_priotity(self):
        waiting_queue = []
        temp_q = []
        prev_process = None
        while True:
            
            temp_q = [p for p in self.q1 if p.at == self.current_time and p not in waiting_queue]
            waiting_queue.extend(temp_q)    

            if self.q1 == []:
                return -1

            #get highest priority
            running_p = waiting_queue[0]
            running_p_index  = 0 

            #check if Q1 is empty:
            if waiting_queue == []:
                # go to Q2
                # return the next arraival time for Q1
                return self.q1[self.q1.index(running_p)+1]

            for p in waiting_queue[1:len(waiting_queue)]:
                
                if p.priority < running_p.priority:
                    #check if the process ran:
                    if f'Q1: P{running_p.pid}' in self.grant_chart:
                        #move process to Q2:
                        self.demote(demoted_p=running_p, demote_to='Q2')

                        #remove it from waiting queue so it does not run again
                        waiting_queue.remove(running_p)

                    # change current running process
                    running_p = p
                    running_p_index = waiting_queue.index(p)

            
            # subtract the BT from the running process
            waiting_queue[running_p_index].bt = waiting_queue[running_p_index].bt - 1
            
            #increment waiting time for all non running processes
            for process in waiting_queue:
                if process != running_p:
                    self.q1[self.q1.index(process)].wt += 1

            for process in self.q2:
                process.wt += 1

            for process in self.q3:
                process.wt += 1

            # remove the process if the burst time is 0
            if waiting_queue[running_p_index].bt == 0:
                waiting_queue.remove(running_p)
                self.process_completed += 1

                # set finish time:
                running_p.ft = self.current_time

                # set the TAT 
                running_p.tat = running_p.ft - running_p.at + 1

                #remove from q1
                self.q1.remove(running_p)
                

            if self.current_time == 0:
                # no prev process
                # store the prev process so we dont print it in a row multiple times
                prev_process = running_p

                #get response time:
                if running_p.rt == 0 and f'Q1: P{running_p}' not in self.grant_chart:
                    # response time is calculated for the first burst 
                    running_p.rt = self.current_time - running_p.at

                #store the process in prev so we check again for context switch
                prev_process = running_p 
                
                #run the process:
                self.grant_chart.append(f'Q1: P{running_p.pid}')

            elif prev_process != running_p:
                # context switch happend, processes have changed

                #get response time:
                if running_p.rt == 0 and f'Q1: P{running_p}' not in self.grant_chart:
                    # response time is calculated for the first burst only
                    running_p.rt = self.current_time - running_p.at

                prev_process = running_p #store the process in prev so we check again for context switch
                
                #run the process:
                self.grant_chart.append(f'Q1: P{running_p.pid}')

            #increment the time
            self.current_time += 1

            
    def round_robin(self, q1_next_p):
        q = self.quantum
        if q1_next_p == -1:
            stop_time = -1
        else:
            stop_time = q1_next_p.at

        for running_p in self.q2:            
            for i in range(q):
                #check current time 
                if self.current_time == stop_time:
                    #conext switch to Q1
                    self.grant_chart.append(f'Q2: P{running_p.pid}')
                    #demote the process
                    self.demote(demoted_p=running_p, demote_to='Q3')

                    #add waiting time

                    return 'Q1'
                
                if running_p.bt != 0:
                    running_p.bt -= 1
                    self.current_time += 1

                    #increment waiting time for all non running processes
                    for process in self.q2:
                        if process != running_p:
                            process.wt += 1

                    for process in self.q3:
                        process.wt += 1


            if running_p.bt == 0 and self.current_time != stop_time:
                self.process_completed += 1
                self.grant_chart.append(f'Q2: P{running_p.pid}')
                #demote the process
                self.demote(demoted_p=running_p, demote_to='Q3')

                # set the TAT 
                running_p.tat = self.current_time - running_p.at 

        return 'Q3'
                    

    
    def first_come_first_served(self, q1_next_p):
        
        if q1_next_p ==-1:
            stop_time = -1
        else:
            stop_time = q1_next_p.at

        for running_p in self.q3:
            while running_p.bt != 0:
                #check current time
                if self.current_time == stop_time:
                    self.grant_chart.append(f'Q3: P{running_p.pid}')
                    return
                
                running_p.bt -= 1
                self.current_time += 1

                #increment waiting time for all non running processes
                for process in self.q3:
                    if process != running_p:
                        process.wt += 1

            if running_p.bt == 0:
                self.process_completed += 1
                self.grant_chart.append(f'Q3: P{running_p.pid}')

                # set the TAT 
                running_p.tat = self.current_time - running_p.at 


            if self.current_time == stop_time:
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

    def determine_queue(self):

        while self.process_completed < len(self.processes):
            #PP queue
            if self.q1 != []:
                q1_next_p = self.preemprtive_priotity()
            # demote the excuted processes that didnot terminate to Q2
                
            go_to = self.round_robin(q1_next_p)

            if go_to == 'Q3':
                self.first_come_first_served(q1_next_p)
        