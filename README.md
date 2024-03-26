# OperatingSystems-Project

This programming project is to simulate a few CPU scheduling policies discussed in the
class. You will write a program (using any language you prefer) to implement a simulator
with different scheduling algorithms. The simulator selects a task to run from ready
queue based on the scheduling algorithm. Since the project intends to simulate a CPU
scheduler so it does not require any actual process creation or execution. When a task is
scheduled, the simulator will simply print out what task is selected to run at a time. It
outputs a way similar to Gantt chart style (horizontal or vertical) specifying the system
time and the process currently running. If a new task arrives, it should print the
system time and the task just arrived.

________________________________________________________________

The selected scheduling algorithms to implement in this project are: 
a. Preemptive priority. (PP)
b. Round Robin (RR)
c. Shortest Remaining Time First (SRTF).
d. Multi-level feedback queue Custom algorithm

**Custom Algorithm:
This algorithm is yours to design, though it must meet the following criteria:
a. It should be preemptive.
b. It should have 3 level queues.
c. Each queue should use a scheduling algorithm. (you can use the algorithms you
implemented in parts a – c or any other scheduling algorithm of your choice).
Note the queues can use the same scheduling algorithm but with different
specifications, like different quantums for example.
d. It should have a method to determine which queue a new process will enter.
e. It should have a method to upgrade a process or a method to demote a process
or both.
You should explain your custom algorithm in detail in the report.
It is one program, but each member of the team should be responsible for implementing
at least an algorithm and all members are responsible for implementing the custom
algorithm.

________________________________________________________________


The task information will be read from an input file. The format is:

q
pid arrival_time burst_time priority

All of fields are integer type where:
 q: is the time quantum used by RR
 pid is a unique numeric process ID
 arrival_time is the time when the task arrives in the unit of milliseconds
 burst_time is the CPU time requested by a task, in the unit of milliseconds
 priority is an integer that represents the priority of the task, a smaller number means a higher priority.
 
This input file can be extended to provide any necessary input for your custom algorithm.
If needed. The changes should be described clearly in the report.
A sample input file is provided. However, this is not the input file that your algorithms
will be tested and graded on.

Sample Input: input.txt
```
3
1 0 10 3
2 0 5 4
3 3 5 2
4 7 4 2
5 10 6 1```
6 10 7 4


