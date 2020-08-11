browser.runtime.onMessage.addListener((rule) => {
    if(rule["rule"] === "document")
        browser.runtime.sendMessage({"data": document.documentElement.outerHTML, "tabURL": rule["tabURL"]});
        // browser.runtime.sendMessage(document.documentElement.outerHTML);
});