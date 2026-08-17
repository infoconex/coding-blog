---
title: "ASP.NET CustomValidator that validates multiple controls using both Server Side and Client Side scripting"
date: "2010-10-11"
description: "ASP.NET has some nice validation controls built in that can help make validating forms much easier. Listed below are a few of the available controls."
tags: []
slug: "asp-net-customvalidator-that-validates-multiple-controls-using-both-server-side-and-client-side-scripting"
author: "Jim Scott"
originalUrl: "http://coding.infoconex.com/post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting"
permalink: "/post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting"
legacyPaths: ["/post/2010/10/11/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting"]
---
ASP.NET has some nice validation controls built in that can help make validating forms much easier. Listed below are a few of the available controls.

[RequiredFieldValidator](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.requiredfieldvalidator.aspx) – Ensures that the user does not skip a field that has some requirement for being selected or filled out.

[CompareValidator](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.comparevalidator.aspx) - Compares a user's entry against a constant value, against the value of another control (using a comparison operator such as less than, equal, or greater than), or for a specific data type.

[RangeValidator](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.rangevalidator.aspx) - Checks that a user's entry is between specified lower and upper boundaries. You can check ranges within pairs of numbers, alphabetic characters, and dates.

[RegularExpressionValidator](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.regularexpressionvalidator.aspx) - Checks that the entry matches a pattern defined by a regular expression. This type of validation enables you to check for predictable sequences of characters, such as those in e-mail addresses, telephone numbers, postal codes, and so on.

