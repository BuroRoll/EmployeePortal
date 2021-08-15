let body = document.querySelector('.calendar-container')

let month = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
];


let date = new Date()
for (let i = 0; i < 12; i++) {
    body.appendChild(MakeCalendarBlock(date.getMonth(), date.getFullYear()))
    date.setMonth(date.getMonth() + 1)
}


function MakeCalendarBlock(m, y) {
    let calendarBlock = document.createElement('div')
    calendarBlock.classList.add('calendar-block')

    let calendarHeader = document.createElement('div');
    calendarHeader.classList.add('calendar-header');
    calendarHeader.innerHTML = '<b class="mouth">' + month[m] + ' </b><span class="year">' + y + '</span>';
    calendarBlock.appendChild(calendarHeader)

    let table = document.createElement('table');
    table.classList.add('calendar-table');
    calendarBlock.appendChild(table)

    let tbody = document.createElement('tbody');
    table.appendChild(tbody)
    tbody.innerHTML = '<tr><th>Пн</th><th>Вт</th><th>Ср</th><th>Чт</th><th>Пт</th><th class="red">Сб</th><th class="red">Вс</th></tr>' +
        "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" +
        "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" +
        "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" +
        "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" +
        "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>" +
        "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>";
    let deltaDate = new Date((m + 1) + '/01/' + y)
    let curMonth = deltaDate.getMonth();


    let first = true;
    let tds = tbody.querySelectorAll('td')


    let firstWeekDay = deltaDate.getDay()

    if (firstWeekDay === 0) {
        firstWeekDay = 7;
    }

    for (let j = firstWeekDay - 1; j < tds.length; j++) {
        if (deltaDate.getMonth() === curMonth) {
            tds[j].id = (curMonth + 1) + '/' + deltaDate.getDate() + '/' + y;
            tds[j].textContent = deltaDate.getDate();
            deltaDate.setDate(deltaDate.getDate() + 1)
        }
    }

    return calendarBlock;
}

/*Работа кнопок в календаре*/

let calendarCountBlock = document.querySelector('.calendar-count')
let calendarCount = calendarCountBlock.innerHTML
let flagList = [];


let tds = document.querySelectorAll('td')

for (let td of tds) {
    td.onclick = function () {
        if (td.innerHTML !== '') {
            if (calendarCountBlock.innerHTML > 0) {
                if (!td.classList.contains('flag')) {
                    td.classList.add('flag')
                    flagList.push(td.id)
                    calendarCountBlock.innerHTML = calendarCountBlock.innerHTML - 1;
                } else {
                    td.classList.remove('flag')
                    let i = flagList.indexOf(td.id)
                    flagList.splice(i, 1)
                    calendarCountBlock.innerHTML = Number(calendarCountBlock.innerHTML) + 1;
                }
            } else if (td.classList.contains('flag')) {
                td.classList.remove('flag')
                let i = flagList.indexOf(td.id)
                flagList.splice(i, 1)
                calendarCountBlock.innerHTML = Number(calendarCountBlock.innerHTML) + 1;
            }
        }
    }
}


/*Работа кнопки отправления данных*/

let subBtn = document.querySelector('.calendar-sub-btn');

subBtn.onclick = function () {
    if (flagList.length !== 0) {
        flagList.sort(function (a, b) {
            return new Date(a) - new Date(b);
        });

        let sub = arrToStr(flagList)
        if (checkIntervalDate(sub)) {
            let countDate = (document.querySelector('.calendar-count')).textContent
            /*ЗДЕСЬ ОТПРАВЛЯТЬ ДАННЫЕ НА СЕРВЕР (тупо замени alert на функцию, которая отправляет данные на сервер)*/
            /*normalizeData(sub) - это дата в формате строки, а countDate - количество дней, которые остались*/
            const csrftoken = getCookie('csrftoken')

            fetch('/set_vacations/', {
                method: 'POST',
                headers: {
                    "X-CSRFToken": csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    vacations_days: sub,
                    day_counts: countDate
                })
            }).then(
                response => {
                    if (response.ok) {
                        let snackbar = document.getElementById("snackbar");
                        snackbar.className = "show";
                        setTimeout(function () {
                            snackbar.className = snackbar.className.replace("show", "");
                        }, 3000);
                    } else {
                        return Promise.reject(response)
                    }
                })
        } else {
            alert('Нужно обязательно выбрать промежуток не менее 14 дней')
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*Превращает массив дат в одну строку*/
function arrToStr(arr) {
    let res = '';
    let flagRange = false;
    for (let i = 0; i < arr.length; i++) {
        if (!flagRange) {
            res += arr[i];
        }

        let cur = new Date(arr[i])
        let next = new Date(arr[i + 1])
        cur.setDate(cur.getDate() + 1)

        if (cur.toDateString() === next.toDateString()) {
            flagRange = true;
        } else if (flagRange) {
            res += '->' + arr[i] + ';'
            flagRange = false;
        } else {
            res += ';'
        }

    }

    return res;
}


function strToArr(str) {
    let res = []
    let arrInterval = str.split(';').filter((x) => x !== '')
    for (let interval of arrInterval) {
        if (interval.includes('->')) {
            let interArr = interval.split('->')
            let cur = new Date(interArr[0])
            let last = new Date(interArr[1])
            while (cur.toDateString() !== last.toDateString()) {
                res.push(cur.getMonth() + 1 + '/' + cur.getDate() + '/' + cur.getFullYear())
                cur.setDate(cur.getDate() + 1)
            }
            res.push(last.getMonth() + 1 + '/' + last.getDate() + '/' + last.getFullYear())
        } else {
            res.push(interval)
        }
    }
    return res
}

function checkIntervalDate(strDate) {
    let arr = strDate.split(';').filter((x) => x !== '')
    for (let interval of arr) {
        if (strToArr(interval).length >= 14) {
            return true
        }
    }
    return false
}

function setDays(str) {
    let arr = strToArr(str)
    for (let date of arr) {
        let elementDate = document.getElementById(date.toString())
        elementDate.classList.add('flag')
        flagList.push(date)
    }
}

function setCountDays(str) {
    let doc = document.querySelector('.calendar-count')
    doc.innerHTML = str
}


function toNormalize(str) {
    let d_arr = str.split('/')
    return d_arr[0] + '/' + d_arr[1] + '/' + d_arr[2]
}