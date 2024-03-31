from scheduling.process import Process
from scheduling.custom import Custom
from scheduling.preePriority import PreemptivePriority
import matplotlib.pyplot as plt
import numpy as np

def read_file():
    # returns a list of process objects
    f = open("input.txt", "r")
    processes_data = []
    q = int(f.readline())
    for line in f:
        d = line.strip("\n")
        d = d.split(" ")
        processes_data.append( [int(d[0]), int(d[1]),int(d[2]), int(d[3])] )

    #create process objects
    p_objects = []
    for p in processes_data:
        p_obj = Process(*p)
        p_objects.append(p_obj)

    f.close()
    return p_objects, q

def plotting(process_pid, pp, custom, title):
# Create figure and axis objects
    fig, ax = plt.subplots()

    # Set width of bar
    bar_width = 0.35

    # Set position of bar on X axis
    r1 = np.arange(len(process_pid))
    r2 = [x + bar_width for x in r1]

    # Make the plots
    ax.bar(r1, pp, color='blue', width=bar_width, edgecolor='grey', label='PP')
    ax.bar(r2, custom, color='green', width=bar_width, edgecolor='grey', label='MLFQ')

    # Adding labels and title
    ax.set_xlabel('Process PID')
    ax.set_ylabel(f'{title} Time')
    ax.set_title(f'{title} Time Comparison')
    ax.set_xticks([r + bar_width / 2 for r in range(len(process_pid))])
    ax.set_xticklabels(process_pid)
    ax.legend()


def main():
    p_objects, q = read_file()
    
    # test pp algorithm scheduling
    pp = PreemptivePriority(p_objects)
    pp.simulate_pp()
    pp.calculate_average()

    #store pp response times for all processes 
    pp_rt = [i.rt for i in pp.processes]
    #store pp waiting times for all processes 
    pp_wt = [i.wt for i in pp.processes]
    #store pp TAT times for all processes 
    pp_tat = [i.tat for i in pp.processes]

    p_objects, q = read_file()

    # test custom algorithm scheduling
    custom = Custom(p_objects, q)
    custom.determine_queue()
    custom.calculate_average()

    #store custom response times for all processes 
    custom_rt = [i.rt for i in custom.processes]
    #store custom waiting times for all processes 
    custom_wt = [i.wt for i in custom.processes]
    #store custom TAT times for all processes 
    custom_tat = [i.tat for i in custom.processes]
    
    # get the averages 
    averages_pp = [pp.avg_rt, pp.avg_wt, pp.avg_tat ] # avg rt, avg wt, avg tat
    averages_mlfq = [custom.avg_rt, custom.avg_wt, custom.avg_tat ] # avg rt, avg wt, avg tat

    process_pid = [i.pid for i in p_objects]

    # Create threads for plotting
    plotting(process_pid, pp_rt, custom_rt, "Response")
    plotting(process_pid, pp_wt, custom_wt, "Waiting")
    plotting(process_pid, pp_tat, custom_tat, "Turn Around")

    plt.show()

main()