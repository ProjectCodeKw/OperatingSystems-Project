from scheduling.process import Process
from scheduling.custom import Custom
from scheduling.preePriority import PreemptivePriority
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import pandas as pd
from time import sleep
from scheduling.rr import RoundRobin
from scheduling.SRTF import SRTF

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

    return q, p_objects

def set_session_state(b, page):
    st.session_state.b = b
    st.session_state.page = page


def get_session_state():
    if 'b' not in st.session_state:
        st.session_state.b =  False
    if 'page' not in st.session_state:
        st.session_state.page = '1'

    
    return st.session_state.b, st.session_state.page

def streamlit_app1():
    
    st.title("Main Page")
    st.markdown('---')

    #input file
    user_input = st.file_uploader("please upload your input txt file here or use the default data", type='txt')
    st.markdown("The file should follow the following structure:")

    #display input snippet
    contents = ''
    with open('input.txt', 'r') as f:
        for line in f:
            contents += line
        
    st.code(contents, language='python')

    st.markdown('---')
    avs.add_vertical_space(1)
    
    if user_input is not None:
        file_contents = user_input.getvalue().decode("utf-8")

        # Write the content to a new file named "new.txt"
        with open("input.txt", "w") as new_file:
            for line in file_contents:
                if line != '\n':
                    new_file.write(line)

        #display the user input:
        st.markdown("Your input:")
        st.code(file_contents, language='python')

        avs.add_vertical_space(1)

    tab_a, tab_b, tab_c, tab_d = st.tabs(["PP","RR", "SRTF", "MLFD Custom"])
    with tab_a:
        algo = "Preemptive Priority"
        #title 
        st.subheader(algo)
        avs.add_vertical_space(2)
        q, processes_objs = read_file()
        # test the preemptive scheduling
        preemptive = PreemptivePriority(processes_objs)
        preemptive.simulate_pp(page)
        preemptive.calculate_average()

        #row number 1: start time-->finish time
        avs.add_vertical_space(1)
        st.markdown('---')
        st.subheader("FINAL GRANT CHART:")
        st.markdown(f":green[CONTEXT SWITCH COUNT: {len(preemptive.grant_chart)-1}]")
        time_list = [f'{preemptive.gc_st[i]} -> {preemptive.gc_ft[i]}ms' for i,v in enumerate(preemptive.gc_ft)] 
        p_list =  [i for i in preemptive.grant_chart] 
        data_PP = [
                tuple(p_list),
            ]
        df1_PP = pd.DataFrame(data_PP, ['Process'],  columns=time_list)
        st.table(df1_PP)
    
        avg_data_PP = [
                      (" Response Time (ms)", preemptive.avg_rt),
                      (" Waiting Time (ms)", preemptive.avg_wt),
                      (" TurnAround Time (ms)", preemptive.avg_tat)
                  ]
      
        df2_PP = pd.DataFrame(avg_data_PP, [' ','  ', '   '], columns=["Average", "Value"])
      
        st.table(df2_PP)

    with tab_b:
        algo = "Round Robin"
        #title 
        st.subheader(algo)
        avs.add_vertical_space(2)
        q, processes_objs = read_file()
        rr = RoundRobin(processes_objs, q)
        Avg_WT, Avg_TAT, Avg_RT = rr.roundrobin(page_no="1")

        avs.add_vertical_space(1)
        st.markdown('---')
        st.subheader("FINAL GRANT CHART:")
        st.markdown(f":green[CONTEXT SWITCH COUNT: {len(rr.grant_chart)-1}]")
        time_list = [f'{rr.gc_st[i]} -> {rr.gc_ft[i]}ms' for i,v in enumerate(rr.grant_chart)] 
        p_list =  [i for i in rr.grant_chart] 
        
        data_PP = [
                tuple(p_list),
            ]
        df1_PP = pd.DataFrame(data_PP, ['Process'],  columns=time_list)
        st.table(df1_PP)

        avg_data_RR = [
                      (" Response Time (ms)", Avg_RT),
                      (" Waiting Time (ms)", Avg_WT),
                      (" TurnAround Time (ms)", Avg_TAT)
                  ]
      
        df2_RR = pd.DataFrame(avg_data_RR, [' ','  ', '   '], columns=["Average", "Value"])
        avs.add_vertical_space(2)
        st.table(df2_RR)

    with tab_c:
        algo = "Shortest Remaining Time First "
        #title 
        st.subheader(algo)
        srtf = SRTF("input.txt")
        avg_waiting_time, avg_turnaround_time, avg_response_time = srtf.schedule(page_no="1")
        avg_data_srtf = [
                      (" Response Time (ms)", avg_response_time),
                      (" Waiting Time (ms)", avg_waiting_time),
                      (" TurnAround Time (ms)", avg_turnaround_time)
                  ]
      
        df2_srtf = pd.DataFrame(avg_data_srtf, [' ','  ', '   '], columns=["Average", "Value"])
        avs.add_vertical_space(2)
        st.table(df2_srtf)

    with tab_d:
        algo = "Multi-level Feedback Queue Custom"
        #title 
        st.subheader(algo)
        
        q, processes_objs = read_file()
        st.markdown("This scheduler offers the following algorithms (preemptive): ")
        st.code("> Preemptive Priority (highest priority queue: Q1)", language='python')
        st.code(f"> Round Robin w/ q=4 (medium priority queue: Q2)",  language='python')
        st.code("> First Come First Served (lowest priority queue: Q3)",  language='python')
        avs.add_vertical_space(2)
         # test the preemptive scheduling
        custom = Custom(processes_objs, q)
        custom.determine_queue(page)
        custom.calculate_average()

        #row number 1: start time-->finish time
        avs.add_vertical_space(2)
        st.markdown('---')
        st.subheader("FINAL GRANT CHART:")
        st.markdown(f":green[CONTEXT SWITCH COUNT: {len(custom.grant_chart)-1}]")

        #fix the grand_chgart format for printing
        time_list = [f'{custom.gc_st[i]} -> {custom.gc_ft[i]}ms' for i,v in enumerate(custom.gc_ft)]  #row number 3
        Q_list = [v[0:2]+f' '*i for i,v in enumerate(custom.grant_chart)] #row number 1
        p_list =  [i[4:len(i)] for i in custom.grant_chart] # row number 2
        data_MLFQC = [
                (t for t in time_list),
                (p for p in p_list)
            ]
        df1_MLFQC = pd.DataFrame(data_MLFQC, ['Time', 'Process'], columns=Q_list)
        st.table(df1_MLFQC)
                
        avg_data_MLFQC = [
                      (" Response Time (ms)", custom.avg_rt),
                      (" Waiting Time (ms)", custom.avg_wt),
                      (" TurnAround Time (ms)", custom.avg_tat)
                  ]

        df2_MLFQC = pd.DataFrame(avg_data_MLFQC,  [' ','  ', '   '], columns=["Average", "Value"])
        st.table(df2_MLFQC)

