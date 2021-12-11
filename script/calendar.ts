// event definition
class CalEvent {
  end_time: Date;
  start_time: Date;
  name: string;
  color: string;
  description: string;

  constructor(name: string, start_time: Date, end_time: Date, color: string, description: string) {
    this.name = name;
    this.start_time = start_time;
    this.end_time = end_time;
    this.color = color;
    this.description = description;
  }
}


// this list should be sorted by date when populated!
// sorting the list will help event layering work properly

let events_list: CalEvent[] = [
  // new CalEvent('Event D', new Date('October 20, 2021 0:00'), new Date('October 20, 2021 23:59'), '#ff7961', ''),
  // new CalEvent('Event D', new Date('October 20, 2021 2:15'), new Date('October 20, 2021 22:00'), '#ff7961', ''),
];

const sort_events = (a: CalEvent, b: CalEvent) => {
  if (a.start_time < b.start_time) return -1;
  else if (a.start_time > b.start_time) return 1;
  return 0;
}


// websocket frames + parsing
var socket = new WebSocket('ws://' + window.location.host + '/calsocket');
socket.onmessage = addEvent


// functions

interface Frame {
  name: string;
  start_time: string;
  end_time: string;
  color: string;
  description: string;
}

function addEvent(frame) {
  console.log(frame.data)

  const parsed: Frame = JSON.parse(frame.data);
  const event: CalEvent = new CalEvent(
      parsed['event_name'],
      new Date('1970-01-01T' + parsed['start_time']),
      new Date('1970-01-01T' + parsed['end_time']),
      parsed['color'],
      parsed['description']
  )
  events_list.push(event)
  events_list.sort(sort_events)
  loadEvents(events_list);
}

const parseTime = (date: Date) => date.getHours() * 60 + date.getMinutes();
const SHIFT = 40;


function loadEvents(events_list: CalEvent[]): void {
  const calendar = document.getElementById('calendar');

  let event: CalEvent
  for (event of events_list) {
    const eventBlock = generateEventBlock(event, events_list);
    calendar.appendChild(eventBlock);
  }
}

// Count the number of intersections of one event with all others
// Is used to determine how many pixels to shift each event on overlaps

function intersections(event: CalEvent, events_list: CalEvent[]): number {
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


function generateEventBlock(event: CalEvent, events_list: CalEvent[]) {
  const calendar = document.getElementById('calendar');
  const eventBlock = document.createElement("div");

  const start_time = event.start_time.toLocaleString('en-US', { hour: 'numeric', hour12: true, minute: 'numeric' })
  const end_time = event.end_time.toLocaleString('en-US', { hour: 'numeric', hour12: true, minute: 'numeric' })
  eventBlock.innerHTML = `<div class="content">
                          <p><b>${event.name}</b><br/> ${start_time} - ${end_time}</p>
                          </div>`;

  eventBlock.className = 'event';

  const start: number = Math.round(parseTime(event.start_time)) + calendar.offsetTop + 20;
  const end: number = parseTime(event.end_time) + calendar.offsetTop + 20;

  eventBlock.style.top = (Math.round(start)).toString() + 'px';
  eventBlock.style.height = (Math.round(end-start)).toString() + 'px';
  eventBlock.style.backgroundColor = event.color;
  eventBlock.style.marginLeft = (SHIFT*intersections(event, events_list)).toString() + 'px';

  return eventBlock;
}

function toggleEventForm() {
  const form = document.getElementById('form');
  const calendar = document.getElementById('calendar');
  const new_button = document.getElementById('new');

  if (form.style.display === 'flex') {
    form.style.display = 'none';
    calendar.style.display = 'block';
    new_button.innerHTML = '<i class="bi bi-calendar-plus"></i>';
  } else {
    form.style.display = 'flex';
    calendar.style.display = 'none';
    new_button.innerHTML = '<i class="bi bi-x"></i>';
  }
}

// all functions executed at loadtime
function load() {
  loadEvents(events_list);
}

// Event Listeners

document.addEventListener('DOMContentLoaded', load);
document.getElementById('new').addEventListener('click', toggleEventForm)
