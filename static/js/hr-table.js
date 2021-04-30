let blocks = document.querySelectorAll('.candidate-list-block')

for(let block of blocks) {
    let tds = block.querySelectorAll('td')
        if (tds.length !== 0) {
            tds[4].onclick = function () {

                if (tds[4].firstChild.textContent === 'Удалить') {
                    deleteBlock()
                }

                setImg()
                let img = tds[4].querySelector('img')
                tds[4].removeChild(img)
                tds[4].insertAdjacentHTML('beforeend', '<div id="delete-block">Удалить</div>')
            }
        }
}


function setImg() {
    for (let b_delta of blocks) {
        let tds_delta = b_delta.querySelectorAll('td')
        if (tds_delta.length !== 0 && tds_delta[4].childNodes.length !== 0 ) {
            while (tds_delta[4].firstChild) {
                tds_delta[4].removeChild(tds_delta[4].lastChild);
            }
            tds_delta[4].insertAdjacentHTML('beforeend', '<img src="img/delete.png" alt="" class="delete-img">')
        }
    }
}

function deleteBlock() {
    alert('Удаление блока')
}




/*
let blocks = document.querySelectorAll('.candidate-list-block')

for(let block of blocks) {
    let tds = block.querySelectorAll('td')
    block.onclick = function () {
        setImg()

        let img = tds[4].querySelector('img')
        tds[4].removeChild(img)
        tds[4].insertAdjacentHTML('beforeend', '<div>Удалить</div>')
    }
}

function setImg() {
    for (let b_delta of blocks) {
        let tds_delta = b_delta.querySelectorAll('td')
        if (tds_delta.length !== 0 && tds_delta[4].childNodes.length !== 0 ) {
            while (tds_delta[4].firstChild) {
                tds_delta[4].removeChild(tds_delta[4].lastChild);
            }
            tds_delta[4].insertAdjacentHTML('beforeend', '<img src="img/delete.png" alt="" class="delete-img">')
        }
    }
}
 */