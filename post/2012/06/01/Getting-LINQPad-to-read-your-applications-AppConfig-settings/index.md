---

title: "Getting LINQPad to read your applications App.Config settings"
date: "2012-06-01"
description: "I have been using LINQPad for a while now and I love it. This utility allows me to write and execute immediately code that I am working out before I put it into my project."
tags: ["LINQPad"]
slug: "getting-linqpad-to-read-your-applications-app-config-settings"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2012/06/01/Getting-LINQPad-to-read-your-applications-AppConfig-settings"
permalink: "/post/2012/06/01/Getting-LINQPad-to-read-your-applications-AppConfig-settings"
legacyPaths: ["/post/2012/06/01/Getting-LINQPad-to-read-your-applications-AppConfig-settings"]
---
I have been using LINQPad for a while now and I love it. This utility allows me to write and execute immediately code that I am working out before I put it into my project. However on occassion I need to reference assemblies from my project that are getting settings from the applications App.Config such as SQL connection strings etc...

Each time I would run into this I would search and not come up with how to get my app.config settings to be honored by LINQPad and today I finally found how to do it so I thought I would write up something really quick to show others how to accomplish this.

1) Find the path that LINQPad uses for its configuration file by excuting this: AppDomain.CurrentDomain.SetupInformation.ConfigurationFile.Dump()

This returned for me the following: C:\Program Files\LINQPad4\LINQPad.config

I was suprised this returned LINQPad.config instead of LINQPad.exe.config which is what you would typically expect since most .NET applications name the file the same as the executable.

2) Take your App.config and copy it to the location above naming the config file whatever yours returned. In my case it was LINQPad.config

3) Close LINQPad or the TAB that you have opened to execute your assembly and reopen to get LINQPad to read the configuration file.

Now execute your code and you should see that LINQPad is now pulling in your settings as needed.
