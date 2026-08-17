---
title: "Understanding .NET Reference Types and Value Types"
date: "2009-03-20"
description: "I have been developing in .NET now for about 4 years and while I have visited this topic many times I have not always fully understood things. Dealing with Value Types is really straight forward however when we start to…"
tags: []
slug: "understanding-net-reference-types-and-value-types"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/03/20/Understanding-NET-Reference-Types-and-Value-Types"
permalink: "/post/2009/03/20/Understanding-NET-Reference-Types-and-Value-Types"
legacyPaths: ["/post/2009/03/20/Understanding-NET-Reference-Types-and-Value-Types"]
---
I have been developing in .NET now for about 4 years and while I have visited this topic many times I have not always fully understood things. Dealing with Value Types is really straight forward however when we start to get into Reference Types things become a bit clouded. Well I have recently been forced to try and explain them to someone else and so I decided it was time to make sure I fully understand things. So this is my attempt to provide based on things I have read and learned how things work.

 I will start by simply making some statements that will later help us understand things.

**Value Types** - Stored on the stack. When you declare a variable based on a value type, the CLR allocates memory for the value type instance wherever the variables is declared.

**Reference Types** - Variable declared is stored on the stack. When you declare a reference type, the CLR allocates memory for instance on the heap.

**Reference Types with Value Types:** When declaring inside a reference type a field that is a value type it is important to note that the memory is allocated inside the hosted object.

-----------     ------------
-  stack  -     -  heap    -
-----------     ------------
-  var1   -     -  Class1  -
-----------     - Instance -
-   10    -     ------------
-----------           ^
-  var2   -           |
-----------           |
-   ref   - -----------
-----------

**Strings** - It is important to point out that strings are immutable. When making changes to a string you are actually creating a new instance of that string. You will see in the examples below that they behave a little different when making changes to them as opposed to making changes to a field in a Class.

**Memory Cleanup:**

- **Value Types** - When a value type goes out of scope the memory is immediatly removed from the stack.
- **Reference Types** - When a reference type goes out of scope the variable is immediatly removed from the stack. However the memory allocated on the heap still exists and the removal is managed by the Memory Manager and Garbage Collector process.

**Methods:** Passing arguments to methods ByValue and ByReference When you declare a method you by default pass in the argument ByValue. However the behaviour giving this statement is not always as expected when dealing with reference types. Here are some scenarios.

- **Value Type being passed ByValue:** Remember that a value type holds the data itself. When passing in ByValue a copy of the actual data is passed. The method now contains its own variable and data and so the result is that the original variable will not change as changes are made to the new variable inside the method.
- **Value Type being passed ByReference:** When passing in a value type ByReference we are actually passing a reference is created that points to the data. The result is that any changes made to the variable inside the scope of the method are reflected back to the external variable.
- **Reference Type being passed ByValue:** When you pass in a reference type ByValue you get a bit  different behaviour. Remember that the value is always on the heap, so you are actually pointing the new variable to the same memory location as the original variable. Thus when making changes to the variable changes are reflected to the original variable. So if you need to pass a reference type and not have changes reflected you need to make sure you create a full new copy of the object being passed in.
- **Reference Type being passed ByReference:** This last situation you most likely want to avoid. This basically ends up creating a reference variable that points to the reference variable that points to the data. So a reference to a reference. While I said you usually should avoid this it is worth pointing out why you might want to use this approach. Remember that in the  previous Reference ByValue changes are reflected back to the original variable. However if you make any changes to the object itself, for example set the object to NULL or set it to a NEW object then the changes would not be reflected outside as your internal variable now points to a new memory location. So if you need to have NEW or NULL changes reflected back outside you could pass it in ByRef.

Below you will find some examples that will help see how value types and refernce types differ when making changes to them and how the behaviour changes when passing them into methods.

**STRING TEST - Reference Type - Immutable**
Creating two strings. Setting the first to the value "one-before" and then initializing the second variable by pointing it to the first. Writing out the initial values so that we can see that each is now set to "one-before". So at this point what we have in effect is to variables declared on the stack one and two that both point to the same memory location which holds "one-before". Then we come along and we set one = "one-after" and since strings are immutable a new memory locations is allocated and one is now pointed to the new memory location. However two still remains pointed to the previous memory location so the result is that they now have different values.

**//Begin Test**string one = "one-before";
string two = one;

Console.WriteLine(one); //Output = one-before
Console.WriteLine(two); //Output = one-before

one = "one-after";

Console.WriteLine(one); //Output = one-after
Console.WriteLine(two); //Output = one-before
**// End Test**

**INTEGER TEST - Value Type**
Creating two integers. Setting the first to the value 1 and then initializing the second variable by pointing it to the first. Writing out the initial values we see that both variables have the same value of 1. The next thing we do is change the value or i = 2. Then we write out the values of the variables and see that i = 2 but j = 1. The reason for this is that value types when assigned a value contain the actual data. So when we created j = i we got a copy of the actual data that i contained and j now has its own data. So when we come along later and make a change to i we are only changing its information and j will still reflect the information it holds.

**// Begin Test**
int i = 1;
int j = i;

Console.WriteLine(i); // Output = 1
Console.WriteLine(j); // Output = 1

i = 2;

Console.WriteLine(i); // Output = 2
Console.WriteLine(j); // Output = 1
**// End Test**

**To be continued.** Will be adding tests for passing into methods Structure (ValueType) and Class (ReferenceType)
