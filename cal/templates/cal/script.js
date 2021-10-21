var HEIGHT = document.body.offsetHeight;
var CalendarEvent = /** @class */ (function () {
    function CalendarEvent(name, start_time, end_time, color) {
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.color = color;
    }
    return CalendarEvent;
}());
var parseTime = function (date) { return date.getHours() * 60 + date.getMinutes(); };
var events_list = [
    new CalendarEvent('Event A', new Date('October 20, 2021 3:00'), new Date('October 20, 2021 5:00'), 'green'),
    new CalendarEvent('Event B', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00'), 'red'),
    new CalendarEvent('Event Z', new Date('October 20, 2021 13:00'), new Date('October 20, 2021 18:00'), 'purple'),
    new CalendarEvent('Event C', new Date('October 20, 2021 15:00'), new Date('October 20, 2021 18:00'), 'blue'),
    new CalendarEvent('Event A', new Date('October 20, 2021 23:00'), new Date('October 20, 2021 23:59'), 'orange'),
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
function loadEvents() {
    var calendar = document.getElementById('calendar');
    var event;
    for (var _i = 0, events_list_1 = events_list; _i < events_list_1.length; _i++) {
        event = events_list_1[_i];
        var eventBlock = document.createElement("div");
        eventBlock.innerHTML = "<div class=\"content\">\n                            <b>" + event.name + "</b>\n                            <p>" + event.start_time.toLocaleTimeString() + " - " + event.end_time.toLocaleTimeString() + "</p>\n                            </div>";
        eventBlock.className = 'event';
        var start = parseTime(event.start_time);
        var end = parseTime(event.end_time);
        console.log('start: ' + event.start_time.getHours() + ', end: ' + event.end_time.getHours());
        eventBlock.style.top = (Math.floor(start)).toString() + 'px';
        eventBlock.style.height = (Math.floor(end - start)).toString() + 'px';
        eventBlock.style.backgroundColor = event.color;
        eventBlock.style.marginLeft = (20 * intersections(event)).toString() + 'px';
        calendar.appendChild(eventBlock);
    }
}
document.addEventListener('DOMContentLoaded', loadEvents);
