let event_blocks = document.querySelectorAll('.event-block')


for (let block of event_blocks) {
    let pointer = block.querySelector('.pointer')

    //Укорачивание названия
    let title = block.querySelector('h1')
    title.data = title.textContent
    title.textContent = title.textContent.length > 20 ? title.textContent.substring(0, 20) + '...' : title.data

    //Настройка цветов
    let freePlace = block.querySelector('.free-places')
    let daysBefore = block.querySelector('.days-before-start')
    let maxPlace = block.querySelector('.max-count')

    if (daysBefore.textContent <= 3) {
        daysBefore.classList.add('red-text')
    } else {
        daysBefore.classList.add('green-text')
    }

    if (freePlace.textContent / maxPlace.textContent < 0.2) {
        freePlace.classList.add('red-text')
    } else {
        freePlace.classList.add('green-text')
    }

    //Раскрытие блока
    pointer.onclick = function () {
        if (block.classList.contains('no-show')) {
            block.classList.add('show')
            block.classList.remove('no-show')
            pointer.style.transform = 'rotate(270deg)'
            title.textContent = title.data
        } else {
            block.classList.add('no-show')
            block.classList.remove('show')
            pointer.style.transform = 'rotate(90deg)'
            title.textContent = title.textContent.length > 20 ? title.textContent.substring(0, 20) + '...' : title.data
        }
    }

    let subBtn = block.querySelector('.event-sub')

    //Обработка кнопки мероприятия
    subBtn.onclick = function () {
        if (subBtn.classList.contains('green-btn')) {
            //Добавление в мероприятие
            subBtn.textContent = 'Отменить заявку'
            subBtn.classList.remove('green-btn')
            subBtn.classList.add('red-btn')
            // freePlace.textContent--
        } else {
            //Удаление из мероприятия
            subBtn.textContent = 'Подать заявку'
            subBtn.classList.remove('red-btn')
            subBtn.classList.add('green-btn')
            // freePlace.textContent++
        }
    }


}
