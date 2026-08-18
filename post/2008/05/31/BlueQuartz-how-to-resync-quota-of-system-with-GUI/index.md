---
title: "BlueQuartz how to resync quota of system with GUI"
date: "2008-05-31"
description: "Not sure how many others have had this issue but on occasion I get a user that calls because they are getting email rejected because they are over quota. I log into the administration interface only to find that the quo…"
tags: ["Quota"]
slug: "bluequartz-how-to-resync-quota-of-system-with-gui"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/05/31/BlueQuartz-how-to-resync-quota-of-system-with-GUI"
permalink: "/post/2008/05/31/BlueQuartz-how-to-resync-quota-of-system-with-GUI"
legacyPaths: ["/post/2008/05/31/BlueQuartz-how-to-resync-quota-of-system-with-GUI"]
---
Not sure how many others have had this issue but on occasion I get a user that calls because they are getting email rejected because they are over quota. I log into the administration interface only to find that the quota does not report that they are over quota. I go to a command prompt and checkquota and sure enough  they are over quota.

 So seems that I have a difference between what BQ reports and what the system actually reports. I have asked, googled and for over a year did not find a solution other than to simply increase the site quota so it allowed for the difference. Obviously not a very good solution.

Well I finally figured out how to fix it and it is really simple so I thought I would put it online for others to hopefully use in the future.

/sbin/quotaoff -u /home/
/sbin/quotacheck /home/ -m
/sbin/quotaon -u /home/

That is it. Could not believe for how many questions I asked and the googling I did that it came down to this set of simple steps.
