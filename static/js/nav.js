

$(document).ready(function () {

    var session_id = sessionStorage.getItem("session_id");
    if ( session_id == null){
        session_id = makeid(6);
        sessionStorage.setItem("session_id", session_id);
    }
    $("#id_session_id").val(session_id);

    function makeid(length) {
        var result           = '';
        var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
          result += characters.charAt(Math.floor(Math.random() * 
     charactersLength));
       }
       return result;
    }
    
    function loadPreviousNav() {
        prev_nav_link = $(`.nav-link[href="${previousHref}"]`);
        if (typeof prev_nav_link.attr('href') !== 'undefined') {
            if (!prev_nav_link.hasClass('nav-link-selected')) {
                // remove higlight from previousl selected option
                $(".nav-link").each(function () {
                    $(this).removeClass('nav-link-selected');
                });
                // add highlight to the clicked option
                prev_nav_link.addClass('nav-link-selected');
                console.log(prev_nav_link.attr('title'));
                $(".content-title").html(prev_nav_link.attr('title'));
                $(".exercise-tools").remove();
                $(".graph-tools").remove();
                $(".custom-select").each(function () {
                    $(this).remove();
                    console.log('removed')

                });
                // requests the new html segment
                $.ajax({
                    type: "GET",
                    url: prev_nav_link.attr('href'),
                    data: {},
                    success: function (data) {
                        $(".content-backing").html(data)
                    }
                })

            }
        }
    }
    loadPreviousNav();
    // when a navigation link is clicked
    $(".nav-link").click(function () {
        var nav_link = $(this);
        console.log(nav_link.hasClass('nav-link-selected'));
        if (!nav_link.hasClass('nav-link-selected')) {
            // remove higlight from previousl selected option
            $(".nav-link").each(function () {
                $(this).removeClass('nav-link-selected');
            });
            // add highlight to the clicked option
            nav_link.addClass('nav-link-selected');
            console.log(nav_link.attr('title'));
            $(".content-title").html(nav_link.attr('title'));
            $(".exercise-tools").remove();
            $(".graph-tools").remove();
            $(".custom-select").each(function () {
                $(this).remove();

            });
            // requests the new html segment
            $.ajax({
                type: "GET",
                url: nav_link.attr('href'),
                data: {},
                success: function (data) {
                    $(".content-backing").html(data)
                }
            })

        }

    });
})
// Alert popup
function tempAlert(msg, duration, type) {
    var el = document.createElement("div");
    if (type == 0) {
        el.setAttribute("class", "alertPopupError slideAnim");
    }
    else if (type == 1) {
        el.setAttribute("class", "alertPopupSuccess slideAnim");
    }

    el.innerHTML = msg;
    setTimeout(function () {
        el.parentNode.removeChild(el);
    }, duration);
    document.body.appendChild(el);
}
// for graph.js
months = {
    0: 'Jan',
    1: 'Feb',
    2: 'Mar',
    3: 'Apr',
    4: 'May',
    5: 'Jun',
    6: 'Jul',
    7: 'Aug',
    8: 'Sept',
    9: 'Oct',
    10: 'Nov',
    11: 'Dec'
};