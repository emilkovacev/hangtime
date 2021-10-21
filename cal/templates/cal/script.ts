const HEIGHT = document.body.offsetHeight


class CalendarEvent {
  end_time: Date;
  start_time: Date;
  name: string;

  constructor(name: string, start_time: Date, end_time: Date) {
    this.name = name;
    this.start_time = start_time;
    this.end_time = end_time;
  }
}

const parseTime = (date: Date) => date.getHours() * 60 + date.getMinutes();


let events_list: CalendarEvent[] = [
  new CalendarEvent('Event A', new Date('October 20, 2021 3:00'), new Date('October 20, 2021 5:00')),
  new CalendarEvent('Event B', new Date('October 20, 2021 15:00'), new Date('October 20, 2021 18:00')),
  new CalendarEvent('Event C', new Date('October 20, 2021 15:00'), new Date('October 20, 2021 18:00')),
  new CalendarEvent('Event A', new Date('October 20, 2021 23:00'), new Date('October 20, 2021 23:59')),
];

function loadEvents(): void {
  const calendar = document.getElementById('calendar');

  let event: CalendarEvent
  for (event of events_list) {
    const eventBlock = document.createElement("div");
    eventBlock.innerHTML = `<div class="content">
                            <b>${event.name}</b>
                            <p>${event.start_time.toLocaleTimeString()} - ${event.end_time.toLocaleTimeString()}</p>
                            </div>`;

    eventBlock.className = 'event';

    const start: number = parseTime(event.start_time);
    const end: number = parseTime(event.end_time);

    console.log('start: ' + event.start_time.getHours() + ', end: ' + event.end_time.getHours())

    eventBlock.style.top = (Math.floor(start)).toString() + 'px';
    eventBlock.style.height = (Math.floor(end-start)).toString() + 'px';

    calendar.appendChild(eventBlock);
  }
}

document.addEventListener('DOMContentLoaded', loadEvents);
