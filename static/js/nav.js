$(document).ready(function () {

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