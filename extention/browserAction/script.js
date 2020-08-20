const add = document.getElementById("AddHere")

function onGet(items) {
    let counter = 0

    for (let item in items) {

        let id = `AddcontextMessage${counter}`

        add.innerHTML += `
        <tr style="font-size: 10px">
          <td><b>${items[item]["title"]}</b></td>
          <td><b>${items[item]["message"]}</b></td>
          <td id=${id}></td>
        </tr>`;

        document.getElementById(id).innerText = items[item]["contextMessage"];
        counter++;
    }
}

function onError(error) {
    console.log(`Error: ${error}`);
}

let gettingItem = browser.storage.local.get();
gettingItem.then(onGet, onError);
