import streamlit as st
import pandas as pd
from streamlit_extras import add_vertical_space as avs

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
        self.quantum = 4
        self.time_record = [] # keep track of the time printed in streamlit_print_gc()

        #these two lists are for grant chart printing format:
        self.gc_ft = []
        self.gc_st = [0]
        

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

    def streamlit_print_gc(self, pid, waiting_q1, running_p, page_no, next_running_p):
        if page_no == "1":

            if self.current_time not in self.time_record:
                if self.current_time != 0: st.markdown('---')
                c1,c2,c3 = st.columns(3)
                with c2:
                    st.subheader(f"Time⏰: {self.current_time}ms")

            waiting_q1 = waiting_q1.copy()
            avs.add_vertical_space(1)
            st.markdown(f"<span style='color:yellow;'>⚠️🚗 P{pid} process just arrived to the queue..</span>", unsafe_allow_html=True)        
            pid_q1 = []
            pid_q3 = []
            pid_q2 = []
            
            if waiting_q1 !=[]:
                pid_list = []
                try:
                    waiting_q1.remove(next_running_p)
                except ValueError: pass

                if running_p in self.q1:
                    st.markdown(f":green[CURRENT RUNNING PROCESS: Q1: P{running_p.pid}({running_p.bt}, {running_p.priority})]")
                elif running_p in self.q2:
                    st.markdown(f":green[CURRENT RUNNING PROCESS: Q2: P{running_p.pid}({running_p.bt}, {running_p.priority})]")
                else:
                    st.markdown(f":green[CURRENT RUNNING PROCESS: Q3: P{running_p.pid}({running_p.bt}, {running_p.priority})]")

                st.caption("Ready Q1 (Priotity):")
                for i in waiting_q1:
                    if i.pid != running_p.pid:
                        pid_q1.append(f'P{i.pid}({i.bt}, {i.priority})')
                    
                st.code(pid_q1, language='python')
                
                st.caption("Ready Q2 (Round Robin):")
                for i in self.q2:
                    if i.pid != running_p.pid:
                        pid_q2.append(f'P{i.pid}({i.bt}, {i.priority})')
                    
                st.code(pid_q2, language='python')

                st.caption("Ready Q3 (FCFS):")
                for i in self.q3:
                    if i.pid != running_p.pid:
                        pid_q3.append(f'P{i.pid}({i.bt}, {i.priority})')
                    
                st.code(pid_q3, language='python')

            if self.grant_chart != []:
                if next_running_p == running_p:
                    st.markdown("**Current Grant chart with the running processes:**")
                else:
                    st.markdown(f"**Grant chart after prioritizing Q1: P{next_running_p.pid}({next_running_p.bt}, {next_running_p.priority})**")

                #fix the grand_chgart format for printing
                temp_ft = self.gc_ft.copy()
                temp_ft.append(self.current_time)
                time_list = [f'{self.gc_st[i]} -> {temp_ft[i]}ms' for i,v in enumerate(temp_ft)]  #row number 3
                Q_list = [v[0:2]+f' '*i for i,v in enumerate(self.grant_chart)] #row number 1
                p_list =  [i[4:len(i)] for i in self.grant_chart] # row number 2
                data_MLFQC = [
                        (t for t in time_list),
                        (p for p in p_list)
                ]
                df1_MLFQC = pd.DataFrame(data_MLFQC, ['Time', 'Process'], columns=Q_list)
                st.table(df1_MLFQC)


                    
            
        if self.current_time not in self.time_record:
                self.time_record.append(self.current_time)

    def preemprtive_priotity(self, page_no="1"):
        waiting_queue = []
        temp_q = []
        prev_process = None
        while True:
            
            temp_q = [p for p in self.q1 if p.at == self.current_time and p not in waiting_queue]
            waiting_queue.extend(temp_q)    

            if self.q1 == []:
                #append finish time to grant chart
                self.gc_ft.append(self.current_time)
                self.gc_st.append(self.current_time)
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
                # get highest priority
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

            if self.current_time == 0:
                # no prev process
                # store the prev process so we dont print it in a row multiple times
                prev_process = running_p
                
                #run the process:
                self.grant_chart.append(f'Q1: P{running_p.pid}')

            if temp_q != []:
                # a new process have arravied
                for i in temp_q:
                    self.streamlit_print_gc(i.pid, waiting_queue, prev_process, page_no, running_p)

            
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
                

            if prev_process != running_p:
                # context switch happend, processes have changed

                #get response time:
                if running_p.rt == 0 and f'Q1: P{running_p}' not in self.grant_chart:
                    # response time is calculated for the first burst only
                    running_p.rt = self.current_time - running_p.at

                prev_process = running_p #store the process in prev so we check again for context switch
                
                #run the process:
                self.grant_chart.append(f'Q1: P{running_p.pid}')

                #append finish time to grant chart
                self.gc_ft.append(self.current_time)
                self.gc_st.append(self.current_time)

            #increment the time
            self.current_time += 1

            
    def round_robin(self, q1_next_p):
        q = self.quantum
        if q1_next_p == -1:
            # self.q1 is empty thats why its -1
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

                    #append process finish and arraival times
                    self.gc_ft.append(self.current_time)
                    self.gc_st.append(self.current_time)

                    return 
                
                if running_p.bt != 0:
                    running_p.bt -= 1
                    self.current_time += 1

                    #increment waiting time for all non running processes
                    for process in self.q2:
                        if process != running_p:
                            process.wt += 1

                    for process in self.q3:
                        process.wt += 1


            if running_p.bt == 0:   
                # process has been termindated
                self.process_completed += 1
                self.grant_chart.append(f'Q2: P{running_p.pid}')
                #demote the process
                self.demote(demoted_p=running_p, demote_to='Q3')

                # set the TAT 
                running_p.tat = self.current_time - running_p.at 

                #append process finish and arraival times
                self.gc_ft.append(self.current_time)
                self.gc_st.append(self.current_time)

            #process needs to be demoted 
            self.grant_chart.append(f'Q2: P{running_p.pid}')
            #demote the process
            self.demote(demoted_p=running_p, demote_to='Q3')
            #append process finish and arraival times
            self.gc_ft.append(self.current_time)
            self.gc_st.append(self.current_time)
            
        return 
                    
    
    def first_come_first_served(self, q1_next_p):
        #QUEUE3
        if q1_next_p ==-1:
            #no processes is waitintg in Queue 1 or QUEUE 2
            stop_time = -1
        else:
            stop_time = q1_next_p.at

        for running_p in self.q3:
            while running_p.bt != 0:
                #check current time
                if self.current_time == stop_time:
                    self.grant_chart.append(f'Q3: P{running_p.pid}')
                    #append process finish and arraival times
                    self.gc_ft.append(self.current_time)
                    self.gc_st.append(self.current_time)
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

                #append process finish and arraival times
                self.gc_ft.append(self.current_time)
                self.gc_st.append(self.current_time)


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


    def determine_queue(self, page_no):
        while self.process_completed < len(self.processes):
            #PP queue
            if self.q1 != []:
                q1_next_p = self.preemprtive_priotity(page_no)

            if self.q2 != []:    
                self.round_robin(q1_next_p)

            if self.q1 == [] and self.q2 == []:
                self.first_come_first_served(q1_next_p)
        