def simulate_srtf():
    srtf = SRTF("input.txt", '2')
    avg_waiting_time, avg_turnaround_time, avg_response_time = srtf.schedule(page_no="2")
    wt = srtf.WT
    rt = srtf.RT
    tat = srtf.TAT

    return rt, wt, tat, [avg_response_time, avg_waiting_time, avg_turnaround_time]


def simulate_rr():
    q, processes_objs = read_file()
    rr = RoundRobin(processes_objs, q)
    Avg_WT, Avg_TAT, Avg_RT = rr.roundrobin(page_no="2")
    rr_rt = [i.rt if i.rt !=-1 else 0 for i in rr.processes ]
    rr_wt =  [i.wt for i in rr.processes]
    rr_tat =  [i.tat for i in rr.processes]

    return rr_rt, rr_wt, rr_tat, [Avg_RT, Avg_WT, Avg_TAT]

def simulate_pp():
    # read the input file:
    q, p_objects  = read_file()

    #1. PP algo
    pp = PreemptivePriority(p_objects)
    pp.simulate_pp(page)
    pp.calculate_average()

    #store pp response times for all processes 
    pp_rt = [i.rt for i in pp.processes]
    #store pp waiting times for all processes 
    pp_wt = [i.wt for i in pp.processes]
    #store pp TAT times for all processes 
    pp_tat = [i.tat for i in pp.processes]

    return pp_rt, pp_wt, pp_tat, [pp.avg_rt, pp.avg_wt, pp.avg_tat]

def simulate_mlfq():
    # read the input file:
    q, p_objects  = read_file()

    #2. MLFQ algo
    custom = Custom(p_objects, q)
    custom.determine_queue(page)
    custom.calculate_average()
    
    #store custom response times for all processes 
    custom_rt = [i.rt for i in custom.processes]
    #store custom waiting times for all processes 
    custom_wt = [i.wt for i in custom.processes]
    #store custom TAT times for all processes 
    custom_tat = [i.tat for i in custom.processes]

    return custom_rt, custom_wt, custom_tat, [custom.avg_rt, custom.avg_wt, custom.avg_tat]