All the above controls have you specify the [ControlToValidate](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.basevalidator.controltovalidate.aspx) which can be any one of these types: [DropDownList](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.dropdownlist.aspx), [FileUpload](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.fileupload.aspx), [ListBox](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.listbox.aspx), [RadioButtonList](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.radiobuttonlist.aspx), [TextBox](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.textbox.aspx), [HtmlInputFile](http://msdn.microsoft.com/en-us/library/system.web.ui.htmlcontrols.htmlinputfile.aspx), [HtmlInputPassword](http://msdn.microsoft.com/en-us/library/system.web.ui.htmlcontrols.htmlinputpassword.aspx), [HtmlInputText](http://msdn.microsoft.com/en-us/library/system.web.ui.htmlcontrols.htmlinputtext.aspx), [HtmlSelect](http://msdn.microsoft.com/en-us/library/system.web.ui.htmlcontrols.htmlselect.aspx) and [HtmlTextArea](http://msdn.microsoft.com/en-us/library/system.web.ui.htmlcontrols.htmltextarea.aspx)

But what if you want to perform validation against a control type not listed or on multiple controls? Have no fear as the  [CustomValidator](http://msdn.microsoft.com/en-us/library/system.web.ui.webcontrols.customvalidator.aspx) control allows you to write your own server side and client side validation logic and get as complex as you want.

All of the previously mentioned controls require you to specify the control you want to validate via the poperty ControlTValidate, however with CustomValidator you can leave it blank which then leaves you to specify logic server side and client side to perform any validation you like.

So let’s take this to the real world. Recently I was faced a scenario that could not be handled by the standard set of validation controls.

Example) A series of 5 independent checkbox controls and at least one of them was required to be checked. Plus if Other is selected then you must fill in the textbox.

[![image](images/image-thumb-5.png "image")](images/image-5.png)

So the behavior should be that you must select at least one checkbox and if none selected then you will get an error “You must select at least one checkbox” and if the Other checkbox is selected then they must also supply text in the texbox field.

Here is a snippet from the ASPX source showing the controls and the CustomValidator

Code Snippet

```xml
Please select the skill's you have:

<asp:CheckBox ID="checkBoxCSharp" runat="server" Text="C#" />

<asp:CheckBox ID="checkBoxASPNET" runat="server" Text="ASP.NET" />

<asp:CheckBox ID="checkBoxJavascript" runat="server" Text="Javascript" />

<asp:CheckBox ID="checkBoxHtml" runat="server" Text="Html" />

<asp:CheckBox ID="checkBoxOther" runat="server" Text="Other" />
&nbsp;
<asp:TextBox ID="textBoxOther" runat="server" />


<asp:Button ID="buttonSubmit" runat="server" Text="Submit" />
<asp:CustomValidator
ID="CustomValidatorSkillsYouHave"
runat="server"
ErrorMessage="You must select at least one skill"
ForeColor="Red"
OnServerValidate="CustomValidatorSkillsYouHave_ServerValidate" />
```

Notice that we do not have specified ControlToValidate. As well we have defined a OnServerValidate method that will get called when the page is posted back to the server.

Here is the server side method

Code Snippet

```csharp
protected void CustomValidatorSkillsYouHave_ServerValidate(
object source, ServerValidateEventArgs args)
{
if (!this.checkBoxASPNET.Checked &&
!this.checkBoxCSharp.Checked &&
!this.checkBoxHtml.Checked &&
!this.checkBoxJavascript.Checked &&
!this.checkBoxOther.Checked)
{
args.IsValid = false;
}
else if (this.checkBoxOther.Checked &&
string.IsNullOrEmpty(this.textBoxOther.Text.Trim()))
{
((CustomValidator)source)
.ErrorMessage = @"You must supply a text
description when selecting other";
args.IsValid = false;
}
}
```

In this method we check to see if at least one checkbox was checked and if not set the args.IsValid = false which will cause the validator to fail. If the first test is passed we check to see if the Other checkbox is checked and if so ensure that the texbox was filled out. If not then we set args.IsValid = false but we also change the error message to provide a better description of the failure.

However the above only happens when posted back to the server. We also want to provide some client side validation in order to prevent a post back to the server if the same type of validation fails on the client side.

To do this we specify the **ClientValidationFunction** property on the CustomValidator to point to our JavaScript function to perform the client side validation. In this case I created a JavaScript function called **IsSkillsYouHaveValid** as shown below.

Code Snippet

```javascript
<script type="text/javascript">
function IsSkillsYouHaveValid(source, args) {
var checkBoxCSharp = document.getElementById('checkBoxCSharp');
var checkBoxASPNET = document.getElementById('checkBoxASPNET');
var checkBoxJavascript = document.getElementById('checkBoxJavascript');
var checkBoxHtml = document.getElementById('checkBoxHtml');
var checkBoxOther = document.getElementById('checkBoxOther');
var textBoxOther = document.getElementById('textBoxOther');
if (!checkBoxASPNET.checked &&
!checkBoxCSharp.checked &&
!checkBoxHtml.checked &&
!checkBoxJavascript.checked &&
!checkBoxOther.checked) {
args.IsValid = false;
}
else if (checkBoxOther.checked &&
textBoxOther.value == "") {
source.innerText = 'You must supply a text ' +
'description when selecting other';
args.IsValid = false;
}
}
</script>
```

So with this extra bit of client side code we will now perform client side validation that if failed will prevent the page from being posted back to the server, thus avoiding an unnecessary round-trip.

BUT we are not done yet. I am picky and one of the things I don’t like about the following solution so far is that when you correct the validation failure by for instance selecting at least one checkbox or by filling out the textbox if you have selected Other is that the error message still appears until you click the submit button. I want the user to immediately know once they have correct the issue that they have satisfied the validation.

To do this we need to add one more method. This method will be responsible revalidating to see if the validation passes if any change happens to one of the controls we are validating.

Code Snippet

```javascript
function ValidateSkillsYouHave() {
var customValidator = document.getElementById('CustomValidatorSkillsYouHave');
var checkBoxCSharp = document.getElementById('checkBoxCSharp');
var checkBoxASPNET = document.getElementById('checkBoxASPNET');
var checkBoxJavascript = document.getElementById('checkBoxJavascript');
var checkBoxHtml = document.getElementById('checkBoxHtml');
var checkBoxOther = document.getElementById('checkBoxOther');
var textBoxOther = document.getElementById('textBoxOther');
if (!checkBoxASPNET.checked &&
!checkBoxCSharp.checked &&
!checkBoxHtml.checked &&
!checkBoxJavascript.checked &&
!checkBoxOther.checked &&
!checkBoxOther.checked) {
customValidator.isvalid = false;
customValidator.style.visibility = "visible";
}
else if (checkBoxOther.checked &&
textBoxOther.value == "") {
customValidator.innerText = 'You must supply a text ' +
'description when selecting other';
customValidator.isvalid = false;
customValidator.style.visibility = "visible";
}
else {
customValidator.isvalid = true;
customValidator.style.visibility = "hidden";
}
}
```

Now when we submit the form and the validation fails and the user goes and selects at least one checkbox then the validation will be re-evaluated and immediately update the display to remove the validation error when it passes.

I know this was a bit of extra work but when you have a big form and you have implemented RequiredFieldValidators etc.. in which the error message goes away when you fill in the field but your custom validators do not it starts to stand out and the extra little bit of work provides a better end user experience.

Now much of the Javascript code written about could have been done much easier using [JQuery](http://jquery.com/) and no guarantee the javascript written is cross browse safe. I used IE8 in all my testing and would personally recommend implementing a Javascript library like JQuery that abstracts the browser differences out. However I wanted to keep it simple without adding the need to explain the JQuery syntax.

Click on the download link to download a copy of the full source for this article [Download Source](http://coding.infoconex.com/file.axd?file=validation-source.zip)

[![kick it on DotNetKicks.com](http://dotnetkicks.com/Services/Images/KickItImageGenerator.ashx?url=http://coding.infoconex.com/post/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting.aspx)](http://www.dotnetkicks.com/kick/?url=http://coding.infoconex.com/post/ASPNET-CustomValidator-that-validates-multiple-controls-using-both-Server-Side-and-Client-Side-scripting.aspx)
