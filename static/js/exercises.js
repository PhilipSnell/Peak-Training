
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
function monitorEdit() {
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
}
monitorEdit();
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

// add tools to navbar
if ($('.navbar').find('.exercise-tools').length != 0) {
    $('.exercise-tools').html('')
} else {
    $('.navbar').append('<div class="exercise-tools"><i class="fa-solid fa-arrow-up-from-bracket"></i><i class="fa-solid fa-plus"></i><div class="exercise-search-wrapper"><textarea class="exercise-search" spellcheck="false"></textarea><i class="fa-solid fa-magnifying-glass"></i></div></div>')
}

$(".exercise-search").on("keyup", function () {
    var search = $(this).val().trim().toLowerCase();
    $(".exercise-card").show().filter(function () {
        return $(".exercise-title", this).text().toLowerCase().indexOf(search) < 0;
    }).hide();
});

$(".fa-plus").on('click', function () {

    $(".exercise-search-wrapper").hide();
    $(".fa-plus").hide();

    backing = $(".table-wrapper");
    console.log(backing.find('.cover-content').length)
    if (backing.find('.cover-content').length === 0) {
        backing_cover = $('<div></div>').attr({
            'class': 'cover-content',
        })
        backing_cover.appendTo(backing);
        form = $('<form></form').attr({
            'class': 'exercise-form',
        })
        form.appendTo(backing_cover);
        card = $('<div></div>').attr({
            'class': 'exercise-card',
        })
        card.appendTo(form);
        content = $('<div></div>').attr({
            'class': 'exercise-card-content',
        });
        content.appendTo(card);
        image = $('<div></div>').attr({
            'class': 'exercise-image',
        });
        image.appendTo(content);
        title_wrapper = $('<div></div>').attr({
            'class': 'exercise-title-wrapper',
        });
        title_wrapper.appendTo(content);
        right = $('<div></div>').attr({
            'class': 'exercise-right',
        });
        right.appendTo(content);
        description = $('<div></div>').attr({
            'class': 'exercise-card-description',
        });
        description.appendTo(card);
        title = $('<input required></input>').attr({
            'class': 'exercise-title-edit new-title',
            'placeholder': 'Enter Exercise Name . . .',
        });
        title.appendTo(title_wrapper);
        options = $('<div></div>').attr({
            'class': 'exercise-options',
        });
        options.appendTo(right);
        url = $('<div></div>').attr({
            'class': 'exercise-url',
        });
        url.appendTo(right);
        thumbnail = $('<div></div>').attr({
            'class': 'exercise-thumbnail',
        });
        thumbnail.appendTo(options);
        public = $('<div></div>').attr({
            'class': 'exercise-public',
        });
        public.appendTo(options);
        thumbnail_text = $('<div>Use Video Thumbnail</div>').attr({
            'class': 'exercise-thumbnail-text',
        });
        thumbnail_text.appendTo(thumbnail);
        thumbnail_toggle = $('<div><i class="fas fa-toggle-off" aria-hidden="true"></i></div>').attr({
            'class': 'exercise-thumbnail-toggle',
        });
        thumbnail_toggle.appendTo(thumbnail);

        public_text = $('<div>Public</div>').attr({
            'class': 'exercise-public-text',
        });
        public_text.appendTo(public);
        public_toggle = $('<div><i class="fas fa-toggle-off" aria-hidden="true"></i></div>').attr({
            'class': 'exercise-public-toggle',
        });
        public_toggle.appendTo(public);

        url_input = $('<input></input>').attr({
            'class': 'exercise-url-text-edit',
            'type': 'text',
            'placeholder': 'Enter a youtube URL . . .'
        })
        url_input.appendTo(url);
        description_text = $('<div></div>').attr({
            'class': 'exercise-description-text',
        });
        description_text.appendTo(description);
        description_input = $('<input required></input>').attr({
            'class': 'editable-edit new-description',
            'type': 'text',
            'placeholder': 'Enter a Description for the Exercise . . .'
        })
        description_input.appendTo(description_text);
        $('<input></input>').attr({
            'class': 'submit-new-exercise',
            'type': 'submit',
            'value': 'Create Exercise',
        }).appendTo(form);
    } else {
        $('.cover-content').show();
    }

    $('.cover-content').on('click', function (e) {
        if (e.target !== this)
            return;
        $('.cover-content').hide();
        $(".exercise-search-wrapper").show();
        $(".fa-plus").show();
    });
    $('.exercise-form').on('submit', function (e) {
        e.preventDefault();
        // console.log(title.val())

        $.ajax({
            type: 'POST',
            url: '/dashboard/addExercise/',
            data: {
                title: title.val(),
                description: description_input.val(),
                video: url_input.val(),
                csrfmiddlewaretoken: csrf_token,
                dataType: "json",
            },
            success: function (data) {
                if (data['error']) {
                    tempAlert(data['error'], 4000, 0);
                } else {
                    $('.cover-content').hide();
                    $(".exercise-search-wrapper").show();
                    $(".fa-plus").show();
                    tempAlert(data['success'], 4000, 1);
                    new_id = data['id'];

                    $(".exercise-search").text(title.val());
                    title_text = $('<div></div>').attr({
                        'class': 'exercise-title',
                    });
                    title_text.text(title.val());
                    title.remove();
                    title_wrapper.addClass('editable');
                    title_wrapper.attr('id', new_id);
                    title_text.appendTo(title_wrapper);

                    description_txt = $('<div></div>').attr({
                        'class': 'exercise-description-text editable',
                        'style': 'display:none',
                    });
                    description_txt.text(description_input.val());
                    description_text.remove();
                    description.attr('id', new_id);
                    description_txt.appendTo(description);
                    description_icon = $('<div><i class="fa-solid fa-ellipsis"></i></div>').attr({
                        'class': 'exercise-description-icon',
                    });
                    description_icon.appendTo(description);

                    url_text = $('<div></div>').attr({
                        'class': 'exercise-url-text',
                    });
                    url_text.text(url_input.val());
                    url_icon = $('<div></div>').attr({
                        'class': 'exercise-open-url',
                    });
                    url_link = $('<a><i class="fa-solid fa-up-right-from-square"></i></a>').attr({
                        'href': url_input.val(),
                        'target': "_blank",
                    });
                    url_link.appendTo(url_icon);

                    url_input.remove();
                    url.attr('id', new_id);
                    url.addClass('editable');
                    url_text.appendTo(url);
                    url_icon.appendTo(url);
                    remove_wrapper = $('<div></div>').attr({
                        'class': 'exercise-remove-wrapper',
                    });
                    remove_wrapper.appendTo(options);
                    remove_button = $('<div>+</div>').attr({
                        'class': 'exercise-remove',
                        'id': new_id,
                    });

                    remove_button.appendTo(remove_wrapper);
                    card.prependTo($('.table-wrapper'));


                    $('.fa-ellipsis').on('click', function () {
                        icon = $(this);
                        desc_container = icon.parent().parent();
                        description = desc_container.find('.exercise-description-text');
                        description.slideToggle();
                    })
                    monitorEdit();
                }
            },
            failure: function () {
                tempAlert('Error deleting exercise', 4000, 0);

            }
        });

    })

})