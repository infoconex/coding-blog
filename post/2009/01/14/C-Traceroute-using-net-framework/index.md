---

title: "C# Traceroute using .net framework"
date: "2009-01-14"
description: "If you have ever tried to create a traceroute program using one of the few available ICMP libraries freely available for C# you may have run into some issues mainly to do with the ICMP…"
tags: []
slug: "c-traceroute-using-net-framework"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/01/14/C-Traceroute-using-net-framework"
permalink: "/post/2009/01/14/C-Traceroute-using-net-framework"
legacyPaths: ["/post/2009/01/14/C-Traceroute-using-net-framework"]
---
If you have ever tried to create a traceroute program using one of the few available ICMP libraries freely available for C# you may have run into some issues mainly to do with the ICMP checksum not being correct. It seems that as of .NET 2.0 framework that microsoft included a Ping class that makes it really easy to then use it to create a traceroute utility. Here is some basic code to create a traceroute utility.

```csharp
public string Traceroute(string ipAddressOrHostName)
{
    IPAddress ipAddress = Dns.GetHostEntry(ipAddressOrHostName).AddressList[0];
    StringBuilder traceResults = new StringBuilder();

    using(Ping pingSender = new Ping())
    {
        PingOptions pingOptions = new PingOptions();
        Stopwatch stopWatch = new Stopwatch();
        byte[] bytes = new byte[32];

        pingOptions.DontFragment = true;
        pingOptions.Ttl = 1;
        int maxHops = 30;


        traceResults.AppendLine(
            string.Format(
                "Tracing route to {0} over a maximum of {1} hops:",
                ipAddress,
                maxHops));

        traceResults.AppendLine();

        for(int i = 1; i < maxHops + 1; i++)
        {
            stopWatch.Reset();
            stopWatch.Start();
            PingReply pingReply = pingSender.Send(
                ipAddress,
                5000,
                new byte[32], pingOptions);

            stopWatch.Stop();

            traceResults.AppendLine(
                string.Format("{0}\t{1} ms\t{2}",
                i,
                stopWatch.ElapsedMilliseconds,
                pingReply.Address));

            if(pingReply.Status == IPStatus.Success)
            {
                traceResults.AppendLine();
                traceResults.AppendLine("Trace complete."); break;
            }

            pingOptions.Ttl++;
        }

    }

    return traceResults.ToString();
}
```

```

```
