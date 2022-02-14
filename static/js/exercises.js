
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
    var title = wrapper.find(">:first-child");
    var name = title.text();
    console.log(wrapper.children().length)
    if (wrapper.children().length < 2) {
        title.attr('style', 'display: None');
        $('<textarea></textarea>')
            .attr({
                'type': 'text',
                'class': 'exercise-title-edit',
                'id': 'edit-exercise-title',
                'value': name,
                'spellcheck': 'false'
            })
            .appendTo(this);

        $('#edit-exercise-title').val(name);
        $('#edit-exercise-title').focus();
    }
    $('#edit-exercise-title').on('blur', function () {
        var input = $(this);
        var name = input.val();
        input.remove();
        temp = title.text();

        title.attr('style', 'display: block');
        if (temp !== name) {
            title.text(name);
            wrapper.on('click.editable');
            $.ajax({
                type: 'POST',
                url: '/dashboard/editexercise/',
                data: {
                    id: wrapper.attr('id'),
                    title: name,
                    csrfmiddlewaretoken: csrf_token,
                    dataType: "json",
                },
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
                    tempAlert('Error updating title', 4000, 0);

                }
            });
        }
    })

});

