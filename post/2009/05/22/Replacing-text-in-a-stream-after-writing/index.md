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

It turns out it is actually fairly simple. One we want to make sure memory utilization is a factor since these files can be very large we probably do not want to open the whole file and prepend text, or do some kind of search and replace on text content that size. So my suggestion is using a stream. Also by using a Stream we can avoid entirely writing the file, then having to open the file again and write the text. StreamWriter has a BaseStream property that lets you access the underlying stream. However, the original example did not flush its buffered text before writing directly to that stream, and its initial blank line did not reserve enough space for a longer count. The corrected example reserves a fixed-width ASCII header, flushes the StreamWriter before seeking, then overwrites only those reserved bytes. This approach avoids loading a large extract into memory. The header width must be large enough for the expected count.

Here is my answer.

```csharp
private void WriteUsers()
{
    const int headerWidth = 32;
    int userCounter = 0;

    using (FileStream stream = new FileStream(
        "myfile.txt", FileMode.Create, FileAccess.Write))
    using (StreamWriter writer = new StreamWriter(stream, Encoding.ASCII))
    {
        // Reserve a fixed-width first line; the count is not known yet.
        writer.WriteLine(new string(' ', headerWidth));

        for (int i = 1; i < 100; i++)
        {
            writer.WriteLine("User" + i);
            userCounter++;
        }

        // Flush the text writer before writing directly to its BaseStream.
        writer.Flush();

        string header = ("User Count: " + userCounter).PadRight(headerWidth);
        if (header.Length != headerWidth)
        {
            throw new InvalidOperationException("Header exceeds reserved width.");
        }

        byte[] headerBytes = Encoding.ASCII.GetBytes(header);
        stream.Position = 0;
        stream.Write(headerBytes, 0, headerBytes.Length);
    }
}
```
