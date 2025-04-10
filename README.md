# CPU SCHEDULING ALGORITHMS SIMULATOR
*Assumung you have VS code and Python installed on your deviece already*
## Description
CPU scheduling is about choosing which process gets to use the CPU for running its tasks, while other processes wait. It’s important because it helps use resources efficiently and improves how well the system works. The main aim of CPU scheduling is to keep the CPU busy and to reduce system overhead. The operating system ensures there’s always a process ready to go, so the CPU always has something to do.

For more details check the report PDF.

## To run the website interface on your local machine do the following steps:

1. Download the following libraries in your VS code terminal,
   run the following commands:
   
   *for mac use pip3 instead of pip*
   
   `pip install streamlit`
   
   `pip install streamlit-extras`
   
   `pip install pandas`

   `pip install matplotlib`
      

3. Check the installation for the libraries
   
   run the following command for all the libraries you just installed:
   
   `library_name --version`
   
   **If you got an error it means the library was not installed correctly**
   
   *a video that might help you install streamlit if this problem occured:*
   
   --> https://youtu.be/Uloc4Z0SUks?si=KZmxrbT8ycPoyK7q

5. Download the zip file for this repositary from Github
6. Un-Zip the folder on your machine using the default un-zipper or download zip7 program if you do not have one
7. Drag and drop your folder into VS code enviroment
8. Make sure to select the Python interpetor that you previously downloaded the libraries on
9. using the VS code terminal run the following command:
    
   `streamlit run main.py`

CONGRATS NOW THE WEBSITE SHOULD APPEAR ON YOUR LOCACL HOST WEB PAGE.

NOTE: the default input txt file that is used in main.py & pyplot.py is named: input.txt
if you want to change the default input, modify that file.

## To display the plots only without a website interface (plot the diffrences between the algorithms)

run the following command:

WINDOWS: `python pyplot.py`

MAC: `python3 pyplot.py`
   
