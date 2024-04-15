import streamlit as st
import pandas as pd
from streamlit_extras import add_vertical_space as avs

class RoundRobin():
    def __init__(self, processes:list, q:int):
        self.processes = processes
        self.q = q
        self.avg_rt = 0
        self.avg_wt = 0
        self.avg_tat = 0
        self.grant_chart = []
        self.current_time = 0
        self.time_record = [] # keep track of the time printed in streamlit_print_gc()

        #these two lists are for grant chart printing format:
        self.gc_ft = []
        self.gc_st = []

        #keep track of completed processes..
        self.process_completed  = 0


    def round_robin(self, page_no = "1"):
        ready_q = []
        while self.process_completed < len(self.processes):  

            self.gc_st.append(self.current_time)

            temp_q = [p for p in self.processes if p.at == self.current_time and p not in ready_q]
            ready_q.extend(temp_q)

            running_p = ready_q.pop(0)

            if self.current_time == 0:
                for pro in temp_q:
                        self.streamlit_print_gc(pro.pid, ready_q, running_p, page_no, running_p)

            for i in range(self.q):
                if running_p.bt != 0:

                    #set response time
                    if i==0 and running_p.bt == 0:
                        running_p.rt = self.current_time

                    running_p.bt -= 1
                    self.current_time += 1

                    temp_q = [p for p in self.processes if p.at == self.current_time and p not in ready_q ]
                    ready_q.extend(temp_q)

                    if i==3:
                        self.grant_chart.append(f'P{running_p.pid}({running_p.bt})')

                    for pro in temp_q:
                        self.streamlit_print_gc(pro.pid, ready_q, running_p, page_no, running_p)

                    #increment waiting time for all non running processes
                    for process in self.processes:
                        if process != running_p:
                            process.wt += 1

            if running_p.bt == 0:   
                # process has been termindated
                self.process_completed += 1
                self.grant_chart.append(f'P{running_p.pid}({running_p.bt})')
                # set the TAT 
                running_p.tat = self.current_time - running_p.at 

            #--- Q TIME FINISHED BUT PROCESS BT DID NOT FINISH ---
            ready_q.append(running_p)
            

            #append process finish time
            self.gc_ft.append(self.current_time)


        self.avg_wt = sum([p.wt for p in self.processes]) /  len(self.processes)
        self.avg_tat = sum([p.tat for p in self.processes]) /  len(self.processes)
        self.avg_rt = sum([p.rt for p in self.processes]) / len(self.processes)
             
    
    def streamlit_print_gc(self, pid, waiting_q, running_p, page_no, next_running_p):
            if page_no == "1":
                
                if self.current_time not in self.time_record:
                    if self.current_time != 0: st.markdown('---')
                    c1,c2,c3 = st.columns(3)
                    with c2:
                        st.subheader(f"Time⏰: {self.current_time}ms")
                    
                        
                st.markdown(f"<span style='color:yellow;'>⚠️🚗 P{pid} process just arrived to the queue..</span>", unsafe_allow_html=True)
                use_next = False
                
                if self.grant_chart != []:
                    st.markdown("**Current Grant chart with the running processes:**")
                    
                    #print grant chart table
                    temp_ft = self.gc_ft.copy()
                    temp_ft.append(self.current_time)
                    time_list = [f'{self.gc_st[i]} -> {temp_ft[i]}ms' for i,v in enumerate(temp_ft) if temp_ft[i]!=self.gc_st[i]] 
                    p_list =  [i for i in self.grant_chart] 

                    # check if the two lists are the same size
                    if len(p_list) < len(time_list):
                        if temp_ft[-1] - self.gc_st[-1] > 1: 
                            p_list.append(f'P{running_p.pid}({running_p.bt})')
                        else:
                             p_list.append(f'P{waiting_q[1].pid}({waiting_q[1].bt})')
                             use_next = True
                    
                    data = [
                            tuple(p_list),
                    ]

                wq = waiting_q.copy()
                if wq !=[]:

                    pid_list = []
                    st.markdown(f":green[CURRENT RUNNING PROCESS: P{running_p.pid}({running_p.bt})]")
                    st.caption("Ready queue ")
                    for i in wq:
                        if i.pid != running_p.pid:
                            pid_list.append(f'P{i.pid}({i.bt})')
                        
                    if use_next:
                        pid_list.pop(0)
                    st.code(pid_list, language='python')

                if self.grant_chart != []: 
                    df1= pd.DataFrame(data, ['Process'],  columns=time_list)
                    st.table(df1)
                    
                
                if self.current_time not in self.time_record:
                    self.time_record.append(self.current_time)