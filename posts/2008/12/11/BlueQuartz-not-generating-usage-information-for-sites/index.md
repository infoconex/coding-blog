---
title: "BlueQuartz not generating usage information for sites"
date: "2008-12-11"
description: "For those that might be having the same problem here is what I found."
tags: []
slug: "bluequartz-not-generating-usage-information-for-sites"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/12/11/BlueQuartz-not-generating-usage-information-for-sites"
permalink: "/post/2008/12/11/BlueQuartz-not-generating-usage-information-for-sites"
legacyPaths: ["/post/2008/12/11/BlueQuartz-not-generating-usage-information-for-sites"]
---
For those that might be having the same problem here is what I found.

Going to Usage Information and clicking to generate web, mail or ftp stats resulted in no stats available for period. I looked for a recent site created and tried and stats worked. When I went and looked at what the difference was between the site that worked and the one did not I found there was a permission difference on the logs folder.

Site that worked
drwxr-s---  3 nobody site26  4096 Nov 13 03:28 logs

Site that did not work
drwxr-s--x   4 SITE66-logs site66  4096 Dec 11 12:30 logs

To fix this I issued this command to reset on all sites the permission on the logs folder

find /home -type d -name 'logs' -mindepth 4 -print | xargs chmod 02751

Now all my sites are able to generate stats again.
