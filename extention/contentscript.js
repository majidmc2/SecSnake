document.body.style.border = "10px solid blue";

// document.body.addEventListener('click', () => console.log("---------- HI -----------"))

// document.addEventListener('', () => console.log('DOM Events')); // number of event: 96

// setInterval(() => {
//     console.log(document.body)
// }, 200)

// let time;



browser.runtime.onMessage.addListener((rule) => {
    if(rule["rule"] === "document")
        browser.runtime.sendMessage({"data": document.documentElement.outerHTML, "tabURL": rule["tabURL"]});
        // browser.runtime.sendMessage(document.documentElement.outerHTML);
});