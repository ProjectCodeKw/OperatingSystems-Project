import streamlit as st
from streamlit_extras import add_vertical_space as avs
class SRTF:
    def __init__(self, filepath):
        self.p = self.read_processes(filepath)
        self.num_of_processes = len(self.p)
        self.BT = [i[2] for i in self.p]  # Burst Time
        self.AT = [i[1] for i in self.p]  # Arrival Time
        self.time_passed = 0
        self.execution_time = [-1] * self.num_of_processes  # To track the first execution time
        self.WT = [0] * self.num_of_processes  # Waiting Time
        self.RT = [0] * self.num_of_processes  # Response Time, initially not calculated
        self.TAT = [0] * self.num_of_processes  # Turnaround Time
        self.Ready_queue = [i for i in range(self.num_of_processes)]  # Ready queue initialized

    # Reading from the file
    def read_processes(self, filepath, page_no="1"):
        # Reading the processes from the file and then print them
        processes = []  # store the process that will be read from the file in the list
        with open(filepath, 'r') as file:  # opening the file in read mode
            quantum = int(file.readline())  # read the quantum from the file
            for line in file:
                d = line.strip("\n")
                d = d.split(" ")
                processes.append((int(d[0]), int(d[1]), int(d[2])))  # append them to the processes's list

                if page_no == '1':
                    st.markdown(f"Read process: PID={int(d[0])}, Arrival Time={int(d[1])}, Burst Time={int(d[2])}")
        return processes


    # The Execution Part
    def schedule(self, page_no='1'):
        if page_no == '1':
            st.markdown("Starting Shortest Remaining Time First Scheduling")
        while self.Ready_queue:  # scheduling loop until all processes finish
            for i in self.Ready_queue:  # print that process i is arrived if time_passed = its AT
                if self.AT[i] == self.time_passed:
                    if page_no == '1':
                        st.markdown(f"⏰: {self.time_passed}ms | Process ID: {self.p[i][0]} | Arrived ")


            min_remaining_time = float('inf')
            shortest_process_index = -1

            # Find the process with the shortest remaining burst time and has arrived
            for i in self.Ready_queue:
                if self.BT[i] > 0 and self.AT[i] <= self.time_passed and self.BT[i] < min_remaining_time:
                    min_remaining_time = self.BT[i]
                    shortest_process_index = i

            if shortest_process_index == -1:
                # No processes are ready to execute we need to wait for the next arrival
                self.time_passed += 1
                continue

            i = shortest_process_index

            if self.execution_time[i] == -1:  # if it is the first execution of the process
                self.execution_time[i] = self.time_passed  # save the start time of the process execution
                self.RT[i] = self.time_passed - self.AT[i]  # calculate response time

            exec_time = min(self.BT[i], 1)  ## execute for 1 unit of time ( 1 BT)
            self.BT[i] -= exec_time
            self.time_passed += exec_time

            # prints execution info:
            if page_no == '1':
                st.markdown(f"⏰: {self.time_passed}ms | Process ID: {self.p[i][0]} is :green[Running] ")

            # calculate TAT and WT if the process terminates
            if self.BT[i] == 0:
                self.TAT[i] = self.time_passed - self.p[i][1]  # total time (arrival to termination) --> current time - AT
                self.WT[i] = self.TAT[i] - self.p[i][2]  # waiting in the ready queue --> TAT - BT
                if page_no == '1':
                    st.markdown(f"⏰: {self.time_passed}ms | Process ID: {self.p[i][0]} is :red[Finished!] ")

                # remove the process from the ready queue if it finishes execution
                self.Ready_queue.remove(i)

        Avg_WT = sum(self.WT) / self.num_of_processes
        Avg_TAT = sum(self.TAT) / self.num_of_processes
        Avg_RT = sum(self.RT) / self.num_of_processes

        return Avg_WT, Avg_TAT, Avg_RT

