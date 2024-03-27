from scheduling.process import Process
from scheduling.preePriority import PreemptivePriority


def main():
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

    # test the preemptive scheduling
    preemptive = PreemptivePriority(p_objects)
    preemptive.simulate_CPU()

main()