def leaderboard(average_time, rr, srtf, pp,mlfq ,index):
    c1,c2,c3,c4 = st.columns(4)
    selected = []
    with c1:
            if average_time[0] == mlfq[index]:
                st.markdown(f"🥇: MLFQ = {average_time[0]}ms")
                selected.append('MLFQ')
            elif average_time[0] == pp[index]:
                st.markdown(f"🥇: PP = {average_time[0]}ms")
                selected.append('PP')
            elif average_time[0] == rr[index]:
                st.markdown(f"🥇: RR = {average_time[0]}ms")
                selected.append('RR')
            elif average_time[0] == srtf[index]:
                st.markdown(f"🥇: SRTF = {average_time[0]}ms")
                selected.append('SRTF')

    with c2:
            if average_time[1] == mlfq[index] and 'MLFQ' not in selected:
                st.markdown(f"🥈: MLFQ = {average_time[1]}ms")
                selected.append('MLFQ')
            elif average_time[1] == pp[index] and 'PP' not in selected :
                st.markdown(f"🥈: PP = {average_time[1]}ms")
                selected.append('PP')
            elif average_time[1] == rr[index] and 'RR' not in selected :
                st.markdown(f"🥈: RR = {average_time[1]}ms")
                selected.append('RR')
            elif average_time[1] == srtf[index] and 'SRTF' not in selected :
                st.markdown(f"🥈: SRTF = {average_time[1]}ms")
                selected.append('SRTF')

    with c3:
            if average_time[2] == mlfq[index] and 'MLFQ' not in selected :
                st.markdown(f"🥉: MLFQ = {average_time[2]}ms")
            elif average_time[2] == pp[index] and 'PP' not in selected:
                st.markdown(f"🥉: PP = {average_time[2]}ms")
            elif average_time[2] == rr[index] and 'RR' not in selected: 
                st.markdown(f"🥉: RR = {average_time[2]}ms")
            elif average_time[2] == srtf[index] and 'SRTF' not in selected:
                st.markdown(f"🥉: SRTF = {average_time[2]}ms")

    st.markdown("---")


def plot(dataframe_time, rows):
    chart_data = pd.DataFrame(
    dataframe_time,
        columns = ['Process PID (starting from 1)', 'PP', 'MLFQ', 'RR', 'SRTF'])

    st.line_chart(
            chart_data,
            x = 'Process PID (starting from 1)',
            y = ['PP', 'MLFQ', 'RR', 'SRTF'],
            color=['#8bd8bd', '#3b8a0b', '#a3193b', '#ffa500']
        )

    df = pd.DataFrame(dataframe_time,rows, columns=["PID", "PP", "MLFQ", 'RR', 'SRTF'])
    st.table(df)


