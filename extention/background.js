browser.storage.local.clear()
keyCounter = 0
function setToStorage(value) {
    browser.storage.local.set({[keyCounter]: value});
    keyCounter++;
}

let notificationId = "SecSnake"
function createNotification(title, message) {
    browser.notifications.create(notificationId, {
        "type": "basic",
        "iconUrl": browser.runtime.getURL("icons/secsnake.png"),
        "eventTime": 5000,
        "title": title,
        "message": message
    });
}

function contentScriptOnMeddage(data) {
    interactionMonitoring.postMessage(data['tabURL'] + "--//*****Split*****//--" + data['data']);  // Send all documents of tabs to 'interaction_monitoring' script
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
    else if (response["status"] === "no-config") {
        createNotification("Interaction Monitoring", "No config for interaction monitoring");
    }
    else if (response["status"] === "find-attack") {
        setToStorage({title: response["title"], message: response["message"], contextMessage: response["contextMessage"]});
    }
}

function blockRequest(requestDetails) {
    for (let i = 0; i < conditions.length; i++) {

        let condition = conditions[i]
        var block = true

        if ("type" in condition) {
            for (let t of condition.type)
                block &= t === requestDetails.type;
        }

        if ("method" in condition) {
            for (let m of condition.method)
                 block &= m === requestDetails.method;
        }

        if ("url" in condition) {
            var URL = requestDetails.url
            if (condition.decode_url)
                URL = decodeURIComponent(requestDetails.url);

            if ("data" in condition.url)
                block &= condition.url.data === URL;

            if ("regexp" in condition.url) {
                let reg = new RegExp(URL);
                block &= reg.test(requestDetails.url);
            }
        }

        if ("document_url"in condition) {
            if (condition.document_url)
                block &= condition.document_url !== requestDetails.url;
        }

        if ("origin_url"in condition) {
            if (condition.origin_url)
                block &= condition.origin_url !== requestDetails.url;
        }

        if ("main_frame"in condition) {
            if (condition.main_frame)
                block &= condition.main_frame !== 0;
        }

        if ("parent_frame"in condition) {
            if (condition.parent_frame)
                block &= condition.parent_frame !== -1;
        }

        if (block) {
            setToStorage({title: "Request Analyzer", message: "Blocked the request", contextMessage: "URL: " + requestDetails.url});
            return {cancel: true};
        }
    }
}

function requestAnalyzeronMessage(response) {
    response = JSON.parse(response)
    if (response["status"] === "start") {
        conditions = response["data"];
        browser.webRequest.onBeforeRequest.addListener(blockRequest, {urls: ["<all_urls>"]}, ["blocking"]);
    }
    else if (response["status"] === "no-config") {
        createNotification("Request Analyzer", "No config for request analyzer");
    }
}

// --------------------------------------------- main ---------------------------------------------

var patternParser = browser.runtime.connectNative("pattern_parser");

patternParser.onMessage.addListener((response) => {
    response = JSON.parse(response);
    if (response["parsed"]){
        interactionMonitoring = browser.runtime.connectNative("interaction_monitoring");
        interactionMonitoring.onMessage.addListener(interactionMonitoringonMessage);

        requestAnalyzer = browser.runtime.connectNative("request_analyzer");
        requestAnalyzer.onMessage.addListener(requestAnalyzeronMessage);
    }
    else {
        createNotification("Error", response["error"]);
    }
});
