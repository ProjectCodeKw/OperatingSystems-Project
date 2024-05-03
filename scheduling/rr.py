import streamlit as st
import pandas as pd
from streamlit_extras import add_vertical_space as avs

class RoundRobin:
    def __init__(self, processes:list, q:int):
        self.processes = processes
        self.q = q
        self.grant_chart = []
        self.current_time = 0

        # THESE ARE FOR PRINTING ONLY THEY SURVE NO USE IN COMPUTING
        self.time_record = [] #times printed
        self.arrived = [] #processes that arrived
        self.gc_ft = []
        self.gc_st = [0]


    def streamlit_print_gc(self, pid, waiting_q, running_p, page_no, next_running_p):
        #**note: this function is for printing only it does no computing**
        if page_no == "1":
            if self.current_time not in self.time_record:
                if self.current_time != 0:
                    st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c2:
                    st.subheader(f"Time⏰: {self.current_time}ms")

            st.markdown(
                f"<span style='color:yellow;'>⚠️🚗 P{pid} process just arrived to the queue..</span>",
                unsafe_allow_html=True,
            )
            waiting_q = waiting_q.copy()
            if waiting_q != []:
                pid_list = []
                try:
                    waiting_q.remove(next_running_p)
                except ValueError:
                    pass
                st.markdown(
                    f":green[CURRENT RUNNING PROCESS: P{running_p.pid}({running_p.bt})]"
                )
                st.caption("Ready queue")
                for i in waiting_q:
                    if i.pid != running_p.pid:
                        pid_list.append(f"P{i.pid}({i.bt})")

                st.code(pid_list, language="python")

            if self.grant_chart != [] and self.current_time!=0:
                
                st.markdown("**Current Grant chart with the running processes:**")

                # print grant chart table
                temp_ft = self.gc_ft.copy()
                temp_ft.append(self.current_time)
                time_list = [
                    f"{self.gc_st[i]} -> {temp_ft[i]}ms" for i, v in enumerate(temp_ft)
                ]
                p_list = [i for i in self.grant_chart]
                data_PP = [
                    tuple(p_list),
                ]
                df1_PP = pd.DataFrame(data_PP, ["Process"], columns=time_list)
                st.table(df1_PP)
                

            if self.current_time not in self.time_record:
                self.time_record.append(self.current_time)


    def roundrobin(self, page_no = '1'):
        processes = []
        counter_q = self.q
        i = 0

        # get the initial queue
        for k in self.processes:
                if k.at == 0:
                    processes.append(k)

        prev_p = processes[i]

        while len(processes) > 0:

            #set the response time for the process if its the first time running only
            if processes[i].rt == 0  and f"P{processes[i].pid}({processes[i].bt})" not in self.grant_chart:
                if processes[i].at == 0 and self.current_time == 0:
                    #set it to negative temporarly 
                    self.processes[self.processes.index(processes[i])].rt = -1
                else:
                    self.processes[self.processes.index(processes[i])].rt = self.current_time - processes[i].at

            # [1] add process to grant chart 
            if f"P{processes[i].pid}({processes[i].bt})" not in self.grant_chart and prev_p is not None:
                if prev_p.pid != processes[i].pid or self.current_time == 0:

                    self.grant_chart.append(f"P{processes[i].pid}({processes[i].bt})")
                    

            # check if any new process have arrived to the queue
            for j in processes:
                if j not in self.arrived and j.at == self.current_time:
                    #print that the process just arraived to the queue
                    self.streamlit_print_gc(j.pid, processes, processes[i], page_no, processes[i])
                    self.arrived.append(j)

            #decrement the burst time 
            processes[i].bt -= 1

            #increment waiting time for all processes in waiting queue
            for j in processes:
                # dont increment for the current running process
                if j.at <= self.current_time and j != processes[i]:
                    self.processes[self.processes.index(j)].wt += 1

            #increment the current time and decrement the quantum 
            self.current_time += 1
            counter_q -= 1

            p = None # in this variable we will pop the process if context switch

            #check if processes finished using BT
            if processes[i].bt == 0:
                #set the finish time for the process
                self.processes[self.processes.index(processes[i])].ft = self.current_time

            # check if any process has arrived and append it to the queue
            if self.current_time > 0:
                for process in self.processes:
                    if process.at == self.current_time:
                        processes.append(process)

            if processes[i].bt == 0 or counter_q == 0:
                # CONTEXT SWITCH HAPPEND
                p = processes.pop(i)

                #if quantum is zero then select another process
                if counter_q == 0:
                    if p.bt != 0:
                        processes.append(p)

                #reset quantum 
                counter_q = self.q

                #set start time of grantchart cell
                self.gc_st.append(self.current_time)

                #set finish time for grantchart 
                self.gc_ft.append(self.current_time)

            if p is None:
                #same process is running (this is just to test the grant chart condition, see [1])
                prev_p = processes[i]
        
        
        #set TAT for all the processes:
        for p in self.processes:
            # TAT = finish time - arrive time
            p.tat = p.ft - p.at

        Avg_WT= sum([i.wt for i in self.processes])/len(self.processes)
        Avg_TAT= sum([i.tat for i in self.processes])/len(self.processes)
        Avg_RT= sum([i.rt if i.rt !=-1 else 0 for i in self.processes ])/len(self.processes)

        return Avg_WT, Avg_TAT, Avg_RT


            