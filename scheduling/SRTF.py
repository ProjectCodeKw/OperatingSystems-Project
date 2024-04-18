import streamlit as st
from streamlit_extras import add_vertical_space as avs

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.response_time = -1

class SRTF:
    def __init__(self, file_path, page_no="1"):
        self.processes = self.read_processes(file_path)

    def read_processes(self, file_path, page_no="1"):
        # Reading the processes from the file and then print them
        processes = []  #  store the process that will be read from the file in the list
        with open(file_path, 'r') as file:   # opening the file in read mode
            quantum = int(file.readline())  # read the quantum from the file
            for line in file:     # iterate the lines
                d = line.strip("\n")
                d = d.split(" ")
                processes.append(Process(int(d[0]), int(d[1]),int(d[2])))  # append them to the processes's list
                if page_no == '1':
                    st.markdown(f"Read process: PID={int(d[0])}, Arrival Time={int(d[1])}, Burst Time={int(d[2])}")
        return processes


    def srtf_scheduling(self, page_no="1"):
        processes = self.processes
        system_time = 0  #Keeping track of the current system time
        completed_processes = 0  # counter that count the number of processes that have been terminated
        avg_waiting_time = avg_turnaround_time = avg_response_time = 0

        while completed_processes < len(processes): # loop that will continue until all processes finish

            # track the shortest remaining time and the index of the process
            shortest_remaining_time = float('inf')
            shortest_process_index = -1

            for i, process in enumerate(processes):  #will iterate over each process
                if process.arrival_time <= system_time and process.remaining_time > 0:  # It checks if a process has arrived &  if it still has remaining time
                    if process.remaining_time < shortest_remaining_time:
                        # update the shortest remaining time and the index of the shortest process
                        shortest_remaining_time = process.remaining_time
                        shortest_process_index = i

            if shortest_process_index != -1: # if there is a process to run
                running = processes[shortest_process_index]  #the process is set to be running

                if running.response_time == -1:
                    # update the running time
                    running.response_time = abs(system_time - running.arrival_time)
                    avg_response_time += running.response_time # total response time +response time

                running.remaining_time -= 1  # to simulate the procces execution
                if page_no=="1":
                    st.markdown(f"⏰: {system_time}ms | Process ID: {running.pid} is :green[Running]")

                if running.remaining_time == 0: # the process terminated
                    if page_no=="1":
                        st.markdown(f"⏰: {system_time}ms  | Process ID: {running.pid} is :red[Finished!]")
                    completed_processes += 1
                    avg_waiting_time += system_time - running.arrival_time - running.burst_time + 1 # update the WT and TAT
                    avg_turnaround_time += system_time - running.arrival_time + 1

            system_time += 1

        avg_waiting_time /= len(processes)
        avg_turnaround_time /= len(processes)
        avg_response_time /= len(processes)

        return avg_waiting_time, avg_turnaround_time, avg_response_time



