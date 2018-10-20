import copy


class Process:
    def __init__(self, label, arrival, burst_time, priority):
        self.label = label
        self.arrival = arrival
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0
        self.turnaround_time = 0

    def __str__(self):
        return "process: {0:>3};    arrival: {1:>3};    burst time: {2:>3};    priority: {3:>3};    waiting time: {4:>3};    turnaround time: {5:>3};".format(self.label, self.arrival, self.burst_time, self.priority, self.waiting_time, self.turnaround_time)


def init_processes(filename):
    processes = []
    fh = open(filename, 'r')
    first_line = True
    for line in fh:
        if first_line:
            first_line = False
            continue
        process_values = line.split()
        process = Process(int(process_values[0]), int(process_values[1]),
                          int(process_values[2]), int(process_values[3]))
        processes.append(process)
    fh.close()
    return processes


def fcfs(processes):
    time = 0
    processes_fcfs = copy.deepcopy(processes)
    for process in processes_fcfs:
        process.waiting_time = time
        time += process.burst_time
        process.turnaround_time = time
    display_processes(processes_fcfs, "FCFS")


def sjf(processes):
    time = 0
    processes_sjf = copy.deepcopy(processes)
    processes_sjf.sort(key=lambda process: process.burst_time)
    for process in processes_sjf:
        process.waiting_time = time
        time += process.burst_time
        process.turnaround_time = time
    processes_sjf.sort(key=lambda process: process.label)
    display_processes(processes_sjf, "SJF")


def srpt(processes):
    pass
    # time = 0
    # processes_srpt = copy.deepcopy(processes)
    # processes_srpt.sort(key=lambda process: process.arrival)
    # display_processes(processes_srpt, "SRPT")


def display_processes(processes, scheduling):
    print(scheduling)
    for process in processes:
        print(process)
    print()


processes = init_processes('process1.txt')
fcfs(processes)
sjf(processes)
srpt(processes)