def streamlit_app2():
    b, page = get_session_state()
    tab_rt, tab_wt, tab_tat = st.tabs(["Response Time", "Waiting Time", "Turn Around Time"])

    dataframe_pp_rt, dataframe_pp_wt, dataframe_pp_tat,pp_avg= simulate_pp()
    sleep(1)
    dataframe_mlfq_rt, dataframe_mlfq_wt, dataframe_mlfq_tat, custom_avg = simulate_mlfq()
    sleep(1)
    dataframe_rr_rt, dataframe_rr_wt, dataframe_rr_tat, rr_avg = simulate_rr()
    sleep(1)
    dataframe_srtf_rt, dataframe_srtf_wt, dataframe_srtf_tat, srtf_avg = simulate_srtf()


    # return a dataframe sutiable list
    dataframe_rt = []
    for i in range(len(dataframe_mlfq_rt)):
        dataframe_rt.append([ i+1, dataframe_pp_rt[i], dataframe_mlfq_rt[i], dataframe_rr_rt[i],dataframe_srtf_rt[i] ])

    dataframe_wt = []
    for i in range(len(dataframe_mlfq_rt)):
        dataframe_wt.append([i+1, dataframe_pp_wt[i], dataframe_mlfq_wt[i], dataframe_rr_wt[i], dataframe_srtf_wt[i]])

    dataframe_tat = []
    for i in range(len(dataframe_mlfq_rt)):
        dataframe_tat.append([i+1,dataframe_pp_tat[i], dataframe_mlfq_tat[i], dataframe_rr_tat[i], dataframe_srtf_tat[i]])

    rows = [' '*i for i in range(len(dataframe_mlfq_rt))]
    with tab_rt:
        st.title("Graphs Page: Response Time")
        avs.add_vertical_space(2)

        # 1. display the average time winners:
        average_rt = [custom_avg[0], pp_avg[0], rr_avg[0], srtf_avg[0]]
        average_rt.sort()

        st.markdown("**:green[LEADERBOARD]**")
        leaderboard(average_rt,pp=pp_avg, rr=rr_avg, mlfq=custom_avg, srtf=srtf_avg , index=0)

        
        # 2. plot the response times for all the processes:
        st.subheader(":green[Response time for all the processes in all the algorithms]")
        c1,c2,c3,c4 = st.columns(4)
        with c3:
            st.caption("X-axis is PID")
        with c2:
            st.caption("Y-axis is REPONSE TIME")
        
        plot(dataframe_rt, rows)

        avs.add_vertical_space(2)
        st.subheader("The Average Response Times")
        st.markdown(f"PP algorithm: {pp_avg[0]}ms")
        st.markdown(f"RR algorithm: {rr_avg[0]}ms")
        st.markdown(f"SRTF algorithm: {srtf_avg[0]}ms")
        st.markdown(f"MLFQ algorithm: {custom_avg[0]}ms")
        

    with tab_wt:
        st.title("Graphs Page: Waiting Time")
        avs.add_vertical_space(2)

        average_wt = [custom_avg[1], pp_avg[1], rr_avg[1], srtf_avg[1]]
        average_wt.sort()

        st.markdown("**:green[LEADERBOARD]**")
        leaderboard(average_wt,pp=pp_avg, rr=rr_avg, mlfq=custom_avg, srtf=srtf_avg, index=1 )

        # 2. plot the response times for all the processes:
        st.subheader(":green[Waiting time for all the processes in all the algorithms]")
        c1,c2,c3,c4 = st.columns(4)
        with c3:
            st.caption("X-axis is PID")
        with c2:
            st.caption("Y-axis is WAITING TIME")
        
        plot(dataframe_wt, rows)

        avs.add_vertical_space(2)
        st.subheader("The Average Waiting Times")
        st.markdown(f"PP algorithm: {pp_avg[1]}ms")
        st.markdown(f"RR algorithm: {rr_avg[1]}ms")
        st.markdown(f"SRTF algorithm: {srtf_avg[1]}ms")
        st.markdown(f"MLFQ algorithm: {custom_avg[1]}ms")

    with tab_tat:
        st.title("Graphs Page: Turn Around Time")
        avs.add_vertical_space(2)

        # 1. display the average time winners:
        average_tat = [custom_avg[2], pp_avg[2], rr_avg[2], srtf_avg[2]]
        average_tat.sort()

        st.markdown("**:green[LEADERBOARD]**")
        leaderboard(average_tat,pp=pp_avg, rr=rr_avg, mlfq=custom_avg, srtf=srtf_avg, index=2 )

        # 2. plot the response times for all the processes:
        st.subheader(":green[TAT time for all the processes in all the algorithms]")
        c1,c2,c3,c4 = st.columns(4)
        with c3:
            st.caption("X-axis is PID")
        with c2:
            st.caption("Y-axis is TAT TIME")
        
        plot(dataframe_tat, rows)

        avs.add_vertical_space(2)
        st.subheader("The Average TurnAround Times")
        st.markdown(f"PP algorithm: {pp_avg[2]}ms")
        st.markdown(f"RR algorithm: {rr_avg[2]}ms")
        st.markdown(f"SRTF algorithm: {srtf_avg[2]}ms")
        st.markdown(f"MLFQ algorithm: {custom_avg[2]}ms")
        
        
st.set_page_config(page_title="CPU Scheduling", page_icon="⏰", layout="centered")
st.image("header.png")
    
b, page = get_session_state()

if b is False:
    st.balloons()
    set_session_state(True, '1')

with st.sidebar:
    st.header("Go to:")
    if st.button("Main Page", use_container_width=True):
        set_session_state(True, '1')

    if st.button("Graphs Page", use_container_width=True):
        set_session_state(True, '2')

b, page = get_session_state()

if page == '2':
    streamlit_app2() #graphs
elif page == '1':
    streamlit_app1()
