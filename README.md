# TrackEveryday
A non-intrusive and periodic notification program to track every day activities from work projects to personal tasks.

# TL;DR
  * Download TrackEveryday.exe from windows10_distribution folder. 
  * Download settings.txt from windows10_distribution folder. 
  * Keep both files in the same folder.
  * Customize the values of NotificationInterval, Tasks and PauseInterval in settings.txt as per the instructions there.


# Application description
This is a non-intrusive and periodic notification program to track every day activities from work projects to personal tasks.  
You can configure a list of every day tasks to measure for yourself the time spent on each task on a daily/weekly/monthly basis.
The tasks can be work tasks like different projects, meetings etc., or personal tasks like, while working from home, how much time you are spending standing at your standing desk, how many times you are drinking water etc. 
You can configure all the tasks you want to track in \"settings.txt\" file (\"Tasks\" field) and the program will show a notification window every \"x\" minutes (This \"x\" can also be configured using the \"NotificationInterval\" field in \"serttings.txt\")
The repository has a precompiled Windows 10 executable in \"windows10_distribution\" folder. Or you can use the python source code (and pyinstaller package) to build on Mac OS or Linux. 
The program does not upload any data to any remote server or take any screenshots or any fuzzy stuff like that. The main reason for creating this program is to be non-intrusive and in total control of the user.

## Table of Contents

* [Usage](#usage)
  * [Windows Executable](#windows-executable)
    * [Start on boot](#start-on-boot)
  * [Features](#features)
    * [settings.txt](#settings-txt)
    * [GUI features](#gui-features)
* [Build from python source](#build-from-python-source)
* [To do](#to-do)
* [Cite](#cite)

## Usage

### Windows Executable
For Windows users, you can directly use the provided exe.
  * Download TrackEveryday.exe from windows10_distribution folder. 
  * Download settings.txt from windows10_distribution folder. 
  * Keep both files in the same folder.
  * Customize the values of NotificationInterval, Tasks and PauseInterval in settings.txt
  * Click on the TrackEveryday.exe
  * A notification window will pop up on the right top side of your screen showing check boxes next to all the "Tasks" you have configured.
  * Check the tasks you have performed during previous NotificationInterval minutes and press Done button.
  * The program will log the time for those tasks and close.
  * You will keep receiving the notification window every NotificationInterval minutes.
  * You can check your task wise time logs for every day in the "Logs" folder. Time is logged to YYYY_MM_TimeLog.tsv file where YYYY is current year and MM is current month.
The program is up and running till you shutdown the computer. To configure the exe to automatically start when you reboot, check the following section. 

### Start on boot
  * Right click on TrackEveryday.exe and select "Create shortcut".
  * Copy the shortcut file to C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup  where "USERNAME" is your windows username

### Features
This is a very simple program with a simple GUI. "settings.txt" contains 3 configurable parameters and GUI has 3 buttons.

[![GUI](https://github.com/udaypk/trackeveryday/blob/master/GUI.jpg)]
#### settings.txt 
There are just 3 parameters to configure as per your choice.
  * NotificationInterval => This is the time interval at which you want to receive a notification window (in minutes). If you keep this value as 15, you will receive notification every 15 minutes.
  * Tasks => List of all the tasks you want to track every day (each is comma separated)
  * PauseInterval => There may be times where you want to pause the notifications. When you press the Pause button in the GUI, the notifications will not appear for the duration configured here.
  
#### GUI features 
There are just 3 buttons in the GUI. After you check the task check boxes you can press any of the 3 buttons (Done, Show, Pause) to log the time for the tasks.
  * Done => After you check the checkbox of the tasks you want to log time, press Done button. Your time will be logged and the notification window will close.
  * Pause => Press this button to pause notifications. You should also check the task checkboxes so that the time is logged for those tasks. 
  * Show => This button shows you a new window with the details of all the amount of time spent per task aggregated over one month.
There is also a text box present on the right side of every task. This is a way to manually log time more than NotificationInterval. 
For example your NotificationInterval is 15 minutes and you forgot to click on the notification window for 45 minutes, you can enter 2 in the text box next to the task so that extra 2*NotificationInterval time is logged.

## Build from python source
You can build this program for Windows, Mac OS and Linux using pyinstaller. 
Clone the repository and run the command 
```
pyinstaller --onefile -w 'TrackEveryday.py'
```

## To do
  * Settings through GUI Menu
  * More granular logs in "Show" button (Daily/Weekly/Task based etc)

## Cite
```
@misc{Uday2020,
  author = {Uday, Kiran P},
  title = {MyTracker},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/udaypk/trackeveryday}}
}
```