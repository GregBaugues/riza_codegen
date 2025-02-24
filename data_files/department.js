/*
State of California
Version 2013.xx.xx
This file used to hold online renewal window opener javascript
*/

var appWindow;

function openRenewalApp()
{
	appWindow = window.open("https://www2.brea.ca.gov","_blank","toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=yes, width=1050, height=800");
	appWindow.focus();
}

function closeRenewalApp()
{
	appWindow.close();
}

var appWindow2;

function openTPPApp()

{
	appWindow2 = window.open("https://www2.brea.ca.gov/tpp","_blank","toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, copyhistory=yes, width=1050, height=800");
	appWindow2.focus();
}

function closeTPPApp()
{
	appWindow2.close();
}