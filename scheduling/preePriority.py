import streamlit as st
import pandas as pd
from streamlit_extras import add_vertical_space as avs


class PreemptivePriority:
    def __init__(self, processes: list):
        self.processes = processes
        self.avg_rt = 0
        self.avg_wt = 0
        self.avg_tat = 0
        self.grant_chart = []
        self.current_time = 0
        self.time_record = []  # keep track of the time printed in streamlit_print_gc()

        # these two lists are for grant chart printing format:
        self.gc_ft = []
        self.gc_st = [0]

    def streamlit_print_gc(self, pid, waiting_q, running_p, page_no, next_running_p):
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
                    f":green[CURRENT RUNNING PROCESS: P{running_p.pid}({running_p.bt}, {running_p.priority})]"
                )
                st.caption("Ready queue")
                for i in waiting_q:
                    if i.pid != running_p.pid:
                        pid_list.append(f"P{i.pid}({i.bt}, {i.priority})")

                st.code(pid_list, language="python")

            if self.grant_chart != []:
                if next_running_p == running_p:
                    st.markdown("**Current Grant chart with the running processes:**")
                else:
                    st.markdown(
                        f"**Grant chart after prioritizing P{next_running_p.pid}({next_running_p.bt}, {next_running_p.priority})**"
                    )

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

    def simulate_pp(self, page_no="1"):
        waiting_queue = []
        temp_q = []
        prev_process = None
        process_completed = 0

        while True:
            temp_q = [
                p
                for p in self.processes
                if p.at == self.current_time and p not in waiting_queue
            ]
            waiting_queue.extend(temp_q)

            # get highest priority
            running_p = waiting_queue[0]
            running_p_index = 0

            for p in waiting_queue[1 : len(waiting_queue)]:
                if p.priority < running_p.priority:
                    # context switch will happen:
                    # change current running process
                    running_p = p
                    running_p_index = waiting_queue.index(p)

            if self.current_time == 0:
                # no prev process
                # store the prev process so we dont print it in a row multiple times
                prev_process = running_p

            if temp_q != []:
                # a new process have arravied
                for i in temp_q:
                    self.streamlit_print_gc(
                        i.pid, waiting_queue, prev_process, page_no, running_p
                    )

            # subtract the BT from the running process
            self.processes[self.processes.index(running_p)].bt -= 1

            # increment waiting time for all none running processes
            for process in waiting_queue:
                if process != running_p:
                    self.processes[self.processes.index(process)].wt += 1

            # remove the process if the burst time is 0
            if waiting_queue[running_p_index].bt == 0:
                waiting_queue.remove(running_p)
                process_completed += 1

                # set finish time:
                running_p.ft = self.current_time

                # set the TAT
                running_p.tat = running_p.ft - running_p.at + 1

            if self.current_time == 0:
                # get response time:
                if (
                    running_p.rt == 0
                    and f"P{running_p}({running_p.bt}, {running_p.priority})"
                    not in self.grant_chart
                ):
                    # response time is calculated for the first burst
                    running_p.rt = self.current_time - running_p.at

                # store the process in prev so we check again for context switch
                prev_process = running_p

                # run the process:
                self.grant_chart.append(
                    f"P{running_p.pid}({running_p.bt+1}, {running_p.priority})"
                )

            elif prev_process != running_p:
                # context switch happend, processes have changed

                # get response time:
                if (
                    running_p.rt == 0
                    and f"P{running_p}({running_p.bt}, {running_p.priority})"
                    not in self.grant_chart
                ):
                    # response time is calculated for the first burst only
                    running_p.rt = self.current_time - running_p.at

                prev_process = running_p  # store the process in prev so we check again for context switch

                # run the process:
                self.grant_chart.append(
                    f"P{running_p.pid}({running_p.bt+1}, {running_p.priority})"
                )

                # append finish time to grant chart
                self.gc_ft.append(self.current_time)
                self.gc_st.append(self.current_time)

            # increment the time
            self.current_time += 1

            # check if the all the processes have ran:
            if process_completed == len(self.processes):
                return

    def calculate_average(self):
        n = len(self.processes)

        # get avg response time
        for p in self.processes:
            # like we assumed if rt is -1 then it is actually 0 so no need to sum it
            self.avg_rt += p.rt

        self.avg_rt = self.avg_rt / n

        # get average waiting time
        for p in self.processes:
            self.avg_wt += p.wt

        self.avg_wt = self.avg_wt / n

        # get average TAT
        for p in self.processes:
            self.avg_tat += p.tat

        self.avg_tat = self.avg_tat / n

        # add the last current time
        self.gc_ft.append(self.current_time)
