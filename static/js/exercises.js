
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