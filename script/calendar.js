// event definition
var CalEvent = /** @class */ (function () {
    function CalEvent(name, start_time, end_time, color, description) {
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.color = color;
        this.description = description;
    }
    return CalEvent;
}());
// this list should be sorted by date when populated!
// sorting the list will help event layering work properly
var events_list = [
    new CalEvent('Event D', new Date('October 20, 2021 0:00'), new Date('October 20, 2021 23:59'), '#ff7961', ''),
    new CalEvent('Event D', new Date('October 20, 2021 2:15'), new Date('October 20, 2021 22:00'), '#ff7961', ''),
];
var sort_events = function (a, b) {
    if (a.start_time < b.start_time)
        return -1;
    else if (a.start_time > b.start_time)
        return 1;
    return 0;
};
// websocket frames + parsing
var socket = new WebSocket('ws://' + window.location.host + '/websocket');
socket.onmessage = addEvent;
function addEvent(frame) {
    console.log(frame);
    var parsed = JSON.parse(frame);
    var event = new CalEvent(parsed['name'], new Date('1970-01-01T' + parsed['start_time']), new Date('1970-01-01T' + parsed['end_time']), parsed['color'], parsed['description']);
    events_list.push(event);
    events_list.sort(sort_events);
}
var parseTime = function (date) { return date.getHours() * 60 + date.getMinutes(); };
var SHIFT = 40;
function loadEvents(events_list) {
    var calendar = document.getElementById('calendar');
    var event;
    for (var _i = 0, events_list_1 = events_list; _i < events_list_1.length; _i++) {
        event = events_list_1[_i];
        var eventBlock = generateEventBlock(event, events_list);
        calendar.appendChild(eventBlock);
    }
}
// Count the number of intersections of one event with all others
// Is used to determine how many pixels to shift each event on overlaps
function intersections(event, events_list) {
    var count = 0;
    for (var i = 0; i < events_list.indexOf(event); i++) {
        var cal_event = events_list[i];
        if (event.start_time <= cal_event.start_time && cal_event.start_time <= event.end_time) {
            count += 1;
        }
        else if (event.start_time <= cal_event.start_time && cal_event.start_time <= event.end_time) {
            count += 1;
        }
        else if (cal_event.start_time <= event.start_time && event.start_time <= cal_event.end_time) {
            count += 1;
        }
        else if (cal_event.start_time <= event.end_time && event.end_time <= cal_event.end_time) {
            count += 1;
        }
    }
    return count;
}
function generateEventBlock(event, events_list) {
    var calendar = document.getElementById('calendar');
    var eventBlock = document.createElement("div");
    eventBlock.innerHTML = "<div class=\"content\">\n                          <b>" + event.name + "</b>\n                          <p>" + event.start_time.toLocaleTimeString() + " - " + event.end_time.toLocaleTimeString() + "</p>\n                          </div>";
    eventBlock.className = 'event';
    var start = Math.round(parseTime(event.start_time)) + calendar.offsetTop + 20;
    var end = parseTime(event.end_time) + calendar.offsetTop + 20;
    eventBlock.style.top = (Math.round(start)).toString() + 'px';
    eventBlock.style.height = (Math.round(end - start)).toString() + 'px';
    eventBlock.style.backgroundColor = event.color;
    eventBlock.style.marginLeft = (SHIFT * intersections(event, events_list)).toString() + 'px';
    return eventBlock;
}
function toggleEventForm() {
    var form = document.getElementById('form');
    var calendar = document.getElementById('calendar');
    var new_button = document.getElementById('new');
    if (form.style.display === 'flex') {
        form.style.display = 'none';
        calendar.style.display = 'block';
        new_button.innerHTML = '<i class="bi bi-circle-plus"></i>';
    }
    else {
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
document.getElementById('new').addEventListener('click', toggleEventForm);
