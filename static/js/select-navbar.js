function getPhaseDropdown() {
    $.ajax({
        type: "GET",
        url: '/dashboard/phaseDropdown/',
        data: {},
        success: function (data) {
            $('.custom-select-phase').html(data);
            handleDropdown('custom-select-phase');
            getWeekDropdown();
        }
    })
};

if ($('.navbar').find('.custom-select-phase').length != 0) {
    $('.custom-select-phase').html('')
} else {
    $('.navbar').append('<div class="custom-select custom-select-phase"><select><option value="0" title="add phase">+</option></select></div>')
}
if ($('.navbar').find('.custom-select-week').length != 0) {
    $('.custom-select-week').html('')
} else {
    $('.navbar').append('<div class="custom-select custom-select-week"><select></select></div>')
}
getPhaseDropdown();

function getWeekDropdown() {

    $.ajax({
        type: "GET",
        url: '/dashboard/weekDropdown/',
        data: {
            phase: selectedPhase
        },
        success: function (data) {
            $('.custom-select-week').html(data)
            handleDropdown('custom-select-week');
            getDays();
            getDayData();
        }


    })
}


function handleDropdown(target) {
    var dropdown, options, option, numberOfOptions, selectedOption, selectedElement, optionMenu, index
    dropdown = document.getElementsByClassName(target)[0];
    options = dropdown.getElementsByTagName("select")[0].options;
    numberOfOptions = dropdown.getElementsByTagName("select")[0].length;
    selectedElement = document.createElement("div");
    selectedElement.setAttribute('class', 'select-selected');
    if (numberOfOptions > 1) {
        selectedOption = options[1]
        if (target == 'custom-select-week') {
            selectedWeek = options[1].value;
        } else if (target == 'custom-select-phase') {
            selectedPhase = options[1].value;
        }
        selectedElement.innerHTML = selectedOption.innerHTML;
    }
    else { selectedWeek = 0 }

    dropdown.appendChild(selectedElement);
    optionMenu = document.createElement('div');
    optionMenu.setAttribute('class', 'select-items select-hide');
    for (index = 1; index < numberOfOptions; index++) {
        option = document.createElement('div');
        option.innerHTML = options[index].innerHTML;

        option.setAttribute('value', options[index].value);
        option.addEventListener('click', function () {
            var y, i, k, h, yl;
            var selectElement = dropdown.getElementsByTagName("select")[0];
            h = this.parentNode.previousSibling;
            for (i = 0; i < numberOfOptions; i++) {

                if (options[i].innerHTML == this.innerHTML) {
                    if (i == 0 && target == 'custom-select-phase') {
                        $.ajax({
                            type: "POST",
                            url: "/dashboard/addPhase/",
                            data: {
                                csrfmiddlewaretoken: csrf_token,
                                dataType: "json",
                            },
                            success: function (data) {

                                if (data['success']) {
                                    tempAlert(data['success'], 4000, 1);
                                    getPhaseDropdown();
                                } else {
                                    tempAlert(data['error'], 4000, 0);
                                }

                            },
                            failure: function () {
                                tempAlert('Error adding phase', 4000, 0);
                            }
                        });
                    } else if (i == 0 && target == 'custom-select-week') {
                        $.ajax({
                            type: "POST",
                            url: "/dashboard/addWeek/",
                            data: {
                                phase: selectedPhase,
                                csrfmiddlewaretoken: csrf_token,
                                dataType: "json",
                            },
                            success: function (data) {

                                if (data['success']) {
                                    tempAlert(data['success'], 4000, 1);
                                    getWeekDropdown();
                                } else {
                                    tempAlert(data['error'], 4000, 0);
                                }

                            },
                            failure: function () {
                                tempAlert('Error adding phase', 4000, 0);
                            }
                        });
                    } else {
                        selectElement.selectedIndex = i;
                        h.innerHTML = this.innerHTML;
                        y = this.parentNode.getElementsByClassName("same-as-selected");
                        yl = y.length;
                        for (k = 0; k < yl; k++) {
                            y[k].removeAttribute("class");
                        }
                        this.setAttribute("class", "same-as-selected");
                        if (target == 'custom-select-week') {
                            selectedWeek = selectElement.options[i].value;
                            getDays();
                            getDayData();

                        } else if (target == 'custom-select-phase') {
                            selectedPhase = selectElement.options[i].value;
                            getWeekDropdown();
                        }
                        break;
                    }
                }

            }
            h.click();
        });
        optionMenu.appendChild(option);
    }
    dropdown.appendChild(optionMenu);
    selectedElement.addEventListener('click', function (e) {
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
    })


}
function closeAllSelect(elmnt) {
    /* A function that will close all select boxes in the document,
    except the current select box: */
    var dropdown, y, i, xl, yl, arrNo = [];
    dropdown = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    xl = dropdown.length;
    yl = y.length;
    for (i = 0; i < yl; i++) {
        if (elmnt == y[i]) {
            arrNo.push(i)
        } else {
            y[i].classList.remove("select-arrow-active");
        }
    }
    for (i = 0; i < xl; i++) {
        if (arrNo.indexOf(i)) {
            dropdown[i].classList.add("select-hide");
        }
    }
}

document.addEventListener("click", closeAllSelect);