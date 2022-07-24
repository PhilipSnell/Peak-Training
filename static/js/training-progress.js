
$.fn.hScroll = function (options) {
    function scroll(obj, e) {
        var evt = e.originalEvent;
        var scale = 15;
        var direction = evt.detail ? evt.detail * (-scale) : evt.wheelDelta;

        if (direction > 0) {
            direction = $(obj).scrollLeft() - scale;
        }
        else {
            direction = $(obj).scrollLeft() + scale;
        }

        $(obj).scrollLeft(direction);

        e.preventDefault();
    }

    $(this).width($(this).find('div').width());

    $(this).bind('DOMMouseScroll mousewheel', function (e) {
        scroll(this, e);
    });
}
$(document).ready(function () {
    $('.day-selector-wrapper').hScroll();
});


function getDays() {

    $.ajax({
        type: "GET",
        url: '/dashboard/getDays/',
        data: {
            session_id: sessionStorage.getItem("session_id"),
            phase: selectedPhase,
            week: selectedWeek,
            progress: 'true',
        },
        success: function (data) {
            $('.day-selector-wrapper').html(data);
            monitorAddDay();

        }

    })
}
function getDayData() {
    $.ajax({
        type: "POST",
        url: '/dashboard/getDayDataProg/',
        data: {
            session_id: sessionStorage.getItem("session_id"),
            phase: selectedPhase,
            week: selectedWeek,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            if (data['error']) {
                tempAlert(data['error'], 4000, 0);
            } else {
                $('.tableWrapper').html(data);
            }


        },
        failure: function () {
            tempAlert('Could not load days!', 4000, 0);
        }

    })
};
function monitorAddDay() {
    $(".addDayButton").on('click', function () {
        $.ajax({
            type: "POST",
            url: "/dashboard/addDay/",
            data: {
                session_id: sessionStorage.getItem("session_id"),
                phase: selectedPhase,
                week: selectedWeek,
                csrfmiddlewaretoken: csrf_token,
                dataType: "json",
            },
            success: function (data) {

                if (data['success']) {
                    tempAlert(data['success'], 4000, 1);
                    getDays();
                    getDayData();
                } else {
                    tempAlert(data['error'], 4000, 0);
                }

            },
            failure: function () {
                tempAlert('Error adding day', 4000, 0);
            }
        });
    });
}
