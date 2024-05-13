/******************************************************************************
BeepBeep, a runtime monitor (Javascript portion)
Copyright (C) 2008-2009 Sylvain Halle

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
******************************************************************************/

/*
 * Version: 0.9.2
 * Date:    2009-01-23
 * Author:  Sylvain Halle <sylvainjambon@sourceforge.net>
 */

/**
 * Formula to check.  Leave empty to retrieve it from default location.
 */
var m_formula = "";

/**
 * Beginning and end strings.  BeepBeep will only examine what is between these
 * delimiters and discard the rest of the SOAP messages (delimiters included).
 */
var m_beginText = "<SOAP-ENV:Body>";
var m_endText   = "</SOAP-ENV:Body>";

/**
 * Basic properties
 */
var m_invisibleMonitor = false;                   // Whether the monitor is CSS-invisible
var m_defaultContract = "beepbeep-contract.txt";  // Default contract file
var m_monitorWidth = 96;                          // Monitor applet width (px)
var m_monitorHeight = 16;                         // Monitor applet height (px)
var m_url = "";                                   // Remember calling URL

/**
 * Adds a handler for when the page is loaded.
 * This handler will automatically add an element into the page
 * containing the monitor applet (WatcherApplet).
 */
window.onload = function()
{
  // Gets formula
  if (m_formula == null || m_formula == "")
    m_formula = htmlentities(sync_get_file(m_defaultContract));
  // Adds monitor
  el = document.createElement("div");
  el.setAttribute("id","monitor-enclosing");
  if (m_invisibleMonitor)
    style = "display:inline;width:0px;height:0px;";
  else
    style = "display:block;width:" + m_monitorWidth + "px;height:" + m_monitorHeight + "px;";
  el.innerHTML = "<!-- Automatically added runtime monitor -->\n"
    + "<object style=\"" + style + "\" type=\"application/x-java-applet;version=1.6\" name=\"mymonitor\" id=\"mymonitor\">\n"
    + "<param name=\"archive\" value=\"beepbeep.jar\">\n"
    + "<param name=\"code\" value=\"BeepBeepMonitor\">\n"
    + "<param name=\"mayscript\" value=\"yes\">\n"
    + "<param name=\"scriptable\" value=\"true\">\n"
    + "<param name=\"formula\" value=\"" + htmlentities(m_formula) + "\">\n"
    + "<param name=\"name\" value=\"BeepBeepMonitor\">\n"
    + "</object>\n";
  window.document.body.appendChild(el);
};

/**
 * New implementation (wrapper) of the XMLHttpRequest.
 * The original wrapper, assumed to be public domain, was taken from
 * http://www.generation-nt.com/reponses/tutoriel-sur-xml-http-request-entraide-5155.html
 * and modified.
 */
