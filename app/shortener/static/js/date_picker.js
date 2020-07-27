$(document).ready(function() {
    $('.datetimeinput').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        icons: {
            time: "fas fa-clock-o",
            date: "fas fa-calendar",
            up: "fas fa-arrow-up",
            down: "fas fa-arrow-down",
            next: "fas fa-arrow-right",
            previous: "fas fa-arrow-left",
        },
        sideBySide: true,
        defaultDate: moment().add(7,'days').add(1, "hours"),
        minDate: moment(),

    })
});