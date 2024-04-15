
import streamlit as st
import pandas as pd
from streamlit_extras import add_vertical_space as avs

class RoundRobin:
    def __init__(self, processes:list, quantim:int):
        self.quantim = quantim
        self.p = processes #objects
        self.num_of_processes = len(self.p)
        self.BT = [i.bt for i in self.p]  # Burst Time (corrected index based on file input structure)
        self.AT = [i.at for i in self.p]  # Arrival Time
        self.time_passed = 0
        self.execution_time = [-1] * self.num_of_processes  # To track the first execution time
        self.WT = [0] * self.num_of_processes  # Waiting Time
        self.RT = [0] * self.num_of_processes  # Response Time, initially not calculated
        self.TAT = [0] * self.num_of_processes  # Turnaround Time
        self.Ready_queue = [i for i in range(self.num_of_processes)]  # Ready queue initialized with indices

        self.grant_chart = []

        #these two lists are for grant chart printing format:
        self.gc_ft = []
        self.gc_st = []

        self.time_record = [] # keep track of the time printed in streamlit_print_gc()


    def round_robin(self, page_no="1"):
        while self.Ready_queue:
            #pop the running process
            i = self.Ready_queue.pop(0)

            # append entry time
            self.gc_st.append(self.time_passed)

            #check if process arraived so we print it
            st.write(self.p[i].at, self.time_passed)
            if self.p[i].at ==  self.time_passed:
                    
                    # proces just arraived print it!
                    self.streamlit_print_gc(self.p[i].pid, self.Ready_queue, self.p[i], page_no, self.p[i])


            if self.BT[i] > 0:
                if self.execution_time[i] == -1:
                    self.execution_time[i] = self.time_passed
                    self.RT[i] = self.time_passed - self.AT[i]

                exec_time = min(self.BT[i], self.quantim)
                self.BT[i] -= exec_time
                self.time_passed += exec_time
                #st.write(f"Task {self.p[i].pid} executed for {exec_time} ms at time {self.time_passed}.")
                
                #append to grantchart 
                self.grant_chart.append(f"P{self.p[i].pid}({self.BT[i]})")
                self.gc_ft.append(self.time_passed)

                if self.BT[i] == 0:
                    # process terminated 
                    self.TAT[i] = self.time_passed - self.AT[i]
                    self.WT[i] = self.TAT[i] - self.p[i].bt
                    #print(f"Task {self.p[i].pid} completes at time {self.time_passed}.")

                if self.BT[i] > 0:
                    # append the running process back to the queue
                    self.Ready_queue.append(i)

        Avg_WT = sum(self.WT) / self.num_of_processes
        Avg_TAT = sum(self.TAT) / self.num_of_processes
        Avg_RT = sum(self.RT) / self.num_of_processes
        return Avg_WT, Avg_TAT, Avg_RT



    def streamlit_print_gc(self, pid, waiting_q, running_p, page_no, next_running_p):
        if page_no == "1":
            
            if self.time_passed not in self.time_record:
                if self.time_passed != 0: st.markdown('---')
                c1,c2,c3 = st.columns(3)
                with c2:
                    st.subheader(f"Time⏰: {self.time_passed}ms")
                
                    
            st.markdown(f"<span style='color:yellow;'>⚠️🚗 P{pid} process just arrived to the queue..</span>", unsafe_allow_html=True)
            waiting_q = waiting_q.copy()
            if waiting_q !=[]:
                pid_list = []
                try:
                    waiting_q.remove(next_running_p)
                except ValueError:
                    pass
                st.markdown(f":green[CURRENT RUNNING PROCESS: P{running_p.pid}({running_p.bt})]")
                st.caption("Ready queue ")
                for i in waiting_q:
                    if self.p[i].pid != running_p.pid:
                        pid_list.append(f'P{self.p[i].pid}({self.p[i].bt})')
                
                st.code(pid_list, language='python')
            
            if self.grant_chart != []:
                st.markdown("**Current Grant chart with the running processes:**")
                
                #print grant chart table
                temp_ft = self.gc_ft.copy()
                temp_ft.append(self.time_passed)
                time_list = [f'{self.gc_st[i]} -> {temp_ft[i]}ms' for i,v in enumerate(temp_ft)] 
                p_list =  [i for i in self.grant_chart] 
                data_PP = [
                        tuple(p_list),
                ]
                df1_PP = pd.DataFrame(data_PP, ['Process'],  columns=time_list)
                st.table(df1_PP)
                
            
            if self.time_passed not in self.time_record:
                self.time_record.append(self.time_passed)