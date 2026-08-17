---
title: "Replacing text in a stream after writing"
date: "2009-05-22"
description: "Recently I responded to a question asked on StackOverflow. The question was \"What is the BEST way to replace text in a File using C# / .NET?\""
tags: []
slug: "replacing-text-in-a-stream-after-writing"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/05/22/Replacing-text-in-a-stream-after-writing"
permalink: "/post/2009/05/22/Replacing-text-in-a-stream-after-writing"
legacyPaths: ["/post/2009/05/22/Replacing-text-in-a-stream-after-writing"]
---
Recently I responded to a question asked on StackOverflow. The question was "What is the BEST way to replace text in a File using C# / .NET?"

Just by the question you might assume they were wanting to simply replace text in an existing file and of course you could do that by opening the file and looping over it or doing a Replace of content.

Here is the requirements they gave.

Have a text file that is being written to as part of a very large data extract. The first line of the text file is the number of "accounts" extracted.

Because of the nature of this extract, that number is not known until the very end of the process, but the file can be large (a few hundred megs).

What is the BEST way in C# / .NET to open a file (in this case a simple text file), and replace the data that is in the first "line" of text?

So as you can see they are in the process of writing the file, at the end of the write of the file they now know the information they wish to write at the top of the file. So how might we able to go back and write that information without having to open the file again and write the information at the top of the file?

It turns out it is actually fairly simple. One we want to make sure memory utilization is a factor since these files can be very large we probably do not want to open the whole file and prepend text, or do some kind of search and replace on text content that size. So my suggestion is using a stream. Also by using a Stream we can avoid entirely writing the file, then having to open the file again and write the text. StreamWriter has a BaseStream property that provides you access to the base stream object which then allows you to set the position of the stream back to the top and write out the information.

Here is my answer.

```csharp
private

void
 WriteUsers()
{

string
 userCountString =
null
;
    ASCIIEncoding enc =
new
 ASCIIEncoding();

byte
[] userCountBytes =
null
;

int
 userCounter = 0;


using
(StreamWriter sw = File.CreateText(
"myfile.txt"
))
    {

// Write a blank line and return


// Note this line will later contain our user count.

        sw.WriteLine();


// Write out the records and keep track of the count


for
(
int
 i = 1; i < 100; i++)
        {
            sw.WriteLine(
"User"
 + i);
            userCounter++;
        }


// Get the base stream and set the position to 0

        sw.BaseStream.Position = 0;

        userCountString =
"User Count: "
 + userCounter;

        userCountBytes = enc.GetBytes(userCountString);

        sw.BaseStream.Write(userCountBytes, 0, userCountBytes.Length);
    }

}
```
