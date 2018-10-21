import copy
from operator import attrgetter


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


def get_arrivals(processes):
    arrivals = [processes[0]]
    arrival = processes[0]

    for i in range(1, len(processes)):
        if arrival.arrival == processes[i].arrival:
            arrivals.append(processes[i])
        else:
            break
    return arrivals


def to_execute(processes_queue):
    options = [processes_queue[0]]
    first_option = processes_queue[0]
    for process in processes_queue:
        if process.burst_time == first_option.burst_time:
            options.append(process)
        else:
            break
    return min(options, key=attrgetter('arrival'))


def restore_burst_time(processes_srpt_output, processes):
    for i in range(0, len(processes)):
        processes_srpt_output[i].burst_time = processes[i].burst_time

    return processes_srpt_output


def srpt(processes):
    time = 0
    processes_srpt_output = []
    processes_queue = []
    processes_srpt = copy.deepcopy(processes)
    processes_srpt.sort(key=lambda process: process.arrival)
    while True:
        arrivals = get_arrivals(processes_srpt)
        processes_srpt = processes_srpt[len(arrivals):]
        processes_queue.extend(arrivals)
        processes_queue.sort(key=lambda process: process.burst_time)
        process_to_execute = to_execute(processes_queue)

        if len(processes_srpt) == 0:
            break

        next_arrival = processes_srpt[0]
        if process_to_execute.burst_time <= next_arrival.arrival - time:
            process_to_execute.waiting_time += time - process_to_execute.arrival
            time += process_to_execute.burst_time
            process_to_execute.turnaround_time = time
            processes_queue.remove(process_to_execute)
            processes_srpt_output.append(process_to_execute)
        else:
            process_to_execute.burst_time -= (next_arrival.arrival - time)
            process_to_execute.waiting_time += (time - next_arrival.arrival)
            time = next_arrival.arrival

    for process in processes_queue:
        process.waiting_time += time - process_to_execute.arrival
        time += process.burst_time
        process.turnaround_time = time
        processes_srpt_output.append(process)

    processes_srpt_output.sort(key=lambda process: process.label)
    processes_srpt_output = restore_burst_time(processes_srpt_output, processes)
    display_processes(processes_srpt_output, "SRPT")


def best_priority(processes):
    best = processes[0]
    for i in range(1, len(processes)):
        process = processes[i]
        if process.priority == best.priority:
            if process.label < best.label:
                best = process
        else:
            break
    return best


def priority(processes):
    time = 0
    processes_priority_out = []
    processes_priority = copy.deepcopy(processes)
    processes_priority.sort(key=lambda process: process.priority)
    while len(processes_priority) != 0:
        process = best_priority(processes_priority)
        process.waiting_time = time
        time += process.burst_time
        process.turnaround_time = time
        processes_priority.remove(process)
        processes_priority_out.append(process)
    processes_priority_out.sort(key=lambda process: process.label)
    display_processes(processes_priority_out, "Priority")


def awt(processes):
    return sum(process.waiting_time for process in processes) / len(processes)


def att(processes):
    return sum(process.turnaround_time for process in processes) / len(processes)


def display_processes(processes, scheduling):
    print(scheduling)
    for process in processes:
        print(process)
    print("Average waiting time: {}".format(awt(processes)))
    print("Average turnaround time: {}".format(att(processes)), end="\n\n")


processes = init_processes('process1.txt')
fcfs(processes)
sjf(processes)
srpt(processes)
priority(processes)
