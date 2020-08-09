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
var attack_checker = browser.runtime.connectNative("js_attack_checker");


interaction_monitoring.onMessage.addListener((response) => {

    function sendAllDocument(){
        function infoTabs(tabs) {
      
            for (let tab of tabs) {
                if(String(tab.url).includes("about:debugging") || String(tab.url).includes("about:devtools-toolbox"))
                    continue
                browser.tabs.sendMessage(tab.id, {"rule": "document", "tabURL": tab.url});
                browser.runtime.onMessage.addListener((data) => {
                    let fileName = String((Math.random() * 10000000000000000000) + 1)
                    interaction_monitoring.postMessage(fileName + "[[!$AsdTTTT12a3sdVV)))*(888888)+" + data['tabURL'] + "[[!$asdTTTT12a3sdVV)))*(99999)+" + data['data'])
                    // app.postMessage(data)
                    attack_checker.postMessage(fileName + "[[!$AsdTTTT12a3sdVV)))*(888888)+" + data['tabURL'])
                })
            }
        }

        let tabs_query = browser.tabs.query({});
        tabs_query.then(infoTabs);
    }

    function chcker(key, value){
        if(key === "document" && value === true)
            sendAllDocument();
    }
    JSON.parse(response, chcker);
  
});


// attack_checker.onMessage.addListener((response) => {

//     function chekAllPatterns(){
//         function infoTabs(tabs) {
//             for (let tab of tabs) {
//                 console.log(tab.id)
//             }
//         }

//         let tabs_query = browser.tabs.query({});
//         tabs_query.then(infoTabs);
//     }

//     function chcker(key, value){
//         if(key === "check" && value === true)
//             chekAllPatterns();
//     }
//     JSON.parse(response, chcker);
  
// });
