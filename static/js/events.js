// async function set_events() {
//     fetch('/events_list/', {
//         method: 'GET'
//     }).then(response => response.json())
//         .then(response => {
//             set_data(response)
//         });
// }
//
// async function set_data(data){
//     let container = document.getElementById('events_container')
//     for (const event of data) {
//         let event_html = create_event(event)
//         container.appendChild(event_html)
//     }
// }
//
// function create_event(event_data) {
//     const div = document.createElement('div')
//     div.setAttribute('class', 'event-block  no-show')
//     div.innerHTML = `
//     <div className="event-block  no-show">
//         <img className="event-img" style="height: 50px" src=${event_data.picture} alt="">
//             <div className="event-content">
//                 <div className="event-panel"><h1>${event_data.title}</h1> <img className="pointer"
//                                                                                                    src="strelka.png"
//                                                                                                    alt=""></div>
//                 <div className="event-count">
//                     <div className="free-place">Свободных мест: <span className="free-places">15</span></div>
//                     <div className="day-event">Дней до начала: <span className="days-before-start">3</span></div>
//                 </div>
//                 <div className="info-block">
//                     <div className="event-info-block">
//                         <div className="event-info-block-left">
//                             <h4 className="title-event">Время выставки</h4>
//                             <p className="date-info">${event_data.event_date}<br>${event_data.event_time}</p>
//                         </div>
//                         <div className="event-info-block-right">
//                             <h4 className="title-event">Место проведения</h4>
//                             <p className="event-place">${event_data.event_place}</p>
//                         </div>
//                     </div>
//
//                     <div className="event-anons">
//                         <h4 className="title-event">Описание</h4>
//                         <p className="event-opisanie">${event_data.description}</p>
//                     </div>
//
//                     <div className="party">
//                         <div>Всего мест: <span className="max-count">100</span></div>
//                         <a href="" style="color: grey; text-decoration: underline">Список участников</a>
//                     </div>
//
//                     <div className="event-sub green-btn">
//                         Подать заявку
//                     </div>
//                 </div>
//             </div>
//
//     </div>
//     `
//     return div;
// }
//
//
