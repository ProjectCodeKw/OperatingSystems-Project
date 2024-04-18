class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.response_time = -1

def read_processes(file_path):
    # Reading the processes from the file and then print them
    processes = []  #  store the process that will be read from the file in the list
    with open(file_path, 'r') as file:   # opening the file in read mode
        for line in file:     # iterate the lines
            parts = line.split()  # splitting each line into alist of strings based on the whitespace
            if len(parts) != 3:
                raise ValueError("Each line must contain exactly three numbers")
            PID, AT, BT = map(int, parts)    # taking each element in the list parts and converting it into integer
            processes.append(Process(PID, AT, BT))  # append them to the processes's list
            print(f"Read process: PID={PID}, Arrival Time={AT}, Burst Time={BT}")
    return processes



def srtf_scheduling(processes):
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
                running.response_time = system_time - running.arrival_time
                avg_response_time += running.response_time # total response time +response time

            running.remaining_time -= 1  # to simulate the procces execution
            print(f"Process ID: {running.pid} is running")

            if running.remaining_time == 0: # the process terminated
                print(f"Process ID: {running.pid} is Finished!")
                completed_processes += 1
                avg_waiting_time += system_time - running.arrival_time - running.burst_time + 1 # update the WT and TAT
                avg_turnaround_time += system_time - running.arrival_time + 1

        system_time += 1



    avg_waiting_time /= len(processes)
    avg_turnaround_time /= len(processes)
    avg_response_time /= len(processes)

    return avg_waiting_time, avg_turnaround_time, avg_response_time


if __name__ == "__main__":
    file_path = r'C:\Users\Reem\Desktop\OS\project_445\processes_input'

    processes = read_processes(file_path)
    avg_waiting_time, avg_turnaround_time, avg_response_time = srtf_scheduling(processes)
    print("\nAverage Waiting Time =", avg_waiting_time)
    print("Average Turnaround Time =", avg_turnaround_time)
    print("Average Response Time =", avg_response_time)

