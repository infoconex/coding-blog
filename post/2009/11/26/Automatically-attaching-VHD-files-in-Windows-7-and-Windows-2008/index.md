---

title: "Automatically attaching VHD files in Windows 7 and Windows 2008"
date: "2009-11-26"
description: "If you have played with the new VHD feature in windows 7 or windows 2008 then you know just how cool of a feature this is."
tags: []
slug: "automatically-attaching-vhd-files-in-windows-7-and-windows-2008"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/11/26/Automatically-attaching-VHD-files-in-Windows-7-and-Windows-2008"
permalink: "/post/2009/11/26/Automatically-attaching-VHD-files-in-Windows-7-and-Windows-2008"
legacyPaths: ["/post/2009/11/26/Automatically-attaching-VHD-files-in-Windows-7-and-Windows-2008"]
---
If you have played with the new VHD feature in windows 7 or windows 2008 then you know just how cool of a feature this is. However the problem is that when you reboot your machine you find that when it comes back up all your VHD files are no longer attached? Here is what I did to get around the issue.

1. **Create a batch file** that will hold the following line:

    `diskpart /s "c:\path to script\diskpartscript.txt"`

    I named my batch file `attachvhd.bat` and placed it in the same folder as my VHD files.

    [![attachvhd](images/attachvhd-thumb.jpg "attachvhd")](images/attachvhd.jpg)

2. **Create the script file** that is being referenced by the `attachvhd.bat` batch file. Here is what the contents of that script needs to contain:

    ```text
    select vdisk file="c:\path to vhd files\myvhddrive.vhd"
    attach vdisk
    ```

    I named my script file `diskpartscript.txt` and placed it in the same folder as my VHD files.

    [![script](images/script-thumb.jpg "script")](images/script.jpg)

3. **Create a scheduled task** that will automatically run when your machine starts up.

    - Go to Start / Administrative Tools / Task Scheduler

    - **Click** Create Basic Task

        [![1_addtask](images/1-addtask-thumb-2.jpg "1_addtask")](images/1-addtask-2.jpg)

    - **Fill in the name** of the task and the description and **Click Next**

        [![2_createbasictask](images/2-createbasictask-thumb-2.jpg "2_createbasictask")](images/2-createbasictask-2.jpg)

    - **Select “Start a program”** radio button option and then **Click Next**

        [![3_start_program](images/3-start-program-thumb-1.jpg "3_start_program")](images/3-start-program-1.jpg)

    - **Select “When the computer starts”** and then **Click Next**

        [![3_when_computer_starts](images/3-when-computer-starts-thumb-2.jpg "3_when_computer_starts")](images/3-when-computer-starts-2.jpg)

    - **Browse** to the folder that you setup your batch file in and select it. **Click Next**

        [![5_script](images/5-script-thumb-2.jpg "5_script")](images/5-script-2.jpg)

    - **Click Finish**

        [![6_finish](images/6-finish-thumb-2.jpg "6_finish")](images/6-finish-2.jpg)

4. **You have now completed** all the necessary steps. Restart your computer and you should find that your VHD files are now automatically attached. One caveat is that if you reboot and you log into your machine quick enough it is possible that the task may not have been run yet. Once you are logged in if the task runs you will get an Autoplay dialog as follows. Simply close it. This does not happen if the task runs before you get logged in.

    [![auto_play](images/auto-play-thumb-1.jpg "auto_play")](images/auto-play-1.jpg)
