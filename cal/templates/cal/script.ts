// GLOBAL variables
const HEIGHT = document.body.offsetHeight
const SHIFT = 40;


class CalendarEvent {
  end_time: Date;
  start_time: Date;
  name: string;
  color: string;
  description: string;

  constructor(name: string, start_time: Date, end_time: Date) {
    this.name = name;
    this.start_time = start_time;
    this.end_time = end_time;
    this.color = '#949494';
    this.description = '';
  }
}

const parseTime = (date: Date) => date.getHours() * 60 + date.getMinutes();


// this list should be sorted by date when populated!
// sorting the list will help event layering work properly

let events_list: CalendarEvent[] = [
  new CalendarEvent('Event D', new Date('October 20, 2021 0:00'), new Date('October 20, 2021 23:59')),
  new CalendarEvent('Event D', new Date('October 20, 2021 2:15'), new Date('October 20, 2021 22:00')),
  new CalendarEvent('Event A', new Date('October 20, 2021 3:00'), new Date('October 20, 2021 5:00')),
  new CalendarEvent('Event B', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00')),
  new CalendarEvent('Event Z', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00')),
  new CalendarEvent('Event C', new Date('October 20, 2021 15:00'), new Date('October 20, 2021 18:00')),
  new CalendarEvent('Event A', new Date('October 20, 2021 23:00'), new Date('October 20, 2021 23:59')),
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

function loadTimes(): void {
  const calendar = document.getElementById('calendar');
  for (let i=0; i<=24; i++) {
    calendar
  }
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

    const start: number = Math.round(parseTime(event.start_time)) + calendar.offsetTop + 20;
    const end: number = parseTime(event.end_time) + calendar.offsetTop + 20;

    console.log('start: ' + event.start_time.getHours() + ', end: ' + event.end_time.getHours())

    eventBlock.style.top = (Math.round(start)).toString() + 'px';
    eventBlock.style.height = (Math.round(end-start)).toString() + 'px';
    eventBlock.style.backgroundColor = event.color;
    eventBlock.style.marginLeft = (SHIFT*intersections(event)).toString() + 'px';

    calendar.appendChild(eventBlock);
  }
}

function load() {
  loadTimes();
  loadEvents();
}

function toggleEventForm() {
  const form = document.getElementById('form');
  const calendar = document.getElementById('calendar');
  const new_button = document.getElementById('new');
  if (form.style.display === 'flex') {
    form.style.display = 'none';
    calendar.style.display = 'block';
    new_button.innerHTML = '+';
  } else {
    form.style.display = 'flex';
    calendar.style.display = 'none';
    new_button.innerHTML = 'X';
  }
}

document.addEventListener('DOMContentLoaded', load);
document.getElementById('new').addEventListener('click', toggleEventForm)
