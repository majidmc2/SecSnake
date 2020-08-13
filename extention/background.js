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

let notificationId = "SecSnake"
function createNotification(title, message, contextMessage="") {
    browser.notifications.create(notificationId, {
        "type": "basic",
        "iconUrl": browser.runtime.getURL("icons/secsnake.png"),
        "eventTime": 5000,
        "title": title,
        "message": message,
        "contextMessage": contextMessage
    });
}


function contentScriptOnMeddage(data) {
    interactionMonitoring.postMessage(data['tabURL'] + "--//*****Split*****//--" + data['data']);  // Send all documents of tabs to 'interaction_monitoring' script
    // attack_checker.postMessage(data['tabURL'] + "--//*****Split*****//--" + data['data']);
}

function interactionMonitoringonMessage(response) {
    function sendAllDocument(){
        function infoTabs(tabs) {

            let tabsLength = 0;
            for (let tab of tabs) {
                if (tab.url.startsWith("http") && tab.title !== "Problem loading page")
                    tabsLength++;
            }

            interactionMonitoring.postMessage(tabsLength);  // Send length of Tabs to 'interaction_monitoring' script
            browser.runtime.onMessage.addListener(contentScriptOnMeddage);  // Add listener for get documents from content-script

            for (let tab of tabs) {
                if (tab.url.startsWith("http") && tab.title !== "Problem loading page")
                    browser.tabs.sendMessage(tab.id, {"rule": "document", "tabURL": tab.url});  // Send request for get documents from content-script
            }

        }

        let tabs_query = browser.tabs.query({status: "complete"});
        tabs_query.then(infoTabs);
    }

    response = JSON.parse(response)
    if (response["status"] === "start") {
        sendAllDocument();
    }
    else if (response["status"] === "stop") {
        browser.runtime.onMessage.removeListener(contentScriptOnMeddage); // Remove listener for get documents from content-script
    }
    else if (response["status"] === "config") {
        console.log("config")
    }
    else if (response["status"] === "no-config") {
        console.log("no-config")
        // TODO:createNotification or in ui
    }
}


var patternParser = browser.runtime.connectNative("pattern_parser");

patternParser.onMessage.addListener((response) => {
    response = JSON.parse(response)
    if (response["parsed"]){
        interactionMonitoring = browser.runtime.connectNative("interaction_monitoring");
        interactionMonitoring.onMessage.addListener(interactionMonitoringonMessage);
    }
    else {
        createNotification("Error", response["error"])
        // TODO: Send message to UI
    }
});
