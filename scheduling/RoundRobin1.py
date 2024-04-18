import streamlit as st
from streamlit_extras import add_vertical_space as avs

class RoundRobin:
    def __init__(self, filepath):
        self.p,self.quantim = self.read_processes(filepath)
        self.num_of_processes = len(self.p)
        self.BT = [i[1] for i in self.p]  # Burst Time (corrected index based on file input structure)
        self.AT = [i[0] for i in self.p]  # Arrival Time
        self.time_passed = 0
        self.execution_time = [-1] * self.num_of_processes  # To track the first execution time
        self.WT = [0] * self.num_of_processes  # Waiting Time
        self.RT = [0] * self.num_of_processes  # Response Time, initially not calculated
        self.TAT = [0] * self.num_of_processes  # Turnaround Time
        self.Ready_queue = [i for i in range(self.num_of_processes)]  # Ready queue initialized with indices


# Reading from the file
    def read_processes(self, filepath, page_no="1"):
        #Reading the processes from the file and then print them
        processes = [] #  store the process that will be read from the file in the list
        with open(filepath, 'r') as file:  # opening the file in read mode
            quantum = int(file.readline())  # read the quantum from the file

            for line in file:
                d = line.strip("\n")
                d = d.split(" ")
                processes.append((int(d[0]), int(d[1]),int(d[2]))) # append them to the processes's list

                if page_no == '1':
                    st.markdown(f"Read process: PID={int(d[0])}, Arrival Time={int(d[1])}, Burst Time={int(d[2])}")
        return processes,quantum



# The Execution Part
    def schedule(self, page_no="1"):
        if page_no == '1':
            st.subheader(":green[Starting Round Robin Scheduling]")
        while self.Ready_queue: # scheduling loop until all processes finish
            i = self.Ready_queue.pop(0) # get the next process from the ready queue
            if self.BT[i] > 0:  # the process need CPU

                if self.execution_time[i] == -1:  # if it is the first execution of the process
                    self.execution_time[i] = self.time_passed   #save the start time of the process execution
                    self.RT[i] = self.time_passed - self.AT[i]  #calculate responce time

                #execute the process for the quantum or until it finishes
                exec_time = min(self.BT[i], self.quantim)
                self.BT[i] -= exec_time
                self.time_passed += exec_time

                #prints execution info:
                if page_no == '1':
                    st.markdown(f"⏰: {self.time_passed}ms | Process ID: {self.p[i][2]} is :green[Running] ")



                #aclculate turnaround and waiting times if the process terminate
                if self.BT[i] == 0:
                    self.TAT[i] = self.time_passed - self.AT[i]  # total time (arrival to termination) --> current time - AT
                    self.WT[i] = self.TAT[i] - self.p[i][1] #waiting in the ready queue -->TAT -BT
                    if page_no == '1':
                        st.markdown(f"⏰: {self.time_passed}ms | Process ID: {self.p[i][2]} is :red[Finished!] ")

                if self.BT[i] > 0:
                    self.Ready_queue.append(i)  # return the procces back to the queue




        Avg_WT = sum(self.WT) / self.num_of_processes
        Avg_TAT = sum(self.TAT) / self.num_of_processes
        Avg_RT = sum(self.RT) / self.num_of_processes

        return Avg_WT, Avg_TAT, Avg_RT







