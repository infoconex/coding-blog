---

title: "Compress and Decompress using .net framework and built in GZipStream"
date: "2009-05-22"
description: "Use the .NET Framework GZipStream class to compress and decompress files in C#, with sample methods developed for transferring log files between servers."
tags: []
slug: "compress-and-decompress-using-net-framework-and-built-in-gzipstream"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/05/22/Compress-and-Decompress-using-net-framework-and-built-in-GZipStream"
permalink: "/post/2009/05/22/Compress-and-Decompress-using-net-framework-and-built-in-GZipStream"
legacyPaths: ["/post/2009/05/22/Compress-and-Decompress-using-net-framework-and-built-in-GZipStream"]
---
I recently had a project in which I wanted to compress log files I was transferring between servers. I did not realize till I did some research that the .NET framework has a nice little library built in for creating GZIP files. While I think the maximum recommended size for using this is 4GIG I am well under that.

Here is a complete C# example that compresses a log file into a GZip byte array and then decompresses it. The original sample had formatting damage from migration, and its compression method did not return a value even though the usage example expected one. The version below corrects those issues while remaining compatible with .NET Framework 3.5.

```csharp
byte[] startFile = File.ReadAllBytes(@"e:\mylog.log");
byte[] compressed = CompressBytes(startFile);
Console.WriteLine(compressed.Length);

byte[] decompressed = Decompress(compressed);
Console.WriteLine(decompressed.Length);
```

```csharp
private static byte[] CompressBytes(byte[] fileBytes)
{
    using (MemoryStream output = new MemoryStream())
    {
        using (GZipStream gzip = new GZipStream(
            output, CompressionMode.Compress, true))
        {
            gzip.Write(fileBytes, 0, fileBytes.Length);
        }

        return output.ToArray();
    }
}

private static byte[] Decompress(byte[] fileBytes)
{
    using (MemoryStream input = new MemoryStream(fileBytes))
    using (GZipStream gzip = new GZipStream(
        input, CompressionMode.Decompress))
    using (MemoryStream output = new MemoryStream())
    {
        byte[] buffer = new byte[8192];
        int bytesRead;

        while ((bytesRead = gzip.Read(buffer, 0, buffer.Length)) > 0)
        {
            output.Write(buffer, 0, bytesRead);
        }

        return output.ToArray();
    }
}
```

**Why this differs from my original implementation:** The original decompression code read the uncompressed length from the final four bytes of the GZip trailer. That value is stored modulo 2³², so it is not a reliable buffer allocation size for large content. Reading decompressed bytes into a growing `MemoryStream` avoids depending on the trailer length. The methods now also agree with the usage example: `CompressBytes` returns the compressed bytes, and `Decompress` returns the original bytes.