function XMLHttpRequestBEEP()
{
// Because it's a wrapper, we'll make a clear distinction in code
// between the wrapper (public) and the object being wrapped (private)

var _private = null;

// This will hold a calback function in the event of contract violations
var beepbeepcallback = null;

if (window.XMLHttpRequest)
  _private = new XMLHttpRequest();
else
if (window.ActiveXObject) 
{
  try {
    _private = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e)
  {
    try {
      _private = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (e) {}
  }
}


//var _private = new ActiveXObject(LIB + ".XMLHTTP");
var _public = this;

// Default property values
var _defaults =
{
  readyState: 0,
  responseXML: null,
  responseText: "",
  status: 0,
  statusText: ""
};
// Update property values
function update()
{
  for (var i in _defaults)
  {
    try
    {
      _public[i] = (typeof _private[i] == "unknown") ? _defaults[i] : _private[i];
    }
    catch (err)
    {
      // Do nothing.  This is here only to work around a FF bug that creates a
      // "Component returned failure code: 0x80040111 (NS_ERROR_NOT_AVAILABLE)"
    }
  }
};

/**
 * Wraps XMLHttpRequest's "onreadystatechage" property
 * with a function that first intercepts the message
 */
_private.onreadystatechange = function() {
  // refresh properties
  update();
  if(_private.readyState == 4 && _private.status == 200) 
  {
    // A message has been received, send to monitor first
    if (!updateMonitors(_private.responseText))
        return; // Blocks message if violation found
  }
  // call the public event handler (if it's set)
  if (typeof _public.onreadystatechange == "function") {
    _public.onreadystatechange();
  }
};

/**
 * Overrides the original XMLHttpRequest send method with a new one
 * intercepting message contents and sending them to the runtime monitor.
 */
_public.send = function(body, dontsend) 
{
  var message = "";
  // A message has been sent; send to monitor first
  if (body != null)
  {
    // This is a SOAP call; the content is in the body
    message = body;
  }
  else
  {
    // This is a REST call; the content is in the URL
    message = makeMessage(m_url);
  }
  // Update monitors with content
  if (!updateMonitors(message))
    return;
  // The message passed the monitor; send content as before
  if (!dontsend)
    _private.send(body);
};

// Rest of the public interface:  untouched

_public.abort = function()
{
  _private.abort();
};

_public.getAllResponseHeaders = function()
{
  return _private.getAllResponseHeaders();
};

_public.getResponseHeader = function(header) 
{
  return _private.getResponseHeader(header);
};

_public.openRequest = function(method, url, async, user, password)
{
  if (url != "")
  {
    m_url = url;
    _private.open(method, url, async, user, password);
  }
};

_public.open = _public.openRequest;

_public.setRequestHeader = function(header, value)
{
  _private.setRequestHeader(header, value);
};

/**
 * Updates the state of the monitors for a new messages.  Returns true
 * if no violation was detected (or if no monitor was found), false
 * otherwise.
 */
function updateMonitors(message)
{
  var results = Array();
  if (!window.document.mymonitor)
    return true;
  if (!message)
    return true;
  // Trims the message of unwanted parts
  var processedMessage = message;
  var beginIndex = processedMessage.indexOf(m_beginText);
  if (beginIndex >= 0)
  {
    beginIndex += m_beginText.length;
    var endIndex = processedMessage.indexOf(m_endText);
    if (endIndex == -1)
      endIndex = processedMessage.length;
    processedMessage = processedMessage.substr(beginIndex,
      endIndex - beginIndex);
  }
  // The "" is required to convert from Java to JS string
  var s = window.document.mymonitor.eatMessage(processedMessage) + "";
  var results = s.split("/");
  var new_violation = false;
  var message = "";
  var indices = new Array();
  var captions = new Array();
  // Checks whether any monitor returned a NEW violation
  for (var i in results)
  {
    if (results[i] == "F")
    {
      new_violation = true;
      var caption = window.document.mymonitor.getCaption(i);
      if (beepbeepcallback)
        // If a callback function is registered, adds arguments
      {
        indices.push(i);
        captions.push(caption);
      }
      else
      {
        // Otherwise, just add a message to a popup
        message += (message == "" ? "" : "\n\n") + "The property " +
          (parseInt(i) + 1) + " has been violated" +
            (caption == "" ? "." : ": " + caption);
      }
    }
  }
  if (new_violation)
  {
    if (beepbeepcallback)
      // If callback registered, call it with arguments
      beepbeepcallback(indices, captions);
    else
      // Otherwise, show popup
      alert(message);
    return false;
  }
  return true;
}

// initialise attributes
update();
};

XMLHttpRequest.prototype = {
  toString: function() {return "[object XMLHttpRequest]"},
  // not supported
  overrideMimeType: new Function,
  channel: null
};

function DOMParser()
{
  /* empty constructor */
};

DOMParser.prototype = 
{
  toString: function() {return "[object DOMParser]"},
  parseFromString: function(str, contentType)
  {
    var xmlDocument = new ActiveXObject("Microsoft.XMLDOM");
    xmlDocument.loadXML(str);
    return xmlDocument;
  },
  // not supported
  parseFromStream: new Function,
  baseURI: ""
};

function XMLSerializer() 
{
  /* empty constructor */
};

XMLSerializer.prototype =
{
  toString: function() {return "[object XMLSerializer]"},
  serializeToString: function(root)
  {
    return root.xml || root.outerHTML;
  },
  // not supported
  serializeToStream: new Function
};

/**
 * Replaces basic HTML entities in a string
 */
function htmlentities(wText)
{
  if(typeof(wText)!="string")
  wText=wText.toString();
  wText=wText.replace(/&/g, "&amp;") ; // Must be the first
  wText=wText.replace(/"/g, "&quot;");
  wText=wText.replace(/</g, "&lt;") ;
  wText=wText.replace(/>/g, "&gt;") ;
  wText=wText.replace(/'/g, "&#146;") ;
  wText=wText.replace(/\n/g, "&xD;");
  wText=wText.replace(/\r/g, "&xA;");
  return wText;
};

/**
 * Retrieves a contract from a location
 */
function sync_get_file(location)
{
  var req;
  if (window.XMLHttpRequest)
    req = new XMLHttpRequest();
  else if (window.ActiveXObject) {
    try {
      req = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e)
    {
      try {
        req = new ActiveXObject("Microsoft.XMLHTTP");
      } catch (e) {}
    }
  }
  req.open("GET", location, false);
  req.send(null);
  return req.responseText;
};

/**
 * Creates a (flat) XML message from a REST URL.
 * For example, mypage.html?p1=a&p2=b&p2=c becomes
 * <message>
 *  <p1>a</p1>
 *  <p2>b</p2>
 *  <p2>c</p2>
 * </message>
 */
function makeMessage(url)
{
  var message = "<message>\n";
  var parts = url.split("?");
  var arg_part = parts[1];
  var arguments = arg_part.split("&");
  for (i in arguments)
  {
    var arg_pair = arguments[i];
    tuple = arg_pair.split("=");
    message = message + "<" + tuple[0] + ">" + tuple[1] + "</" + tuple[0] + ">\n";
  }
  message = message + "</message>";
  return message;
}
