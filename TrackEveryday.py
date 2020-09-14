import tkinter as tk
from tkinter import font as tkFont
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime
from datetime import timedelta
from sys import exit
import time
from os import listdir
from os.path import isfile, join

class Application(tk.Frame):
  def __init__(self, master,tasks_list,task_vars,task_intervals,notification_interval,pauseInterval_ui_input,pause_pressed,show_logs_pressed):
    super().__init__(master)
    self.master = master
    self.task_vars=task_vars
    self.task_intervals=task_intervals
    self.tasks_list=tasks_list
    self.notification_interval=notification_interval
    self.pauseInterval_ui_input=pauseInterval_ui_input
    self.pause_pressed=pause_pressed
    self.show_logs_pressed=show_logs_pressed
    self.pack()
    self.create_widgets()

  def create_widgets(self):
    helv14 = tkFont.Font(family='Helvetica', size=14) #weight='bold'
    helv12bold = tkFont.Font(family='Helvetica', size=10, weight='bold')
    for count, task in enumerate(self.tasks_list):
      task=tk.Checkbutton(self, text=task, onvalue = 1, offvalue = 0, variable=self.task_vars[count], font=helv14).grid(row=count, column=0, sticky='W')
      task=tk.Entry(self, textvariable=self.task_intervals[count], width=2, font=helv14).grid(row=count, column=2, sticky='W')

    done = tk.Button(self, text="Done", bd=6, width=20, fg="red", font=helv12bold, command=self.log_time)
    done.grid(row=len(tasks_list), columnspan=3)
    show_logs = tk.Button(self, text="ShowLogs", bd=6, fg="red",font=helv12bold, command=self.show_logs)
    show_logs.grid(row=len(tasks_list)+1, column=0, sticky='W')
    pause_intvl=tk.Entry(self, textvariable=self.pauseInterval_ui_input, width=3, font=helv14)
    pause_intvl.grid(row=len(tasks_list)+1, column=1, sticky='W')
    pause_notif = tk.Button(self, text="Pause", bd=6, fg="red",font=helv12bold, command=self.pause_notif)
    pause_notif.grid(row=len(tasks_list)+1, column=2, sticky='W')

  def log_time(self):
    currentMonth = datetime.now().strftime('%m')
    currentYear = datetime.now().strftime('%Y')
    log_file_name=currentYear+"_"+currentMonth+"_TimeLog.tsv"
    output_log_file=os.path.join(os.getcwd(),'Logs',log_file_name)
    if not os.path.exists(os.path.join(os.getcwd(),'Logs')):
      os.makedirs(os.path.join(os.getcwd(),'Logs'))
    if(not os.path.exists(output_log_file)):
      outputlog_df=pd.DataFrame(columns=["Date","Task","TotalTime","TimeIntervalLogs"])
      outputlog_df.to_csv(os.path.join(os.getcwd(),'Logs',log_file_name),index=False,sep='\t')
    outputlog_df=pd.read_csv(os.path.join(os.getcwd(),'Logs',log_file_name),sep='\t',comment='#')

    for count, task in enumerate(self.tasks_list):
      if self.task_vars[count].get()==1:
        #print(outputlog_df.loc[(outputlog_df["Date"]==str(datetime.now().date())) & (outputlog_df["Task"]==task),"TimeIntervalLogs"].index.values)
        int_counter=1
        if self.task_intervals[count].get():
          int_counter=int(self.task_intervals[count].get())
        if task in outputlog_df.loc[outputlog_df["Date"]==str(datetime.now().date()),"Task"].values:
          time_log_index=outputlog_df.loc[(outputlog_df["Date"]==str(datetime.now().date())) & (outputlog_df["Task"]==task),"TimeIntervalLogs"].index.values
          time_log=outputlog_df.loc[time_log_index[0],"TimeIntervalLogs"].strip('][')
          outputlog_df.at[time_log_index[0],"TimeIntervalLogs"]="["+time_log+", ("+str((datetime.now()-timedelta(minutes=int(self.notification_interval)*int_counter)).strftime("%H:%M"))+","+str(datetime.now().strftime("%H:%M"))+")]"
          log_times_list=outputlog_df.loc[time_log_index[0],"TimeIntervalLogs"].strip('][').split(', ')
          total_time_mins=0
          for time_snippet in log_times_list:
            time_snippet=time_snippet.strip(')(').split(',')
            time_mins=(datetime.strptime(time_snippet[1], '%H:%M')-datetime.strptime(time_snippet[0], '%H:%M')).total_seconds()/60
            time_mins=time_mins+1440 if time_mins<0 else time_mins
            total_time_mins=total_time_mins+time_mins
            outputlog_df.at[time_log_index[0],"TotalTime"]=total_time_mins           
        else:
          temp=pd.DataFrame({"Date":[datetime.now().date()],"Task":task,"TotalTime":[int(self.notification_interval)*int_counter],"TimeIntervalLogs":"[("+str((datetime.now()-timedelta(minutes=int(self.notification_interval)*int_counter)).strftime("%H:%M"))+","+str(datetime.now().strftime("%H:%M"))+")]"})
          outputlog_df=outputlog_df.append(temp)        
    if not os.path.exists(os.path.join(os.getcwd(),'Logs')):
      os.makedirs(os.path.join(os.getcwd(),'Logs'))
    outputlog_df.to_csv(os.path.join(os.getcwd(),'Logs',log_file_name),index=False,sep='\t')
    self.master.destroy()
  
  def show_logs(self):
    print("In show_logs")
    self.show_logs_pressed.set(1)
    self.log_time() 

  def pause_notif(self):
    print("In pause_notif") 
    self.pause_pressed.set(1)
    self.log_time() 

