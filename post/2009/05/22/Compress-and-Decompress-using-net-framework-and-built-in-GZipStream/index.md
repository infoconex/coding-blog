---

title: "Compress and Decompress using .net framework and built in GZipStream"
date: "2009-05-22"
description: "I recently had a project in which I wanted to compress log files I was transferring between servers."
tags: []
slug: "compress-and-decompress-using-net-framework-and-built-in-gzipstream"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/05/22/Compress-and-Decompress-using-net-framework-and-built-in-GZipStream"
permalink: "/post/2009/05/22/Compress-and-Decompress-using-net-framework-and-built-in-GZipStream"
legacyPaths: ["/post/2009/05/22/Compress-and-Decompress-using-net-framework-and-built-in-GZipStream"]
---
I recently had a project in which I wanted to compress log files I was transferring between servers. I did not realize till I did some research that the .NET framework has a nice little library built in for creating GZIP files. While I think the maximum recommended size for using this is 4GIG I am well under that.

Here is my Compress / Decompress methods

```
byte
[] startfile = File.ReadAllBytes(
"e:\\mylog.log"
);
byte
[] comp =
null
;
byte
[] decom =
null
;

comp = CompressBytes(startfile);
Console.WriteLine(comp.Length.ToString());
decom = Decompress(comp);
Console.WriteLine(decom.Length.ToString());

```

```csharp
private

void
 Compress(
byte
[] fileBytes)
{

using
(MemoryStream ms =
new
 MemoryStream())
    {

using
(GZipStream gz =
new
 GZipStream(ms,
                                             CompressionMode.Compress,

true
))
        {
            gz.Write(fileBytes, 0, fileBytes.Length);
            gz.Close();
        }
    }
}
private

byte
[] Decompress(
byte
[] fileBytes)
{

int
 buffer_size = 100;

using
(MemoryStream ms =
new
 MemoryStream(fileBytes))
    {

using
(GZipStream gz =
new
 GZipStream(ms,
                                             CompressionMode.Decompress,

true
))
        {

byte
[] bufferFooter =
null
;

int
 readOffset = 0;

int
 totalBytes = 0;

byte
[] finalBuffer =
null
;

int
 uncompLength = 0;

int
 compressedFileLength = fileBytes.Length;

// Get last 4 bytes (footer) as they contain the

// original length of the compressed bytes


// byte array to hold footer value
            bufferFooter =
new

byte
[4];

// Set position of MemoryStream end of stream

// minus the 4 bytes needed
            ms.Position = ms.Length - 4;


// Fill the bufferFooter with the last 4 bytes
            ms.Read(bufferFooter, 0, 4);

// Set Stream back to 0
            ms.Position = 0;

// Convert footer bytes to the length.
            uncompLength = BitConverter.ToInt32(bufferFooter, 0);

// Set a temporary buffer to hold the uncompressed

// information. We also make it slightly larger to

// ensure everything will fit. We will later trim

// off the unused bytes.
            finalBuffer =
new

byte
[uncompLength + buffer_size];

while
(
true
)
            {

// Read from stream up to buffer size. Note that return

// value is actual bytes read in case the number filled

// is less than we requested.

int
 bytesRead = gz.Read(finalBuffer,
                                        readOffset,
                                        buffer_size);

// If no bytes returned we are done

if
(bytesRead == 0)
                {

break
;
                }
                readOffset += bytesRead;
                totalBytes += bytesRead;
            }

// Trim off unused bytes based
            Array.Resize<
byte
>(
ref
 finalBuffer, totalBytes);

return
 finalBuffer;
        }
    }
}
```
