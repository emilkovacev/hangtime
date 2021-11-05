// GLOBAL variables
var HEIGHT = document.body.offsetHeight;
var SHIFT = 40;
var CalendarEvent = /** @class */ (function () {
    function CalendarEvent(name, start_time, end_time) {
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.color = '#949494';
        this.description = '';
    }
    return CalendarEvent;
}());
var parseTime = function (date) { return date.getHours() * 60 + date.getMinutes(); };
// this list should be sorted by date when populated!
// sorting the list will help event layering work properly
var events_list = [
    new CalendarEvent('Event D', new Date('October 20, 2021 0:00'), new Date('October 20, 2021 23:59')),
    new CalendarEvent('Event D', new Date('October 20, 2021 2:15'), new Date('October 20, 2021 22:00')),
    new CalendarEvent('Event A', new Date('October 20, 2021 3:00'), new Date('October 20, 2021 5:00')),
    new CalendarEvent('Event B', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00')),
    new CalendarEvent('Event Z', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00')),
    new CalendarEvent('Event C', new Date('October 20, 2021 15:00'), new Date('October 20, 2021 18:00')),
    new CalendarEvent('Event A', new Date('October 20, 2021 23:00'), new Date('October 20, 2021 23:59')),
];
function intersections(event) {
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
function loadTimes() {
    var calendar = document.getElementById('calendar');
    for (var i = 0; i <= 24; i++) {
        calendar;
    }
}
function loadEvents() {
    var calendar = document.getElementById('calendar');
    var event;
    for (var _i = 0, events_list_1 = events_list; _i < events_list_1.length; _i++) {
        event = events_list_1[_i];
        var eventBlock = document.createElement("div");
        eventBlock.innerHTML = "<div class=\"content\">\n                            <b>" + event.name + "</b>\n                            <p>" + event.start_time.toLocaleTimeString() + " - " + event.end_time.toLocaleTimeString() + "</p>\n                            </div>";
        eventBlock.className = 'event';
        var start = Math.round(parseTime(event.start_time)) + calendar.offsetTop + 20;
        var end = parseTime(event.end_time) + calendar.offsetTop + 20;
        console.log('start: ' + event.start_time.getHours() + ', end: ' + event.end_time.getHours());
        eventBlock.style.top = (Math.round(start)).toString() + 'px';
        eventBlock.style.height = (Math.round(end - start)).toString() + 'px';
        eventBlock.style.backgroundColor = event.color;
        eventBlock.style.marginLeft = (SHIFT * intersections(event)).toString() + 'px';
        calendar.appendChild(eventBlock);
    }
}
function load() {
    loadTimes();
    loadEvents();
}
function toggleEventForm() {
    var form = document.getElementById('form');
    var calendar = document.getElementById('calendar');
    var new_button = document.getElementById('new');
    if (form.style.display === 'flex') {
        form.style.display = 'none';
        calendar.style.display = 'block';
        new_button.innerHTML = '+';
    }
    else {
        form.style.display = 'flex';
        calendar.style.display = 'none';
        new_button.innerHTML = '✕';
    }
}
document.addEventListener('DOMContentLoaded', load);
document.getElementById('new').addEventListener('click', toggleEventForm);
