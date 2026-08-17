---
title: "Running FSCK on an LVM (Logical Volume Manager) using Linux Rescue Disk"
date: "2012-10-12"
description: "I am not a linux expert and so when I have problems from time to time I usually have to go searching for the answer. It usually takes me looking at several articles to get my answer and when I am finished I always try a…"
tags: []
slug: "running-fsck-on-an-lvm-logical-volume-manager-using-linux-rescue-disk"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk"
permalink: "/post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk"
legacyPaths: ["/post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk"]
---
I am not a linux expert and so when I have problems from time to time I usually have to go searching for the answer. It usually takes me looking at several articles to get my answer and when I am finished I always try and put together a article that has everything I need to know in once spot. Please feel free to correct or suggest a better alternative if you come across this article and would like to provide feedback.

Yesterday I had a server crash and when I logged into the console it was showing a kernal panic!!

I rebooted and the same thing happened over on every reboot. This machine had some problems in the past with the disk going into read only mode so I assumed the issue was related to something wrong with the disk. So I grabbed a CentOS disk and booted up with it and booted into resuce mode and skipped the step that would mount the disks.

Once in I attempted to run fsck /dev/sda1 but I got an error back indicating it did not recognize the volume as EXT2. Searching around I found the following solution if you are using a LVM.

 Perform all of the following commands in the following order. I provided a link for each command if you are interested in knowing more about what each of the commands do.

Scan all disks for partiitions:

- lvm [pvscan](http://linux.about.com/library/cmd/blcmdl8_pvscan.htm)

Scan all disks for volume groups and build /etc/lvmtab and /etc/lvmtab.d/\* which are the database for all other lvm commands:

- lvm [vgscan](http://linux.about.com/library/cmd/blcmdl8_vgscan.htm)

Change attributes of a logical volume

- lvm [lvchange](http://linux.about.com/library/cmd/blcmdl8_lvchange.htm) -ay VolGroup00

Scan all disks for logical volumes

- lvm [lvscan](http://linux.about.com/library/cmd/blcmdl8_lvscan.htm)

Then I was able to run fsck as follows

fsck -f /dev/VolGroup00/LogVol00

Which of course reported TONS of errors and fixed them up. I do not claim to be an expert but this worked for me. Hopefully this information will help someone else out in the future.
