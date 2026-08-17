---
title: "Calling ASMX .net Web Service using jQuery"
date: "2009-05-22"
description: "Just started to pick up jquery recently and was playing with calling a .net web service from my page. Was really easy once I used Firefox Firebug to do my debugging and figure out some of the variable names to use to ac…"
tags: []
slug: "calling-asmx-net-web-service-using-jquery"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2009/05/22/Calling-ASMX-net-Web-Service-using-JQuery"
permalink: "/post/2009/05/22/Calling-ASMX-net-Web-Service-using-JQuery"
legacyPaths: ["/post/2009/05/22/Calling-ASMX-net-Web-Service-using-JQuery"]
---
Just started to pick up jquery recently and was playing with calling a .net web service from my page. Was really easy once I used Firefox Firebug to do my debugging and figure out some of the variable names to use to access my data.

Here is my final code

Javascript in page

```xml
<script type=
"text/javascript"
>
    $(document).ready(
function
() {
    $.ajax({
            type:
"POST"
,
            url:
"default.asmx/GetCatalog"
,
            cache:
false
,
            contentType:
"application/json; charset=utf-8"
,
            data:
"{}"
,
            dataType:
"json"
,
            success: handleSuccess,
            error: handleError
        });
    });

function
 handleSuccess(data, status) {

for
 (
var
 count
in
 data.d) {
            $(
'#bookTitles'
).html(

' <strong>Book:</strong> '
 + data.d[count].BookName +

'    <strong>Author:</strong> '
 + data.d[count].Author +

' <br />'
);
        }

    }

function
 handleError(xmlRequest) {
        alert(xmlRequest.status +
' \n\r '
        + xmlRequest.statusText +
'\n\r'

        + xmlRequest.responseText);
    }
</script>
```

and the div that I write the content to

```xml
<
body
>

<
b
>
Books List
</
b
>

<
div

id
="bookTitles"
>

</
div
>
</
body
>
```

and my Web Service and Class Catalog

```
[WebMethod]
public
 Catalog[] GetCatalog()
{
    Catalog[] catalog =
new
 Catalog[1];
    Catalog cat =
new
 Catalog();
    cat.Author =
"Jim"
;
    cat.BookName =
"His Book"
;
    catalog.SetValue(cat, 0);

return
 catalog;

}
public

class
 Catalog
{

public

string
 Author;

public

string
 BookName;
}
```