class ShowLogApp(tk.Frame):
  def __init__(self, master):
    super().__init__(master)
    self.master = master
    self.pack()
    self.create_widgets()

  def create_widgets(self):
    log_file_df=pd.DataFrame(columns=["Task","Time"])
    currentMonth = datetime.now().strftime('%m')
    currentYear = datetime.now().strftime('%Y')
    log_file_name=currentYear+"_"+currentMonth+"_TimeLog.tsv"
    if not os.path.exists(os.path.join(os.getcwd(),'Logs')):
      os.makedirs(os.path.join(os.getcwd(),'Logs'))
    time_log_files = [f for f in listdir(os.path.join(os.getcwd(),'Logs')) if isfile(os.path.join(os.getcwd(),'Logs',f)) and '_TimeLog.tsv' in f]
    time_log_files.sort(reverse=True)
    helv12 = tkFont.Font(family='Helvetica', size=12) #weight='bold'
    helv16 = tkFont.Font(family='Helvetica', size=16, weight='bold') #weight='bold'

    row_count=0
    for time_log_file in time_log_files:
      month_list=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      log_year=time_log_file.split('.')[0][0:4]
      log_month=month_list[int(time_log_file.split('.')[0][5:7])-1]
      tk.Label(self,text=log_year+" "+log_month, font=helv16, bd=5, relief='solid' ).grid(row=row_count, columnspan=2, sticky='W')
      row_count=row_count+1
      temp=pd.DataFrame({"Task":[log_year+" "+log_month],"Time":[""]})
      log_file_df=log_file_df.append(temp)    
      outputlog_df=pd.read_csv(os.path.join(os.getcwd(),'Logs',time_log_file),sep='\t',comment='#')
      all_tasks=list(set(outputlog_df.loc[:,"Task"].values))
      for task in all_tasks:
        total_mins=sum(outputlog_df.loc[outputlog_df["Task"]==task,"TotalTime"].values)
        tk.Label(self,text=task, font=helv12, relief='ridge', width=20, justify='left').grid(row=row_count, column=0, sticky='W')
        tk.Label(self,text=str(total_mins)+" mins ("+str(round(total_mins/60,2))+" hours)", font=helv12, relief='ridge', width=20, justify='left').grid(row=row_count, column=1, sticky='W')
        row_count=row_count+1
        temp=pd.DataFrame({"Task":[task],"Time":[total_mins]})
        log_file_df=log_file_df.append(temp) 
    if not os.path.exists(os.path.join(os.getcwd(),'Logs')):
      os.makedirs(os.path.join(os.getcwd(),'Logs'))    
    log_file_df.to_csv(os.path.join(os.getcwd(),'Logs','SavedLog_'+datetime.now().strftime("%Y_%m_%d_%H_%M")+".tsv"),index=False,header=False,sep='\t')
  
