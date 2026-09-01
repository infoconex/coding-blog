---

title: "My favorite design patterns are Strategy and Factory Method"
date: "2013-10-05"
description: "A number of years back I started my exploration into the world of design patterns and read an incredible book “ Design Patterns Explained ” that did a great job in getting me started on a path…"
tags: []
slug: "my-favorite-design-patterns-are-strategy-and-factory-method"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2013/10/05/My-favorite-design-patterns-are-Strategy-and-Factory-Method"
permalink: "/post/2013/10/05/My-favorite-design-patterns-are-Strategy-and-Factory-Method"
legacyPaths: ["/post/2013/10/05/My-favorite-design-patterns-are-Strategy-and-Factory-Method"]
---
A number of years back I started my exploration into the world of design patterns and read an incredible book “[Design Patterns Explained](http://www.amazon.com/gp/product/0321247140/ref=as_li_qf_sp_asin_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0321247140&linkCode=as2&tag=codblo-20 "Design Patterns Explained")” that did a great job in getting me started on a path that would ultimately change the way I developed code forever.

As I learned more about design patterns I began to see that in many cases I was already using some of those patterns. When I finished with the book I was armed with knowing about design patterns but was not exactly sure how some of those patterns would be put into practice. I knew the only way I was going to actually use these patterns was to writing code and attempting to use the patterns I had learned.

Jump forward a few years now and the two patterns that I see used the most in my software projects are the [Strategy Pattern](http://en.wikipedia.org/wiki/Strategy_pattern) part of the [Behavioral Pattern family](http://en.wikipedia.org/wiki/Behavioral_pattern) and [Factory Method Pattern](http://en.wikipedia.org/wiki/Factory_method_pattern) part of the [Creational Pattern family](http://en.wikipedia.org/wiki/Creational_pattern).  When I typically use these two patterns they are almost always used together, the strategy pattern for implementing different behaviors that my application will use and the factory method pattern to encapsulate the logic required for deciding which concrete implementation of the strategy will be used.

In order to demonstrate the use of these patterns I am going to create a simple application that I may have typically written in the past that could benefit from these two patterns. Unfortunately when I was learning about many of the patterns what was never really clear was when a pattern might typically be used to improve the code I was currently writing. I hope that by the end of the article you will see for at least these two patterns how you might be able to implement these patterns.

**Application Requirements**

You will be building a simple console application that will be used to check to see if a website is up. The console application will initially be run manually by an individual responsible for making sure that the various websites are up and responding. The application must be able to check the content of the returned HTML for a given string to ensure that the content retrieved is returning the expected information. The application must take the following pieces of information as input (website address, content to look for) and then return the word SUCCESS if it found the content and ERROR followed by another line indicating the reason the test failed. The application should also write out the steps that it is performing to provide feedback to the person running the application.

**Application V1.0** – First version written to deal with the current requirements. (Note: do not get caught up in the lack of validation of input parameters as the sample is designed to focus on the strategy pattern not best practices for writing the application as a whole.)

```csharp
using
 System;

using
 System.Net;

namespace
 Design_Patterns
{

internal

class
 Program
    {

f
(
string
[] args)
        {

// More validation would be necessary but the article is not


// about validation of input ;-)


if
 (args.Length != 2)
            {
                Console.WriteLine(
"You must supply the URL and Content to check for."
);
            }


string
 websiteUrl = args[0];

            Console.WriteLine(
"URL supplied to be validated: {0}"
, websiteUrl);


string
 contentToVerify = args[1];

            Console.WriteLine(
"Content to be verified: {0}"
, contentToVerify);

            WebClient webClient =
new
 WebClient();


try

            {
                Console.WriteLine(
"Attempting to retrieve content"
);


string
 htmlContent = webClient.DownloadString(websiteUrl);

                Console.WriteLine(
"Content downloaded, checking to see if content exists."
);


if
 (htmlContent.Contains(contentToVerify))
                {
                    Console.WriteLine(
"SUCCESS: Content supplied was found."
);
                }

else

                {
                    Console.WriteLine(
"ERROR: Content was not found in the returned html."
);
                }
            }

catch
 (Exception ex)
            {
                Console.WriteLine(
"ERROR: Exception occurred while downloading content: {0}"
, ex.Message);
            }

            Console.WriteLine(
"-- Hit enter To close application –"
);

            Console.Read();
        }
    }
}
```

**Application Results –** Running the application from a command prompt to test and see pulling down the html for [www.google.com](http://www.google.com) we could find the content “Google Search” and things worked as expected..

[![image](images/image-thumb-6.png "image")](images/image-6.png)


**Application Revision**

The application designed has meet the needs expected, however after using it for a period of time it is realized that while it is great that someone can open the application and manually verify that a website is up and returning the expected content, they would like to make the process automated instead of manually running have it run on a regular basis and then have the person responsible check periodically to see the results of the tests. It is proposed that you log the output of the results to a text file that the person will check.

**Application V1.1** – Second version to add ability to run manually or automatically and log results to a log file when automated.

```csharp
using
 System;

using
 System.IO;

using
 System.Net;

namespace
 Design_Patterns
{

internal

class
 Program
    {

private

static
 StreamWriter fileWriter =
null
;

private

static

bool
 useFileWriter =
false
;

private

const

string
 loggingFileName =
"WebsiteMonitor.log"
;


private

static

void
 Main(
string
[] args)
        {

try

            {

// More validation would be necessary but the article is not


// about validation of input ;-)


if
 (args.Length < 2)
                {
                    WriteMessage(
"You must supply the URL and Content to check for."
);
return
;
                }

// If third argument supplied then it is used to determine


// if the application will log to a file


if
 (args.Length == 3)
                {
                    useFileWriter = Convert.ToBoolean(args[2]);


if
 (useFileWriter)
                    {
                        fileWriter = File.CreateText(loggingFileName);
                    }
                }


string
 websiteUrl = args[0];

                WriteMessage(
string
.Format(
"URL supplied to be validated: {0}"
, websiteUrl));


string
 contentToVerify = args[1];

                WriteMessage(
string
.Format(
"Content to be verified: {0}"
, contentToVerify));

                WebClient webClient =
new
 WebClient();


try

                {
                    WriteMessage(
"Attempting to retrieve content"
);


string
 htmlContent = webClient.DownloadString(websiteUrl);

                    WriteMessage(
"Content downloaded, checking to see if content exists."
);


if
 (htmlContent.Contains(contentToVerify))
                    {
                        WriteMessage(
"SUCCESS: Content supplied was found."
);
                    }

else

                    {
                        WriteMessage(
"ERROR: Content was not found in the returned html."
);
                    }
                }

catch
 (Exception ex)
                {
                    WriteMessage(
string
.Format(
"ERROR: Exception occurred while downloading content: {0}"
, ex.Message));
                }

                WriteMessage(
string
.Format(
"Test completed at: {0}"
, DateTime.Now));


if
 (!useFileWriter)
                {
                    WriteMessage(
"-- Hit enter To close application --"
);

                    Console.Read();
                }
            }

finally

            {

if
 (fileWriter !=
null
) fileWriter.Dispose();
            }
        }


/// <summary>


/// Writes the message to either the console or file based on configuration


/// </summary>


/// <param name="message"></param>


private

static

void
 WriteMessage(
string
 message)
        {

if
 (!useFileWriter)
            {
                Console.WriteLine(message);
            }

else

            {
                fileWriter.WriteLine(message);
            }
        }
    }
}
```

**Application Results** - Now when you run the application manually as before you get the same output to the console. However you can also run and provide a third argument of true and the output will be written to a log file named WebsiteMonitor.log with the results. The issue with the above code is that the main method now has to be aware of how to write the message in the two different ways. You can imagine that if asked to add a third way of logging to an XML file, the main method starts to get even more complex and its responsibility of knowing about logging becomes a bit out of hand.

[![image](images/image-thumb-7.png "image")](images/image-7.png)


**Solution**

Implement the strategy pattern to deal with the various ways the application would like to implement various logging algorithms.

**Strategy Pattern**

When you look at any article that discusses the strategy pattern you will typically find a UML diagram that shows the various items that make up the pattern. The following UML diagram is an example of the strategy pattern that I will be implementing for logging messages in example code.

[![image](images/image-thumb-9.png "image")](images/image-9.png)


Let me take a minute to explain what the above UML diagram says about the logging I will be implementing.

- **Logger** – Represents the context class that will contain the logging strategy. This is the class that our client code (Program.cs main method) will use to implement logging of messages for the system. The line between the Logger and the ILogWriter with the filled diamond indicates that our Logger class will always have a ILogWriter instance. Notice also that the Logger class has a constructor that takes an ILogWriter object that you will see comes into play as we refactor the existing code.
- **ILogWriter** – Represents the logging strategy that we are implementing for the application. In this case the ILogWriter is an interface that defines that all strategy classes must implement a Write method that will be used to write the message to be logged. However the interface does not contain any implementation but rather defines the contract for any concrete class that implement the interface.
- **ConsoleWriter, XmlWriter, FileWriter** – Represents the concrete classes that will represent each of the logging algorithms that can be used by the application. The dashed lines between the concrete classes and strategy indicate that the concrete classes implement the ILogWriter interface.

**Application V1.2** – Use the strategy pattern to remove some of the complexity in the main method and remove it from being responsible for having to understand the various algorithms required for doing logging of messages.

**Create strategy** – ILogWriter interface that specific logging algorithms will use.

```csharp
namespace
 Design_Patterns
{

public

interface
 ILogWriter
    {

void
 Write(
string
 message);
    }
}
```

Create the new concrete classes that will do the logging for Console and File logging

**Console Writer** – Class that will be responsible for logging messages to the console

```csharp
using
 System;

namespace
 Design_Patterns
{

public

class
 ConsoleWriter : ILogWriter
    {

public

void
 Write(
string
 message)
        {
            Console.WriteLine(message);
        }
    }
}
```

**File Writer** – Class that will be responsible for logging messages to a file

```csharp
using
 System;

using
 System.IO;

namespace
 Design_Patterns
{

public

class
 FileWriter : ILogWriter, IDisposable
    {

private

const

string
 logFileName =
"WebsiteMonitor.log"
;

private
 StreamWriter fileWriter =
null
;


public
 FileWriter()
        {
            fileWriter = File.CreateText(logFileName);
            fileWriter.AutoFlush =
true
;
        }


public

void
 Write(
string
 message)
        {
            fileWriter.WriteLine(message);
        }


/// <summary>


/// Dispose method ensures that the file is closed and disposed


/// </summary>


public

void
 Dispose()
        {

if
 (fileWriter !=
null
) fileWriter.Dispose();
        }

    }
}
```

**Logger** – Client in strategy pattern that will contain an instance of the strategy to do the logging for the application. This class will be used inside the Program main method to do the logging for the application. The default  logger that will be used if not defined is the console logger, this allows us to implement the same behavior that the original application had without any extra configuration. You can also alternatively pass in the type of logger you wish to create or pass in a specific strategy required, this will be important when we implement the final refactoring as you will see in a bit.

```csharp
using
 System;

namespace
 Design_Patterns
{

public

class
 Logger : IDisposable
    {

private
 ILogWriter logger;


/// <summary>


/// Default constructor will implement a console writer


/// </summary>


public
 Logger()
        {
            logger =
new
 ConsoleWriter();
        }


/// <summary>


/// Initializes a new logger based on the LoggerType provided


/// </summary>


/// <param name="loggerType">LoggerType to use</param>


public
 Logger(LoggerType loggerType)
        {

switch
 (loggerType)
            {

case
 LoggerType.Console:
                    logger =
new
 ConsoleWriter();

break
;

case
 LoggerType.File:
                    logger =
new
 FileWriter();

break
;

case
 LoggerType.Xml:
                    logger =
new
 XmlWriter();

break
;

default
:

throw

new
 Exception(
"LoggerType unknown: "
 + loggerType);
            }
        }


/// <summary>


/// Logger type can be passed in


/// </summary>


/// <param name="logger">ILogWriter</param>


public
 Logger(ILogWriter logger)
        {

this
.logger = logger;
        }


/// <summary>


/// Write message to logger


/// </summary>


/// <param name="message"></param>


public

void
 Write(
string
 message)
        {
            logger.Write(message);
        }


/// <summary>


/// Dispose logger if IDisposable is implemented


/// </summary>


public

void
 Dispose()
        {

if
 (logger
is
 IDisposable && logger !=
null
)
            {
                ((IDisposable)logger).Dispose();
            }
        }
    }
}
```

**Program** – Application code that has now been refactored to use the strategy pattern. Take note that this class no longer knows anything about how to perform logging. The only thing that remains regarding logging is the code that decides what type of logger the application should use. These changes will provide an approach that will allow our application to expand and use different loggers as requirements change without having to change the logic in the main method. The program also no longer needs to know anything about how logging happens. The WriteMessage method has now been removed, the application when started looks to see if file logging is required and if so instantiates a new logger passing in that it will need to implement file logging, otherwise the default logger is initialized which will do console logging which is the same as the previous behavior.

```csharp
using
 System;

using
 System.Net;

namespace
 Design_Patterns
{

internal

class
 Program
    {

private

static

bool
 useFileWriter =
false
;


private

static

void
 Main(
string
[] args)
        {
            Logger logger =
null
;


try

            {

// If third argument supplied then it is used to determine


// if the application will log to a file


if
 (args.Length == 3)
                {
                    useFileWriter = Convert.ToBoolean(args[2]);


if
 (useFileWriter)
                    {
                        logger =
new
 Logger(LoggerType.File);
                    }
                }


if
 (logger ==
null
)
                {
                    logger =
new
 Logger();
                }


// More validation would be necessary but the article is not


// about validation of input ;-)


if
 (args.Length < 2)
                {
                    logger.Write(
"You must supply the URL and Content to check for."
);


return
;
                }


string
 websiteUrl = args[0];

                logger.Write(
string
.Format(
"URL supplied to be validated: {0}"
, websiteUrl));


string
 contentToVerify = args[1];

                logger.Write(
string
.Format(
"Content to be verified: {0}"
, contentToVerify));

                WebClient webClient =
new
 WebClient();


try

                {
                    logger.Write(
"Attempting to retrieve content"
);


string
 htmlContent = webClient.DownloadString(websiteUrl);

                    logger.Write(
"Content downloaded, checking to see if content exists."
);


if
 (htmlContent.Contains(contentToVerify))
                    {
                        logger.Write(
"SUCCESS: Content supplied was found."
);
                    }

else

                    {
                        logger.Write(
"ERROR: Content was not found in the returned html."
);
                    }
                }

catch
 (Exception ex)
                {
                    logger.Write(
string
.Format(
"ERROR: Exception occurred while downloading content: {0}"
, ex.Message));
                }

                logger.Write(
string
.Format(
"Test completed at: {0}"
, DateTime.Now));


if
 (!useFileWriter)
                {
                    logger.Write(
"-- Hit enter To close application --"
);

                    Console.Read();
                }
            }

finally

            {

if
 (logger !=
null
) logger.Dispose();
            }
        }
    }
}
```

Our application however still needs to know a bit about how to create an instance of the Logger class and the various strategy classes, to solve this issue we are going to implement the Factory Method pattern which will be responsible for creating new instances. This will help when we decide to have some of our concrete strategy classes get more complex which could make our Logger class complex in understanding how to create the various instances in our switch statement. If you see the new statement used someplace it is probably a good indicator that a factory method pattern could be used. This article is getting a bit longer than I expected so I am going to do the next pattern in a part 2 article.

Stay Tuned!
