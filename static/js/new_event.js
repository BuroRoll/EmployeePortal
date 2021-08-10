//блок предварительного просмотра
let test_block = document.getElementById('test-block')

//Переменные инпутов, чтобы с них брать инфу
let input_name = document.querySelector('input[name=name]')
let input_count = document.querySelector('input[name=event-count]')
let input_dates = document.querySelectorAll('input[type=date]')
let input_date = document.querySelector('input[name=date-event]')
let input_time = document.querySelector('input[name=time-event]')
let input_location = document.querySelector('input[name=location-event]')
let textarea = document.querySelector('textarea[name=description]')
let check_list = document.querySelector('input[name=view-list]')
let check_count = document.querySelector('input[name=view-count]')


//перменные блоков предварительного просмотра
let name = test_block.querySelector('h1')
let free_places = test_block.querySelector('.free-places')
let max_count = test_block.querySelector('.max-count')
let date_event = test_block.querySelector('.event-date')
let time_event = test_block.querySelector('.event-time')
let days_before_start = test_block.querySelector('.days-before-start')
let loc = test_block.querySelector('.event-place')
let des = test_block.querySelector('.event-opisanie')
let e_list = test_block.querySelector('.e-list')
let e_count = test_block.querySelector('.e-count')

//Ограничение инпут дэйт чтобы нельзя было выбрать прошедшие даты
let today = new Date();
let dd = today.getDate();
let mm = today.getMonth() + 1; //January is 0!
let yyyy = today.getFullYear();
if (dd < 10) {
    dd = '0' + dd
}
if (mm < 10) {
    mm = '0' + mm
}

today = yyyy + '-' + mm + '-' + dd;


for (let el of input_dates)
    el.setAttribute("min", today);

//Заполнение данных
input_name.oninput = function () {
    name.textContent = input_name.value
}

input_count.oninput = function () {
    free_places.textContent = max_count.textContent = input_count.value
}

input_date.oninput = function () {
    let month = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
    let date = input_date.value
    let date_arr = date.split('-')
    let date_text = `${parseInt(date_arr[2])} ${month[parseInt(date_arr[1]) - 1]} ${date_arr[0]} г.`
    date_event.textContent = date_text
    let oneDay = 1000 * 60 * 60 * 24
    days_before_start.textContent = Math.ceil(((new Date(input_date.value) - new Date()) / oneDay))
}

input_time.oninput = function () {
    time_event.textContent = input_time.value
}

input_location.oninput = function () {
    loc.textContent = input_location.value
}

textarea.oninput = function () {
    des.textContent = textarea.value
}

check_list.onclick = function () {
    if (check_list.checked) {
        e_list.style.display = 'block'
    } else {
        e_list.style.display = 'none'
    }
}

check_count.onclick = function () {
    if (check_count.checked) {
        e_count.style.display = 'block'
    } else {
        e_count.style.display = 'none'
    }
}

// Удаление мероприятия
let del_btns = document.querySelectorAll('.event-delete')
for (let del_btn of del_btns) {
    del_btn.onclick = function () {
        if (del_btn.classList.contains('event-delete-double')) {
            delete_event(del_btn.id)
        } else {
            setDefault()
            del_btn.classList.add('event-delete-double')
        }
    }
}

function setDefault() {
    for (let del_btn of del_btns) {
        del_btn.classList.remove('event-delete-double')
    }
}

/*Переключение разделов*/
//кнопки
let createElementBtn = document.querySelector('.create-event')
let myEventsBtn = document.querySelector('.my-events')

let createElement = document.getElementById('create-new-event')
let myEvents = document.getElementById('my_events')

//Назначим дефолтный раздел - создание нового элемента
createElement.style.maxHeight = createElement.scrollHeight + 1000 + 'px'
createElement.style.marginBottom = 100 + 'px'

createElementBtn.onclick = function () {
    createElementBtn.classList.add('active-btn')
    myEventsBtn.classList.remove('active-btn')
    createElement.style.maxHeight = createElement.scrollHeight + 100 + 'px'
    createElement.style.marginTop = 50 + 'px'
    myEvents.style.maxHeight = 0;
    myEvents.style.marginTop = 0;
    createElement.style.marginBottom = 100 + 'px'
}

myEventsBtn.onclick = function () {
    myEventsBtn.classList.add('active-btn')
    createElementBtn.classList.remove('active-btn')
    myEvents.style.maxHeight = myEvents.scrollHeight + 1000 * n + 'px'
    myEvents.style.marginTop = 50 + 'px'
    createElement.style.marginTop = 0
    createElement.style.maxHeight = 0;
    createElement.style.marginBottom = 100 + 'px'
    createElement.style.marginBottom = 0 + 'px'

}

//Заполнение данных и обработка формы
let myRedEvents = document.querySelectorAll('.my-red-block')
for (let redEvent of myRedEvents) {
    let iDate = redEvent.querySelector('input[name=new-date]')
    let iCount = redEvent.querySelector('input[name=new-count]')
    let oneDay = 1000 * 60 * 60 * 24
    let daysToEvent = redEvent.querySelector('.days-before-start')
    let freePlaces = redEvent.querySelector('.free-places')
    daysToEvent.textContent = Math.round(((new Date(iDate.value) - new Date()) / oneDay)) + 1
    iDate.oninput = function () {
        daysToEvent.textContent = Math.ceil(((new Date(iDate.value) - new Date()) / oneDay))
    }

    let places = iCount.value - freePlaces.textContent
    iCount.min = places
    iCount.oninput = function () {
        freePlaces.textContent = iCount.value - places
    }

}

// Запрос на создание мероприятия
let createBtn = document.getElementById('create-event')
createBtn.onclick = function () {
    if (input_date.value !== ''
        || input_name.value !== ''
        || input_count.value !== ''
        || input_time.value !== ''
        || input_location.value !== ''
        || textarea.value !== '')
        create_event()
}


//Редактирование мероприятия
for (let editEvent of myRedEvents) {
    let sub = editEvent.querySelector('.event-sub')
    sub.onclick = function () {
        let new_date = editEvent.querySelector('input[name=new-date]')
        let new_time = editEvent.querySelector('input[name=new-time]')
        let new_place = editEvent.querySelector('textarea[name=new-place]')
        let new_description = editEvent.querySelector('textarea[name=new-description]')
        let new_count = editEvent.querySelector('input[name=new-count]')
        edit_event(sub.id, new_date.value, new_time.value, new_place.value, new_description.value, new_count.value)
    }
}



