---

title: "Fix error:  Failed to generate a user instance of SQL Server due to a failure in starting the process for the user instance."
date: "2011-05-25"
description: "For anyone using Visual Studio and trying to add a SQL Database File and getting the error: \"Failed to generate a user instance of SQL Server due to a failure in starting the process for the…"
tags: ["SQL", "Visual Studio"]
slug: "fix-error-failed-to-generate-a-user-instance-of-sql-server-due-to-a-failure-in-starting-the-process-for-the-user-instance"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2011/05/25/Fix-error-Failed-to-generate-a-user-instance-of-SQL-Server-due-to-a-failure-in-starting-the-process-for-the-user-instance"
permalink: "/post/2011/05/25/Fix-error-Failed-to-generate-a-user-instance-of-SQL-Server-due-to-a-failure-in-starting-the-process-for-the-user-instance"
legacyPaths: ["/post/2011/05/25/Fix-error-Failed-to-generate-a-user-instance-of-SQL-Server-due-to-a-failure-in-starting-the-process-for-the-user-instance"]
---
For anyone using Visual Studio and trying to add a SQL Database File and getting the error: "Failed to generate a user instance of SQL Server due to a failure in starting the process for the user instance." you might want to give the following steps a try.

Make sure you have enabled user instances. Open SQL Server Management Studio and connect to .\SQLEXPRESS

Run the following query

exec sp\_configure 'user instances enabled', 1
go
reconfigure

Now restart SQL

Now you must delete the files that SQLExpress creates when adding instances if they already exist.

Go to your Local Settings folder.

Windows 7: C:\Users\YOUR\_USERNAME\AppData\Local\Microsoft\Microsoft SQL Server Data\SQLEXPRESS

Windows XP: C:\Documents and Settings\YOUR\_USERNAME\Local Settings\Application Data\Microsoft\Microsoft SQL Server Data\SQLEXPRESS

Delete all files in the above folder

Hopefully if the above worked you will now be able to create databases inside VS with no issue.
