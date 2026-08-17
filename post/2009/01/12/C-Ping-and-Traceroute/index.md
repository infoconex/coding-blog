---
title: "C# Ping"
date: "2009-01-12"
description: "I was recently tasked with putting together a ping and traceroute feature in an application and like I always do I googled to see if someone had already worked out how to do this."
tags: []
slug: "c-ping"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/01/12/C-Ping-and-Traceroute"
permalink: "/post/2009/01/12/C-Ping-and-Traceroute"
legacyPaths: ["/post/2009/01/12/C-Ping-and-Traceroute"]
---
I was recently tasked with putting together a ping and traceroute feature in an application and like I always do I googled to see if someone had already worked out how to do this.

I found a few people who had posted ICMP libraries and so I used one of them and tested and everything seemed to work properly. However I was getting reports that it was not working on Vista. However the person could use the built in ping and tracert utilities with no issue.

At first I thought it might be related to permissions or firewall but none of those ended up resolving the issue.

So I fired up wireshark and looked at what was different at the packet level between what I was doing and what the built in windows ping was doing.

The code I was using was returning an incorrect checksum on the ICMP reply. So I searched a bit to learn about the checksum and ended up finding somehow that as of .NET 2.0 framework there is a Ping class built into the framework!!

So I am posting this in hopes of saving someone a bunch of time with the same issue I had. Also the code I had to put together initially was much more complex. This I think you will see is very straight forward.

[Download PingUtility.cs (3.14 kb)](/file.axd?file=PingUtility.cs)

Example Output:

```
Pinging 192.168.105.10 with 32 bytes of data:

Reply from 192.168.105.10: bytes=32 time=11ms TTL=128
Reply from 192.168.105.10: bytes=32 time=3ms TTL=128
Reply from 192.168.105.10: bytes=32 time=3ms TTL=128
Reply from 192.168.105.10: bytes=32 time=3ms TTL=128

Ping statistics for 192.168.105.10:
	Packets: Sent = 4, Received = 4, Lost = 0
Approximate round trip times in milli-seconds:
	Minimum = 3ms, Maximum = 11ms
```

```
Code:
```

```csharp
public

static

string
 Ping()

{


using
 (Ping pingSender =
new
 Ping())

    {

        PingOptions pingOptions =
null
;

        StringBuilder pingResults =
null
;

        PingReply pingReply =
null
;

        IPAddress ipAddress =
null
;


int
 numberOfPings = 4;


int
 pingTimeout = 1000;


int
 byteSize = 32;


byte
[] buffer =
new

byte
[byteSize];


int
 sentPings = 0;


int
 receivedPings = 0;


int
 lostPings = 0;


long
 minPingResponse = 0;


long
 maxPingResponse = 0;


string
 ipAddressString = "
192.168.105.10
";

        pingOptions =
new
 PingOptions();


//pingOptions.DontFragment = true;


//pingOptions.Ttl = 128;

        ipAddress = IPAddress.Parse(ipAddressString);

        pingResults =
new
 StringBuilder();

        pingResults.AppendLine(
string
.Format("
Pinging {0} with {1} bytes of data:
", ipAddress, byteSize));

        pingResults.AppendLine();


for
 (
int
 i = 0; i < numberOfPings; i++)

        {

            sentPings++;

            pingReply = pingSender.Send(ipAddress, pingTimeout, buffer, pingOptions);


if
 (pingReply.Status == IPStatus.Success)

            {

                pingResults.AppendLine(
string
.Format("
Reply from {0}: bytes={1} time={2}ms TTL={3}
", ipAddress, byteSize, pingReply.RoundtripTime, pingReply.Options.Ttl));


if
 (minPingResponse == 0)

                {

                    minPingResponse = pingReply.RoundtripTime;

                    maxPingResponse = minPingResponse;

                }


else

if
 (pingReply.RoundtripTime < minPingResponse)

                {

                    minPingResponse = pingReply.RoundtripTime;

                }


else

if
 (pingReply.RoundtripTime > maxPingResponse)

                {

                    maxPingResponse = pingReply.RoundtripTime;

                }

                receivedPings++;

            }


else

            {

                pingResults.AppendLine(pingReply.Status.ToString());

                lostPings++;

            }

        }

        pingResults.AppendLine();

        pingResults.AppendLine(
string
.Format("
Ping statistics for {0}:
", ipAddress));

        pingResults.AppendLine(
string
.Format("
\tPackets: Sent = {0}, Received = {1}, Lost = {2}
", sentPings, receivedPings, lostPings));

        pingResults.AppendLine("
Approximate round trip times in milli-seconds:
");

        pingResults.AppendLine(
string
.Format("
\tMinimum = {0}ms, Maximum = {1}ms
", minPingResponse, maxPingResponse));


return
 pingResults.ToString();

    }

}
```
