

$(document).ready(function () {
    function loadPreviousNav() {
        prev_nav_link = $(`.nav-link[href="${previousHref}"]`);
        if (!prev_nav_link.hasClass('nav-link-selected')) {
            // remove higlight from previousl selected option
            $(".nav-link").each(function () {
                $(this).removeClass('nav-link-selected');
            });
            // add highlight to the clicked option
            prev_nav_link.addClass('nav-link-selected');
            console.log(prev_nav_link.attr('title'));
            $(".content-title").html(prev_nav_link.attr('title'));
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