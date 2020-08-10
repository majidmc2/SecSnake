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

// function listener(e) {
// 	console.log("**************************************")
//   console.log("-------> The tabId   : " + e.tabId)
//   console.log("-------> The originUrl   : " + e.originUrl)
//   console.log("-------> The documentUrl : " + e.documentUrl)
//   console.log("-------> The url         : " + e.url)
//   console.log("-------> The typr        : " + e.type)
// 	console.log("**************************************")
// 	}
	
// browser.webRequest.onBeforeRequest.addListener(
// 	listener,
// 	{urls: ["<all_urls>"]},
// 	["blocking"]
// );


// ---------------------------------------------------------------------


var interaction_monitoring = browser.runtime.connectNative("interaction_monitoring");
// var attack_checker = browser.runtime.connectNative("js_attack_checker");


function contentScriptOnMeddage(data) {
    interaction_monitoring.postMessage(data['tabURL'] + "--//*****Split*****//--" + data['data']);  // Send all documents of tabs to 'interaction_monitoring' script 
    // attack_checker.postMessage(data['tabURL'] + "--//*****Split*****//--" + data['data']);
}


interaction_monitoring.onMessage.addListener((response) => {

    function sendAllDocument(){
        function infoTabs(tabs) {

            let tabsLength = 0;
            for (let tab of tabs) {
                if (tab.url.startsWith("http") && tab.title !== "Problem loading page")
                    tabsLength++;                   
            }

            interaction_monitoring.postMessage(tabsLength);  // Send length of Tabs to 'interaction_monitoring' script
            browser.runtime.onMessage.addListener(contentScriptOnMeddage);  // Add listener for get documents from content-script

            for (let tab of tabs) {
                if (tab.url.startsWith("http") && tab.title !== "Problem loading page")
                    browser.tabs.sendMessage(tab.id, {"rule": "document", "tabURL": tab.url});  // Send request for get documents from content-script
            }

        }

        let tabs_query = browser.tabs.query({status: "complete"});
        tabs_query.then(infoTabs);
    }

    if (response === "start") {
        sendAllDocument();
    }
    else if (response === "stop") {
        browser.runtime.onMessage.removeListener(contentScriptOnMeddage); // Remove listener for get documents from content-script
    }
});
