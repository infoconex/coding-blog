---
title: "Spawning multiple .NET delegates really slow"
date: "2008-10-14"
description: "I recently worked on a project that had a listener service running that took TCP requests and made external calls to a remote WebService. The listener service could have up to 300 concurrent requests."
tags: ["C#"]
slug: "spawning-multiple-net-delegates-really-slow"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2008/10/14/Spawning-multiple-NET-delegates-really-slow"
permalink: "/post/2008/10/14/Spawning-multiple-NET-delegates-really-slow"
legacyPaths: ["/post/2008/10/14/Spawning-multiple-NET-delegates-really-slow"]
---
I recently worked on a project that had a listener service running that took TCP requests and made external calls to a remote WebService. The listener service could have up to 300 concurrent requests.

In testing the service it was showing a significant delay in executing requests above 3-4 concurrent clients. The first bottleneck had to do with the number of allowed HTTP connections to a remote machine from our service. It turns out that by default only 2 concurrent HTTP connections are allowed by default.

Here is an MSDN article that explains the settings that need to be set to allow more connections to be made.

<http://msdn.microsoft.com/en-us/library/fb6y0fyc.aspx>

So setting something like this what required.

configuration>
  <system.net>
    <connectionManagement>
      <add address = "http://www.contoso.com" maxconnection = "10" />
      <add address = "\*" maxconnection = "2" />
    </connectionManagement>
  </system.net>
</configuration>

While this showed a little improvement the problems were not over. It turns out that the ThreadPool by default only starts up with 4 idle threads. As you exceed that limit the ThreadPool checks every 500ms to see if more threads are needed and only spawns up one thread every 500ms. So you can see that it will take a long time to get spawned a large number of concurrent requests.

Solution to this is to set the minimum threads in the threadpool.

ThreadPool.SetMinThreads - <http://msdn.microsoft.com/en-us/library/system.threading.threadpool.setminthreads.aspx>

So we set the Min to the minimum number of threads we wanted sitting idle. Ok now performance was very good up to the number of threads we set as our minimum. But wait things are not over. We moved the code to another machine and the performance degraged. What could be wrong? It worked on my machine just fine!!

So we looked at what was different about the machines. Turned out my machine was running .NET 2.0 and the other machine was running .NET 2.0 SP1. I guess in .NET 2.0 SP1 a new bug was introduced that if threads are requested to quickly it will revert back to slowly invoking new threads.

Solution is to put a delay after each new call to a delegate for a few milliseconds using something like Thread.Sleep(50);. I had to put about 50ms delay on the machine in question. However I found that this bug was to be fixed in .NET 2.0 SP2. A bit of searching I found that .NET 2.0 SP2 had actually been released but not by itself. You have to download .NET 3.5 SP1 which also includes .NET 2.0 SP2. After installing this on the machine no delay was required any longer and performance was very good.

Hope this helps someone