def measure_str_width(str): 
  upper, other, str_width = 0, 0, 0
  for i in range(len(str)): 
    if str[i].isupper(): 
      upper += 13 #upper case characters are 13 px in width on average
    else: 
      other += 9.3 ##other characters are 9.3 px in width on average 
  str_width=round(upper+other) 
  return str_width      

if __name__ == "__main__":
  while 1:
    if os.path.exists(os.path.join(os.getcwd(),"settings.txt")):
      settings_df=pd.read_csv(os.path.join(os.getcwd(),"settings.txt"),sep=':',comment='#',header=None,index_col=0)
      notification_interval=int(settings_df.loc["NotificationInterval",1])
      pauseInterval=int(settings_df.loc["PauseInterval",1])
      tasks_list=settings_df.loc["Tasks",1].strip('][').split(',')
      tasks_list=[x.strip() for x in tasks_list]
    else:
      notification_interval=15
      pauseInterval=45
      tasks_list=["Task 1", "Task 2", "Task 3"]
    root = tk.Tk()
    task_vars=[]
    task_intervals=[]
    pause_pressed=tk.IntVar()
    pause_pressed.set(0)
    pauseInterval_ui_input=tk.IntVar()
    pauseInterval_ui_input.set(pauseInterval)
    show_logs_pressed=tk.IntVar()
    show_logs_pressed.set(0)
    max_task_width=0
    for task in tasks_list:
      curr_task_width=measure_str_width(task)
      max_task_width = curr_task_width if curr_task_width > max_task_width else max_task_width
      task_vars.append(tk.IntVar())
      task_intervals.append(tk.StringVar())
    notif_window = Application(root,tasks_list,task_vars,task_intervals,notification_interval,pauseInterval_ui_input,pause_pressed,show_logs_pressed)
    notif_window.master.title('Test')
    ws = notif_window.master.winfo_screenwidth() # width of the screen 
    hs = notif_window.master.winfo_screenheight() # height of the screen
    print("Windows screendim= "+ str(ws)+ " "+str(hs))
    notif_window_height=70+len(tasks_list)*34
    notif_window_vert_position=688-len(tasks_list)*34
    print(max_task_width)
    notif_window_width=126+max_task_width #160 15 upper chars == 21*15  210 for 10 char  12.7 for uppercase characters
    notif_window_hor_position=1140-max_task_width #1080 1266-124
    
    #notif_window.master.geometry('160x'+str(notif_window_height)+'+1080+'+str(notif_window_vert_position)) #172,138
    notif_window.master.geometry(str(notif_window_width)+'x'+str(notif_window_height)+'+'+str(notif_window_hor_position)+'+5') #172,138
    notif_window.master.overrideredirect(True)
    notif_window.master.attributes('-topmost', True)
    notif_window.master.configure(background='black')    
    notif_window.mainloop()
    notif_window_exit_time=datetime.now()
    print("PauseState is : "+str(pause_pressed.get()))
    sleep_duration_mins=notification_interval
    if pause_pressed.get()==1:
      sleep_duration_mins=pauseInterval
      if pauseInterval_ui_input.get():
        sleep_duration_mins=int(pauseInterval_ui_input.get())
    if show_logs_pressed.get()==1:
      root = tk.Tk()
      show_logs_window = ShowLogApp(root)
      scrollbar = tk.Scrollbar(root)

      show_logs_window.master.title('Time Logs') 
      show_logs_window.master.geometry('400x700') #172,138  
      show_logs_window.mainloop()
      sleep_duration_mins=round(max(0,sleep_duration_mins-(datetime.now()-notif_window_exit_time).total_seconds()/60))
    
    print("Sleeping for "+ str(sleep_duration_mins)+" mins")
    time.sleep(sleep_duration_mins*60) 