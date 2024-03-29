class Custom:
    def __init__(self, processes:list):
        self.processes = processes
        self.avg_rt = 0
        self.avg_wt = 0
        self.avg_tat = 0
        self.grant_chart = []
        self.q1 = [] #PP (priority = 1)
        self.q2 = [] #SJF (priority = 2)
        self.q3 = [] #FCFS (priority = 3)
        self.current_time = 0
        self.process_completed = [0,0,0] #each index is for one QUEUE
        

    def demote(self, processes:list, demote_to:str):
        if demote_to == "Q2":
            self.q2.extend(processes)
        elif demote_to == "Q3":
            self.q3.extend(processes)

    def preemprtive_priotity(self):
        waiting_queue = []
        temp_q = []
        prev_process = None

        while True:
            temp_q = [p for p in self.q1 if p.at == self.current_time and p not in waiting_queue]
            

            #check if Q1 is empty:
            if temp_q == []:
                # go to Q2
                # return the next arraival time for Q1
                return self.q1[self.q1.index(running_p)+1]

            waiting_queue.extend(temp_q)

            #get highest priority
            running_p = waiting_queue[0]
            running_p_index  = 0 
            
            for p in waiting_queue[1:len(waiting_queue)]:
                if p.priority < running_p.priority:
                    #context switch will happen:
                    #get waiting time:
                    running_p.wt += (self.current_time - running_p.ft)
                    running_p.ft = self.current_time

                    # change current running process
                    running_p = p
                    running_p_index = waiting_queue.index(p)
                    
            
            # subtract the BT from the running process
            waiting_queue[running_p_index].bt = waiting_queue[running_p_index].bt - 1

            # remove the process if the burst time is 0
            if waiting_queue[running_p_index].bt == 0:
                waiting_queue.remove(running_p)
                self.process_completed[0] += 1

                # set finish time:
                running_p.ft = self.current_time

                # set the TAT 
                running_p.tat = running_p.ft - running_p.at + 1
                

            if self.current_time == 0:
                # no prev process
                # store the prev process so we dont print it in a row multiple times
                prev_process = running_p

                #get response time:
                if running_p.rt == 0:
                    # response time is calculated for the first burst 
                    running_p.rt = self.current_time - running_p.at
                    

                    # make the response time = -1 to declare that it has been added to the avg
                    # this is good for the case of the first process running
                    running_p.rt = -1 

                #store the process in prev so we check again for context switch
                prev_process = running_p 
                
                #run the process:
                #print(f"| P{running_p.pid} |", end=" ")
                self.grant_chart.append(f'P{running_p.pid}')

            elif prev_process != running_p:
                # context switch happend, processes have changed

                #get response time:
                if running_p.rt == 0:
                    # response time is calculated for the first burst only
                    running_p.rt = self.current_time - running_p.at

                    # make the response time = 1 to declare that it has been added to the avg
                    # this is good for the case of the first process running
                    running_p.rt = -1 

                prev_process = running_p #store the process in prev so we check again for context switch
                
                #run the process:
                #print(f"P{running_p.pid } |", end=" ")
                self.grant_chart.append(f'P{running_p.pid}')

            #increment the time
            self.current_time += 1

            #check if the all the processes have ran:
            if self.process_completed[0] == len(self.q1):
                #no more Q1 processes.
                return None
            
    def shortest_job_first(self):
        
    
    def first_come_first_served(self):
        pass
            
    def determine_queue(self):

        #PP queue
        self.q1 = [p for p in self.processes if p.at == self.current_time and p not in self.q1]
        q1_next_p = self.preemprtive_priotity()
        # demote the excuted processes that didnot terminate to Q2
        demote_p = [p for p in self.q1[0:self.q1.index(q1_next_p)] if p.bt != 0] 
        self.demote(processes=demote_p, demote_to="Q2")

        
        self.current_time += 1