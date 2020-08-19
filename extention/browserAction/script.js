const add = document.getElementById("AddHere")

function onGet(items) {
    for (let item in items) {
        add.innerHTML += `
        <tr style="font-size: 10px">
          <td>${items[item]["title"]}</td>
          <td>${items[item]["message"]}</td>
          <td>${items[item]["contextMessage"]}</td>
        </tr>`;
    }
}

function onError(error) {
    console.log(`Error: ${error}`);
}

let gettingItem = browser.storage.local.get();
gettingItem.then(onGet, onError);
