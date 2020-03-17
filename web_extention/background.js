var port = browser.runtime.connectNative("secsnake_client");
var cont = 0

function logURL(requestDetails) {
	console.log("Loading: " + requestDetails.url);

	port.postMessage("Ping");

	port.onMessage.addListener((response) => {
		console.log("Received: " + response);
	});

	console.log("Counter of URLs: " + cont);
	cont ++;


}

browser.webRequest.onBeforeRequest.addListener(
	logURL,
	{urls: ["<all_urls>"]}
);
