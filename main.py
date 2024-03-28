from scheduling.process import Process
from scheduling.preePriority import PreemptivePriority
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
def main():
   
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

    # test the preemptive scheduling
    preemptive = PreemptivePriority(p_objects)
    preemptive.simulate_CPU()
    preemptive.calculate_average()

    #print the averages:
    print(f"""
--------------------------------------------------------
|average response time    | {preemptive.avg_rt} ms      
|average waiting time     | {preemptive.avg_wt} ms     
|averate turn around time | {preemptive.avg_tat} ms    
---------------------------------------------------------\n
""")
    
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

    return p_objects

def streamlit_app():
    st.set_page_config(page_title="CPU Scheduling", page_icon="⏰", layout="centered")
    st.image("header.png")
    
    #input file
    user_input = st.file_uploader("please input your input txt file here", type='txt')
    st.markdown("The file should follow the following structor:")
    st.code("3\n1 0 3 3\n2 1 6 2\n3 3 2 2\n4 8 2 1", language='python')
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
        st.code("3\n1 0 3 3\n2 1 6 2\n3 3 2 2\n4 8 2 1", language='python')

        avs.add_vertical_space(1)


    algo = "Please select an algorithm from the sidebar menu."
    selected = ''

    tab_a, tab_b, tab_c, tab_d = st.tabs(["PP","RR", "SRTF", "MLFD Custom"])
    with tab_a:
        algo = "Preemptive Priority Simulator"
        #title 
        st.subheader(algo)
        selected = "a"

        if st.button("Simulate Proccess Scheduling", use_container_width=True):
            processes_objs = read_file()
            # test the preemptive scheduling
            preemptive = PreemptivePriority(processes_objs)
            preemptive.simulate_CPU()
            preemptive.calculate_average()

            df1 = pd.DataFrame(preemptive.grant_chart)
            st.table(df1.T)

            avg_data = [
                (" Response Time (ms)", preemptive.avg_rt),
                (" Waiting Time (ms)", preemptive.avg_wt),
                (" TurnAround Time (ms)", preemptive.avg_tat)
            ]

            df2 = pd.DataFrame(avg_data, columns=["Average", "Value"])

            st.table(df2)

    with tab_b:
        algo = "Round Robin"
        #title 
        st.subheader(algo)
        selected = "b"

    with tab_c:
        algo = "Shortest Remaining Time First "
        #title 
        st.subheader(algo)
        selected = "c"

    with tab_d:
        algo = "Multi-level Feedback Queue Custom"
        #title 
        st.subheader(algo)
        selected = "d"

    


#main()

streamlit_app()