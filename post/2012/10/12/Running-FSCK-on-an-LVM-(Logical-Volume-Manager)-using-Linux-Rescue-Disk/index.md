---

title: "Running FSCK on an LVM (Logical Volume Manager) using Linux Rescue Disk"
date: "2012-10-12"
description: "Walk through using a Linux rescue disk to locate LVM volumes and run filesystem checks after a server failure, with commands and troubleshooting context."
tags: ["Linux", "LVM", "Filesystem Recovery", "CentOS", "Troubleshooting"]
slug: "running-fsck-on-an-lvm-logical-volume-manager-using-linux-rescue-disk"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk"
permalink: "/post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk"
legacyPaths: ["/post/2012/10/12/Running-FSCK-on-an-LVM-(Logical-Volume-Manager)-using-Linux-Rescue-Disk"]
---
## Recovering a failed server (2012)

I am not a linux expert and so when I have problems from time to time I usually have to go searching for the answer. It usually takes me looking at several articles to get my answer and when I am finished I always try and put together a article that has everything I need to know in once spot. Please feel free to correct or suggest a better alternative if you come across this article and would like to provide feedback.

Yesterday I had a server crash and when I logged into the console it was showing a kernal panic!!

I rebooted and the same thing happened over on every reboot. This machine had some problems in the past with the disk going into read only mode so I assumed the issue was related to something wrong with the disk. So I grabbed a CentOS disk and booted up with it and booted into resuce mode and skipped the step that would mount the disks.

Once in I attempted to run `fsck /dev/sda1` but I got an error back indicating it did not recognize the volume as EXT2. Searching around I found the following solution if you are using a LVM.

> **Historical recovery note:** This describes what worked for my 2012 CentOS system, not a universal recovery procedure. Filesystem repair can modify or lose data. Before attempting it on a current system, investigate disk-health errors, preserve a backup or disk image when possible, identify the actual filesystem and logical volume, and keep the filesystem **unmounted** during repair. The `fsck` example below is not appropriate for every filesystem: for example, XFS uses `xfs_repair`. See [Red Hat’s filesystem checking and repair guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_file_systems/checking-and-repairing-a-file-system__managing-file-systems) for modern, filesystem-specific procedures.

## Locating and activating the LVM volumes

 The following are the original commands I used during this recovery, in the order I used them. They are preserved as a historical example; verify the volume names, arguments, and filesystem-specific repair steps before adapting any of them. I provided a link for each command if you are interested in knowing more about what each of the commands do.

### Scan physical volumes

Scan all disks for partiitions:

- lvm [pvscan](https://man7.org/linux/man-pages/man8/pvscan.8.html)

### Scan volume groups

Scan all disks for volume groups and build /etc/lvmtab and /etc/lvmtab.d/\* which are the database for all other lvm commands:

- lvm [vgscan](https://man7.org/linux/man-pages/man8/vgscan.8.html)

### Activate a logical volume

Change attributes of a logical volume

- lvm [lvchange](https://man7.org/linux/man-pages/man8/lvchange.8.html) -ay VolGroup00

### Scan logical volumes

Scan all disks for logical volumes

- lvm [lvscan](https://man7.org/linux/man-pages/man8/lvscan.8.html)

## Running the filesystem check

Then I was able to run fsck as follows

```bash
fsck -f /dev/VolGroup00/LogVol00
```

Which of course reported TONS of errors and fixed them up. I do not claim to be an expert but this worked for me. Hopefully this information will help someone else out in the future.
