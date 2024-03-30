from scheduling.process import Process
from scheduling.custom import Custom
from scheduling.preePriority import PreemptivePriority
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import pandas as pd


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
    '''
    preemptive = PreemptivePriority(p_objects)
    preemptive.simulate_pp()
    preemptive.calculate_average()

    #print the averages:
    print(preemptive.grant_chart)
    print(f"""
    --------------------------------------------------------
    |average response time    | {preemptive.avg_rt} ms      
    |average waiting time     | {preemptive.avg_wt} ms     
    |averate turn around time | {preemptive.avg_tat} ms    
    ---------------------------------------------------------\n
    """)
    '''
    

    # test custom algorithm scheduling
    custom = Custom(p_objects, q)
    custom.determine_queue()
    custom.calculate_average()
    print(custom.grant_chart)

    #print the averages:
    print(f"""
    --------------------------------------------------------
    |average response time    | {custom.avg_rt} ms      
    |average waiting time     | {custom.avg_wt} ms     
    |averate turn around time | {custom.avg_tat} ms    
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


    algo = "Please select an algorithm from the sidebar menu."

    tab_a, tab_b, tab_c, tab_d = st.tabs(["PP","RR", "SRTF", "MLFD Custom"])
    with tab_a:
        algo = "Preemptive Priority"
        #title 
        st.subheader(algo)
        if True:
              if st.button(f"Simulate PP Scheduling", use_container_width=True):
                  q, processes_objs = read_file()
                  # test the preemptive scheduling
                  preemptive = PreemptivePriority(processes_objs)
                  preemptive.simulate_pp()
                  preemptive.calculate_average()

                  columns_list = [' '+f' '*i for i,v in enumerate(preemptive.grant_chart)] #row number 1
                  chart = tuple(preemptive.grant_chart),
                  df1_PP = pd.DataFrame(chart,  columns=columns_list)
                  st.table(df1_PP)
      
                  avg_data_PP = [
                      (" Response Time (ms)", preemptive.avg_rt),
                      (" Waiting Time (ms)", preemptive.avg_wt),
                      (" TurnAround Time (ms)", preemptive.avg_tat)
                  ]
      
                  df2_PP = pd.DataFrame(avg_data_PP, columns=["Average", "Value"])
      
                  st.table(df2_PP)

    with tab_b:
        algo = "Round Robin"
        #title 
        st.subheader(algo)

    with tab_c:
        algo = "Shortest Remaining Time First "
        #title 
        st.subheader(algo)

    with tab_d:
        algo = "Multi-level Feedback Queue Custom"
        #title 
        st.subheader(algo)
        if True:
            if st.button(f"Simulate MLFQC Scheduling", use_container_width=True):
                q, processes_objs = read_file()
                st.markdown("This scheduler offers the following algorithms (preemptive): ")
                st.code("> Preemptive Priority (highest priority queue: Q1)", language='python')
                st.code(f"> Round Robin w/ q={q} (medium priority queue: Q2)",  language='python')
                st.code("> First Come First Served (lowest priority queue: Q3)",  language='python')
                avs.add_vertical_space(2)
                # test the preemptive scheduling
                custom = Custom(processes_objs, q)
                custom.determine_queue()
                custom.calculate_average()

                #fix the grand_chgart format for printing
                Q_list = [v[0:2]+f' '*i for i,v in enumerate(custom.grant_chart)] #row number 1
                p_list =  [i[4:len(i)] for i in custom.grant_chart] # row number 2
                p_tuple = [tuple(p_list)]
                df1_MLFQC = pd.DataFrame(p_tuple, columns=Q_list)
                st.table(df1_MLFQC)
                
                avg_data_MLFQC = [
                      (" Response Time (ms)", custom.avg_rt),
                      (" Waiting Time (ms)", custom.avg_wt),
                      (" TurnAround Time (ms)", custom.avg_tat)
                  ]


                df2_MLFQC = pd.DataFrame(avg_data_MLFQC, columns=["Average", "Value"])
      
                st.table(df2_MLFQC)

    
def streamlit_app2():
    st.title("Graphs Page")
    st.markdown('---')
    avs.add_vertical_space(2)
    st.markdown("yet to be done...")

#main()
st.set_page_config(page_title="CPU Scheduling", page_icon="⏰", layout="centered")
st.image("header.png")
    
b, page = get_session_state()

if b is False:
    st.balloons()
    set_session_state(True)

with st.sidebar:
    st.header("Go to:")
    if st.button("Main Page", use_container_width=True):
        set_session_state(True, '1')

    if st.button("Graphs Page", use_container_width=True):
        set_session_state(True, '2')

b, page = get_session_state()

if page=='1':
    streamlit_app1() #grant chart
elif page=='2':
    streamlit_app2() #graphs
