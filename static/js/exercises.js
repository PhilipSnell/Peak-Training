
// File Dropdown
// Alert accept popup
function uploadFileAlert(msg) {
    var el = document.createElement("div");
    el.setAttribute("class", "alertPopupAccept");
    el.innerHTML = msg;
    var optionWrapper = document.createElement("div");
    optionWrapper.setAttribute('class', 'optionWrapper');
    var cancel = document.createElement('button');
    cancel.setAttribute('class', 'cancelToggle toggleButton');
    cancel.innerHTML = 'Cancel';
    var contin = document.createElement('button');
    contin.setAttribute('class', 'continueToggle toggleButton');
    contin.innerHTML = 'Continue';
    optionWrapper.append(cancel);
    optionWrapper.append(contin);
    el.append(optionWrapper);


    document.body.appendChild(el);
    $(".continueToggle").on('click', function (e) {

        $(".alertPopupAccept").css('animation', 'slideC 1s');
        $('.toggleActiveIcon').attr('class', 'fas fa-toggle-on  toggleOn toggleActiveIcon')
        setTimeout(function () {
            $(".alertPopupAccept").remove();
        }, 1000);

        $.ajax({
            type: "POST",
            url: "dashboard/toggleWeek/",
            data: {
                phase: selectedPhase,
                week: selectedWeek,
                csrfmiddlewaretoken: csrf_token,
                dataType: "json",
            },
            success: function (data) {
                if (data['success']) {

                    tempAlert(data['success'], 4000, 1);
                    $('.toggleOff').on('click', function () {
                        tempAcceptAlert('Make this the active week?');
                    });
                } else {
                    tempAlert(data['error'], 4000, 0);
                    $('.toggleActiveIcon').attr('class', 'fas fa-toggle-off toggleOff toggleActiveIcon')
                    $('.toggleOff').on('click', function () {
                        tempAcceptAlert('Make this the active week?');
                    });
                }

            },
            failure: function () {
                tempAlert('Couldnt Activate Week', 4000, 0);
                $('.toggleActiveIcon').attr('class', 'fas fa-toggle-off toggleOff toggleActiveIcon')
            }
        });

    });
    $(".cancelToggle").on('click', function (e) {
        $(".alertPopupAccept").css('animation', 'slideC 1s');
        setTimeout(function () {
            $(".alertPopupAccept").remove();
        }, 1000);
    });
};


// edit in line

$('.editable').click(function () {

    var wrapper = $(this);
    if (wrapper.hasClass('exercise-description-text')) {
        wrapper = wrapper.parent();


    }
    var title = wrapper.find(">:first-child");
    console.log(title.attr('class'));
    var name = title.text();
    if (wrapper.children().not('div').length < 1) {

        $('<textarea></textarea>')
            .attr({
                'type': 'text',
                'class': title.attr('class') + '-edit',
                'id': 'edit-exercise-title',
                'value': name,
                'spellcheck': 'false'
            })
            .prependTo(wrapper);
        title.attr('style', 'display: none');
        $('#edit-exercise-title').val(name);
        $('#edit-exercise-title').focus();
    }
    $('#edit-exercise-title').on('blur', function () {
        var input = $(this);
        var name = input.val();
        input.remove();
        temp = title.text();


        if (temp !== name) {
            title.text(name);
            wrapper.find('a').attr('href', name)
            wrapper.on('click.editable');
            if (wrapper.hasClass('exercise-title-wrapper')) {
                title.attr('style', 'display: block');
                data = {
                    id: wrapper.attr('id'),
                    title: name,
                    csrfmiddlewaretoken: csrf_token,
                    dataType: "json",
                }
            } else if (wrapper.hasClass('exercise-url')) {
                title.attr('style', 'display: inline-block');
                data = {
                    id: wrapper.attr('id'),
                    new_url: name,
                    csrfmiddlewaretoken: csrf_token,
                    dataType: "json",
                }
            } else if (wrapper.hasClass('exercise-card-description')) {
                title.attr('style', 'display: block');
                data = {
                    id: wrapper.attr('id'),
                    description: name,
                    csrfmiddlewaretoken: csrf_token,
                    dataType: "json",
                }
            }
            $.ajax({
                type: 'POST',
                url: '/dashboard/editexercise/',
                data: data,
                success: function (data) {
                    if (data['error']) {
                        title.text(temp);
                        tempAlert(data['error'], 4000, 0);

                    } else {
                        tempAlert(data['success'], 4000, 1);
                    }

                },
                failure: function () {
                    title.text(temp);
                    tempAlert('Error updating exercise', 4000, 0);

                }
            });
        } else {
            if (wrapper.hasClass('exercise-title-wrapper')) {
                title.attr('style', 'display: block');
            } else if (wrapper.hasClass('exercise-url')) {
                title.attr('style', 'display: inline-block');
            }
        }
    })

});

// delete exercise

$('.exercise-remove').on('click', function () {
    delete_button = $(this);
    id = delete_button.attr('id');
    console.log(delete_button.parent().parent().parent().parent().parent().attr('class'))
    $.ajax({
        type: 'POST',
        url: '/dashboard/deleteexercise/',
        data: {
            id: id,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            if (data['error']) {
                tempAlert(data['error'], 4000, 0);
            } else {
                tempAlert(data['success'], 4000, 1);
                delete_button.parent().parent().parent().parent().parent().remove();
            }
        },
        failure: function () {
            title.text(temp);
            tempAlert('Error deleting exercise', 4000, 0);

        }
    });
})


// open description
$('.fa-ellipsis').on('click', function () {
    icon = $(this);
    desc_container = icon.parent().parent();

    description = desc_container.find('.exercise-description-text');
    description.slideToggle();
})
