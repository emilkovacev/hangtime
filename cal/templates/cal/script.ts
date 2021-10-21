const HEIGHT = document.body.offsetHeight


class CalendarEvent {
  end_time: Date;
  start_time: Date;
  name: string;
  color: string;

  constructor(name: string, start_time: Date, end_time: Date, color: string) {
    this.name = name;
    this.start_time = start_time;
    this.end_time = end_time;
    this.color = color;
  }
}

const parseTime = (date: Date) => date.getHours() * 60 + date.getMinutes();


let events_list: CalendarEvent[] = [
  new CalendarEvent('Event A', new Date('October 20, 2021 3:00'), new Date('October 20, 2021 5:00'), 'green'),
  new CalendarEvent('Event B', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00'), 'red'),
  new CalendarEvent('Event Z', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00'), 'purple'),
  new CalendarEvent('Event C', new Date('October 20, 2021 15:00'), new Date('October 20, 2021 18:00'), 'blue'),
  new CalendarEvent('Event A', new Date('October 20, 2021 23:00'), new Date('October 20, 2021 23:59'), 'orange'),
];

function intersections(event: CalendarEvent): number {
  let count = 0;
  for (let i=0; i < events_list.indexOf(event); i++) {
    const cal_event = events_list[i]
    if (event.start_time <= cal_event.start_time && cal_event.start_time <= event.end_time) {count += 1;}
    else if (event.start_time <= cal_event.start_time && cal_event.start_time <= event.end_time) {count += 1;}
    else if (cal_event.start_time <= event.start_time && event.start_time <= cal_event.end_time) {count += 1;}
    else if (cal_event.start_time <= event.end_time && event.end_time <= cal_event.end_time) {count += 1;}
  }
  return count;
}

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

    eventBlock.style.top = (Math.round(start)).toString() + 'px';
    eventBlock.style.height = (Math.round(end-start)).toString() + 'px';
    eventBlock.style.backgroundColor = event.color;
    eventBlock.style.marginLeft = (40*intersections(event)).toString() + 'px';

    calendar.appendChild(eventBlock);
  }
}

function load() {
  loadEvents();
}

document.addEventListener('DOMContentLoaded', load);
