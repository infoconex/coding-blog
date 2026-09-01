---
title: "HP MediaSmart Server is my favorite device for 2009"
date: "2009-11-27"
description: "Automatically Backup all your PC’s and MAC’s. If backing up your machine is important to you but you have just not taken the step to implement a backup process, then I would highly recommend the HP MediaSmart Server . W…"
tags: []
slug: "hp-mediasmart-server-is-my-favorite-device-for-2009"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/11/27/HP-MediaSmart-Server-is-my-favorite-device-for-2009"
permalink: "/post/2009/11/27/HP-MediaSmart-Server-is-my-favorite-device-for-2009"
legacyPaths: ["/post/2009/11/27/HP-MediaSmart-Server-is-my-favorite-device-for-2009"]
---
**Automatically Backup all your PC’s and MAC’s.** If backing up your machine is important to you but you have just not taken the step to implement a backup process, then I would highly recommend the **[HP MediaSmart Server](http://www.amazon.com/gp/product/B002N8A0A2?ie=UTF8&tag=codblo-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=B002N8A0A2)** . While it has many features the most important and coolest one in my opinion is the backup feature.

|  |  |  |
| --- | --- | --- |
|  | ![HP MediaSmart Server Drive Bays](images/1-open-6.jpg) | ![HP MediaSmart Server Back View](images/3-back-4.jpg) |

**So what is so cool about it?**

No matter how many computers you are backing up the [HP MediaSmart Server](http://www.amazon.com/gp/product/B002N8A0A2?ie=UTF8&tag=codblo-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=B002N8A0A2) will only keep a single copy of a given file. That means if you have 3 machines in your network all running Windows 7 the space required to backup the OS will only be the size of one of them. Below is the description from a Microsoft Document explaining how backup works.

*The home computer backup solution in Windows Home Server has a single-instance store at the cluster level. Clusters are typically collections of data stored on the hard drive, 4 kilobytes (KB) in size. Every backup is a full backup, but the home server only stores each unique cluster once. This creates the restore-time convenience of full backups (you do not have to repeat history) with the backup time performance of incremental backups.*

*The home computer backup occurs as follows:*

- *When a home computer is backed up to the home server, Windows Home Server software figures out what clusters have changed since the last backup.*
- *The home computer software then calculates a hash for each of these clusters and sends the hashes to the home server. A hash is a number that uniquely identifies a cluster based on its contents.*
- *The home server looks into its database of clusters to see if they are already stored on the home server.*
- *If they are not stored on the home server already, then the home server asks the home computer to send them.*
- *All file system information is preserved such that a hard disk volume (from any home computer) at any backup point (time) can be reconstituted from the database.*

**So imagine this scenario:** You bring home your new HP MediaSmart Server and set it up by plugging in power and an ethernet cable. You install the client application on one of your machines. You run your first backup of your machine which for me took 17 minutes and 21 seconds to backup a base install of Windows 7 Ultimate Edition with all the updates applied (see below image).

![image](images/image-thumb.png "image")

By default it ignores things like user temporary files, system page file (mine was 2.29GB) , recycle bin, Hibernation file (mine was 2GB), Shadow volume implementation folders (mine was 19.54GB). That saved a tone of space and I would never want to really backup those anyways.

Ok, so you are probably thinking is that all? No it only gets better. Now you go to your second machine that one of your kids use and install the software because you want to have it backed up. The backup software reads all of the data but instead of having to backup everything it only needs to transmit content of those clusters that the home server does not already have. So if this machine has a lot of the same files or the same OS you wont be backing up a second copy of the same file. So think about it. How many machines do you have that have all the same music, photos, software etc… Only one copy of any of that will have to be stored.

Ok, getting cooler? Now you have all your machines in your network setup and backing up. Keep in mind that they are also backing up to a network device that is dedicated to your backups.

Ok, so hopefully you have made it down this far as I saved the best part for last. BARE METAL RESTORE!! For those not familiar with that term it means I could have a machine have a complete hardrive failure, pull it out and install a new blank one, grab the provided restore CD provided by HP, boot up my machine from the CD and it will then search the network, find my HP MediaSmart Server and provide me with a list of backups I can choose to restore from. Come back in a bit and my machine is back up and running as if nothing happened.

Now I don't know about you but that is worth a lot of money. In fact I got to try this process out 2 weeks after I purchased it. One of the things I did when purchasing this unit was to purchase a new larger hardrive. 2 Weeks later my new drive would not work and I had to take it back to the store and get a replacement. I brought the new drive home and restored from backup for the previous day and was back up and running in about 2 hours which I only had to walk away and come back when it was finished.

**Other Features:** Now I have only talked about backup. While that is in my opinion the coolest feature it is not the only. The HP MediaSmart Server also has the following features.

**Media Storage and Streaming:** You can setup the HP MediaSmart Server search computers on an interval and look for Pictures, Music and Videos and take a copy of them over to the server. Music is then available to be streamed to Media Extender devices, iPod, XBOX, Media Center machines, or access via web interface.

**Media Streamer:** Page accessible to stream your Music, Videos and Photos

![image](images/image-thumb-1.png "image")

**Online Photo Album:** Publish pictures that you can then provide access to.

![image](images/image-thumb-2.png "image")

**Small Size:** The unit is only 5.5” x 9.8” x 9.2” in size.

**Remote Access:** If you have the ability to make the device internet accessible then you can also provide Remote Access to any of your machines using Microsoft Remote Desktop services. This provides the ability to remotely access your machines from anywhere. As well once internet connected you can access your files, music, videos and pictures. Also your music and videos are streamed to you as you listen to them so you can instantly start listening to them rather than having to download them first. This also provides a optimum experience if you don’t have a lot of bandwidth.

**HP MediaSmart Server Home:** Default page showing what is available via a web browser.

![image](images/image-thumb-3.png "image")

**Computer Access:** Shows the list of machines in the network that are available to be connected to remotely.

![image](images/image-thumb-4.png "image")

**User Accounts**Each person in your home or small office can have a user account in which they can use to store files in a central location. Now you can share folders on the HP MediaSmart Server and give access to only those that need them.

**Storage**
You can have up to 4 drives in the HP MediaSmart Server and they are also able to be HOT Swapped. My unit came with a 750GB drive and I purchased a 1TB drive to add more capacity and provide a backup drive. The HP MediaSmart Server does not use traditional RAID configuration but rather allow you to define folders that should have the data stored on more than one drive. So in a raid configuration if you put in another drive you do not get access to it as it is only used to provide a backup drive. With the HP MediaSmart Server you get all the extra capacity minus whatever is needed to keep a backup of the folders you said should be mirrored. Maximum storage is only limited by the number of drives and USB ports. So take 4 2TB drives and put them in and 4 2TB external USB drives and you have a whopping 16TB of storage.

**Many More Features**There is a lot more features that you can check out on Amazon. Here is a link to the one I purchased. [HP EX490 1TB Mediasmart Home Server (Black)](http://www.amazon.com/gp/product/B002N8A0A2?ie=UTF8&tag=codblo-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=B002N8A0A2)
