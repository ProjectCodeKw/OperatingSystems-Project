from scheduling.process import Process
from scheduling.custom import Custom
from scheduling.preePriority import PreemptivePriority
from scheduling.rr import RoundRobin
from scheduling.SRTF import SRTF
import matplotlib.pyplot as plt

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


def plotting(process_pid, pp_rt, custom_rt, rr_rt, strf_rt, pp_wt, custom_wt, rr_wt, strf_wt, pp_tat, custom_tat, rr_tat, strf_tat):
    # Plot for Response Time
    fig_rt, ax_rt = plt.subplots(figsize=(8, 6))
    ax_rt.plot(process_pid, pp_rt, marker='o', color='#8bd8bd', label='PP')
    ax_rt.plot(process_pid, custom_rt, marker='o', color='#3b8a0b', label='MLFQ')
    ax_rt.plot(process_pid, rr_rt, marker='o', color='#a3193b', label='RR')
    ax_rt.plot(process_pid, strf_rt, marker='o', color='#ffa500', label='SRTF')
    ax_rt.set_title(f'Response Time')
    ax_rt.set_xlabel('Process PID')
    ax_rt.set_ylabel('Time')
    ax_rt.legend()

    for x, y in zip(process_pid, pp_rt):
        ax_rt.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, custom_rt):
        ax_rt.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, rr_rt):
        ax_rt.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, strf_rt):
        ax_rt.text(x, y, f'({x}, {y})', ha='center', va='bottom')

    fig_rt.tight_layout()

    # Plot for Waiting Time
    fig_wt, ax_wt = plt.subplots(figsize=(8, 6))
    ax_wt.plot(process_pid, pp_wt, marker='o', color='#8bd8bd', label='PP')
    ax_wt.plot(process_pid, custom_wt, marker='o', color='#3b8a0b', label='MLFQ')
    ax_wt.plot(process_pid, rr_wt, marker='o', color='#a3193b', label='RR')
    ax_wt.plot(process_pid, strf_wt, marker='o', color='#ffa500', label='SRTF')
    ax_wt.set_title(f'Waiting Time')
    ax_wt.set_xlabel('Process PID')
    ax_wt.set_ylabel('Time')
    ax_wt.legend()

    for x, y in zip(process_pid, pp_wt):
        ax_wt.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, custom_wt):
        ax_wt.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, rr_wt):
        ax_wt.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, strf_wt):
        ax_wt.text(x, y, f'({x}, {y})', ha='center', va='bottom')

    fig_wt.tight_layout()

    # Plot for Turn Around Time
    fig_tat, ax_tat = plt.subplots(figsize=(8, 6))
    ax_tat.plot(process_pid, pp_tat, marker='o', color='#8bd8bd', label='PP')
    ax_tat.plot(process_pid, custom_tat, marker='o', color='#3b8a0b', label='MLFQ')
    ax_tat.plot(process_pid, rr_tat, marker='o', color='#a3193b', label='RR')
    ax_tat.plot(process_pid, strf_tat, marker='o', color='#ffa500', label='SRTF')
    ax_tat.set_title(f'Turn Around Time')
    ax_tat.set_xlabel('Process PID')
    ax_tat.set_ylabel('Time')
    ax_tat.legend()

    for x, y in zip(process_pid, pp_tat):
        ax_tat.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, custom_tat):
        ax_tat.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, rr_tat):
        ax_tat.text(x, y, f'({x}, {y})', ha='center', va='bottom')
    for x, y in zip(process_pid, strf_tat):
        ax_tat.text(x, y, f'({x}, {y})', ha='center', va='bottom')

    fig_tat.tight_layout()

    return fig_rt, fig_wt, fig_tat



def main():
    p_objects, q = read_file()
    
    # test pp algorithm scheduling
    pp = PreemptivePriority(p_objects)
    pp.simulate_pp(page_no="2")
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
    custom.determine_queue(page_no="2")
    custom.calculate_average()

    #store custom response times for all processes 
    custom_rt = [i.rt for i in custom.processes]
    #store custom waiting times for all processes 
    custom_wt = [i.wt for i in custom.processes]
    #store custom TAT times for all processes 
    custom_tat = [i.tat for i in custom.processes]

    p_objects, q = read_file()

    # test rr algorithm scheduling
    rr = RoundRobin(p_objects, q)
    Avg_WT, Avg_TAT, Avg_RT = rr.roundrobin(page_no="2")

    #store rr response times for all processes 
    rr_rt = [i.rt if i.rt !=-1 else 0 for i in rr.processes ]
    #store rr waiting times for all processes 
    rr_wt = [i.wt for i in rr.processes]
    #store rr TAT times for all processes 
    rr_tat = [i.tat for i in rr.processes]

    # test SRTF algorithm scheduling
    srtf = SRTF("input.txt", '2')
    avg_waiting_time, avg_turnaround_time, avg_response_time = srtf.schedule(page_no="2")
    strf_rt = srtf.RT
    strf_wt = srtf.WT
    strf_tat = srtf.TAT

    # get the averages 
    averages_pp = [pp.avg_rt, pp.avg_wt, pp.avg_tat ] # avg rt, avg wt, avg tat
    averages_mlfq = [custom.avg_rt, custom.avg_wt, custom.avg_tat ] # avg rt, avg wt, avg tat
    average_rr = [Avg_RT, Avg_WT, Avg_TAT]
    average_srtf = [avg_response_time, avg_waiting_time, avg_turnaround_time]

    process_pid = [i.pid for i in p_objects]

    plotting(process_pid, pp_rt, custom_rt, rr_rt, strf_rt, pp_wt, custom_wt, rr_wt, strf_wt, pp_tat, custom_tat, rr_tat, strf_tat)

    plt.show()

main()