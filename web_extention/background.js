// var port = browser.runtime.connectNative("secsnake_client");
// var cont = 0

// function logURL(requestDetails) {
// 	console.log("Loading: " + requestDetails.url);

// 	port.postMessage("Ping");

// 	port.onMessage.addListener((response) => {
// 		console.log("Received: " + response);
// 	});

// 	console.log("Counter of URLs: " + cont);
// 	cont ++;

// }

function showTab(event) {
	// event is same to 'event' in 'JS Handler Function'!!!
	// console.log("--------> Loading: " + event.url + " frameID: " + event.frameId);
	// console.log("------>frameID: " + JSON.stringify(event));
	// console.log("------>frameID: " + event.frameId + " --- "+ event.parentFrameId + " --- "+ event.type);
	console.log("------>frameID: " + event);
}

browser.webRequest.onBeforeSendHeaders.addListener(
	showTab,
	{urls: ["<all_urls>"]}, //, tabId: 9}, // This is a filter and has not 'event' in Handler Function!!!
	["blocking"]
);


// function rewriteUserAgentHeader(e) {
// 	console.log("-------> The URL: " + e.originUrl)
// 	for (var header of e.requestHeaders) {
// 		console.log("-------> Header Fileds: " + header.name + " = " + header.value);
// 	}
// 	console.log("----------------");
//   }
  
//   browser.webRequest.onBeforeSendHeaders.addListener(rewriteUserAgentHeader,
// 											{urls: ["<all_urls>"]},
// 											["blocking", "requestHeaders"]);
