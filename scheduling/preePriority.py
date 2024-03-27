
class PreemptivePriority:
    def __init__(self, processes:list):
        self.processes = processes

    def simulate_CPU(self):
        current_time = 0
        waiting_queue = []
        temp_q = []
        process_completed = 0
        while True:
            temp_q = [p for p in self.processes if p.at == current_time and p.pid not in waiting_queue]
            waiting_queue.extend(temp_q)

            #get highest priority
            running_p = waiting_queue[0]
            running_p_index  = 0 
            for p in waiting_queue[1:len(waiting_queue)]:
                if p.priority < running_p.priority:
                    # change current running process
                    running_p = p
                    running_p_index = waiting_queue.index(p)
            
            #run the process:
            print(f"P{running_p.pid}-", end="")

            # subtract the BT from the running process
            waiting_queue[running_p_index].bt = running_p.bt - 1

            # remove the process if the burst time is now 0
            if waiting_queue[running_p_index].bt == 0:
                p = waiting_queue.pop(running_p_index)
                process_completed+= 1

            #increment the time
            current_time += 1

            #check if the all the processes have ran:
            if process_completed == len(self.processes):
                print(f"\nAll processes have finished, Time needed: {current_time}")
                return
            
            


