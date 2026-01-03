import tkinter as tk
from tkinter import filedialog as fd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set()

#BROWSE BUTTON

def browse_button():
     
    filetypes = (('CSV (comma delimited)', '*.csv'),('All files', '*.*'))

    file_path = fd.askopenfilename(filetypes=filetypes)
    
    entryA.delete(0,len(entryA.get()))
    entryA.insert(0,file_path)
    

def clear_button(text):
    
    entryA.delete(0,len(entryA.get()))
    entryA.insert(0,text)
    
#DERIVATIVE CALC

def der_data_gen(x_data,y_data):

    dx = []
    for i in range(len(x_data)):
      dx.extend([x_data[i]]*2)
    
    dx.pop(0)
    dx.pop(-1)
    
    dy = []
    for i in range(1,len(y_data)):
      dy += [(y_data[i]-y_data[i-1])/(x_data[i]-x_data[i-1])]*2
    
    der_data = np.array([dx,dy]).T
    
    return der_data

#PLOT CREATION

def Plot_Data(file):
    
    ### Create the Data
    raw_data = pd.read_csv(file)
    
    df = raw_data.copy()
    df = df.iloc[:,0:2]
    
    x_data = np.array(df[df.columns[0]],dtype=np.dtype('float'))
    y_data = np.array(df[df.columns[1]],dtype=np.dtype('float'))
    d_data = der_data_gen(x_data,y_data)
    
    ### Smooth out the data
    
    step = 8
    
    d_dataframe = pd.DataFrame(d_data,columns=['x_data','y_data'])
    d_dataframe['Average'] = d_dataframe.y_data.rolling(step).mean()
    d_dataframe.Average = d_dataframe.Average.shift(-int(step/2))
    
    print(d_dataframe.head(20))
    
    
    ### Plot the Data
    dx = d_data[:,0]
    dy = d_data[:,1]
    
    fig, (ax1,ax2) = plt.subplots(2,1,sharex=True,figsize = (10,10))
    fig.subplots_adjust(hspace=0.1)
    
    fig.suptitle(entry1.get(),size=15)
    ax1.plot(x_data,y_data)
    ax2.plot(dx,dy)
    ax2.plot(dx,d_dataframe['Average'])
    
    ax1.set_ylabel(entry2.get())
    
    ax2.set_ylabel(entry3.get())
    ax2.set_xlabel(entry4.get())
    
    ax2.legend([f'{entry3.get()}, Raw',f'{entry3.get()}, Moving Avg'])
    
    plt.show()
    

#INTERFACE CREATION

root = tk.Tk()
root.title('Derivative Plotter')
root.geometry('500x300')
root.resizable(False,False)


#Load the Data Set
button1 = tk.Button(root, text = 'Select Data',command = browse_button)
entryA=tk.Entry(root,width = 50)
entryA.insert(0,"File Path")

#Create a Plot Button 
button2 = tk.Button(root, text = 'Plot Data',command = lambda: Plot_Data(entryA.get()))
button3 = tk.Button(root,text = "Clear Data", command = lambda: clear_button("File Path"))

#Gather Labels for te Graphs
Label1 = tk.Label(root, text="Graph Name: ")
entry1 = tk.Entry(root,width = 50)
Label2 = tk.Label(root, text="Parent Function Name: ")
entry2 = tk.Entry(root,width = 50)
Label3 = tk.Label(root, text="Derivative Function Name: ")
entry3 = tk.Entry(root,width = 50)
Label4 = tk.Label(root, text="With respect to: ")
entry4 = tk.Entry(root,width = 50)
Blank = tk.Label(root)

button1.grid(row=0, column=0,padx=10,pady=5)
entryA.grid(row=0,column = 1,padx=5)
button3.grid(row=1,column=0)

Blank.grid(row=2,column=0,pady=5)

Label1.grid(row=3,column=0)
entry1.grid(row=3,column=1)
Label2.grid(row=4,column=0)
entry2.grid(row=4,column=1)
Label3.grid(row=5,column=0)
entry3.grid(row=5,column=1)
Label4.grid(row=6,column=0)
entry4.grid(row=6,column=1)

button2.grid(row=7,column=0,pady = 15)

root.mainloop()

#testing for git purposes