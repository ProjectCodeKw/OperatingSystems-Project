#ibrahim mohsen alsulaiman 2201122237 SRTF algorithm

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.response_time = -1

def read_processes(file_path):
    processes = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) != 4:
                raise ValueError("Each line must contain exactly four numbers")
            pid, arrival_time, burst_time = map(int, parts[:3])
            processes.append(Process(pid, arrival_time, burst_time))
            print(f"Read process: PID={pid}, Arrival Time={arrival_time}, Burst Time={burst_time}")
    return processes



def srtf_scheduling(processes):
    system_time = 0
    completed_processes = 0
    avg_waiting_time = avg_turnaround_time = avg_response_time = 0

    while completed_processes < len(processes):
        shortest_remaining_time = float('inf')
        shortest_process_index = -1

        for i, process in enumerate(processes):
            if process.arrival_time <= system_time and process.remaining_time > 0:
                if process.remaining_time < shortest_remaining_time:
                    shortest_remaining_time = process.remaining_time
                    shortest_process_index = i

        if shortest_process_index != -1:
            running = processes[shortest_process_index]
            if running.response_time == -1:
                running.response_time = system_time - running.arrival_time
                avg_response_time += running.response_time

            running.remaining_time -= 1
            print(f"Process ID: {running.pid} is running")

            if running.remaining_time == 0:
                print(f"Process ID: {running.pid} is Finished!")
                completed_processes += 1
                avg_waiting_time += system_time - running.arrival_time - running.burst_time + 1
                avg_turnaround_time += system_time - running.arrival_time + 1

        system_time += 1

    avg_waiting_time /= len(processes)
    avg_turnaround_time /= len(processes)
    avg_response_time /= len(processes)

    return avg_waiting_time, avg_turnaround_time, avg_response_time


# Main execution
file_path = r'C:\Users\Reem\Desktop\OS\project_445\processes_input'

processes = read_processes(file_path)
avg_waiting_time, avg_turnaround_time, avg_response_time = srtf_scheduling(processes)
print("\nAverage Waiting Time =", avg_waiting_time)
print("Average Turnaround Time =", avg_turnaround_time)
print("Average Response Time =", avg_response_time)