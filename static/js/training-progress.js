
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

// console.log(`phase: ${selectedPhase}`);
// console.log(`week: ${selectedWeek}`)

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
function getDays() {

    $.ajax({
        type: "GET",
        url: '/dashboard/getDays/',
        data: {
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
var cloneExpanded = false;
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


// var phase = 0;
// var week = 0;
// var day = 0;
// function loadState(id) {
//     var value = localStorage.getItem(id);
//     var x = document.getElementById(id);
//     x.style.display = value;
// }
// function hideItem(id) {

//     var x = document.getElementById(id);
//     var value

//     if (x.style.display === "none" || x.style.display === "") {
//         value = "block";
//     } else {
//         value = "none";
//     }
//     x.style.display = value;
//     localStorage.setItem(id, value)
// }
// function hideTable(id) {
//     var x = document.getElementById(id);
//     if (x.style.display === "none" || x.style.display) {
//         x.style.display = "table";
//     } else {
//         x.style.display = "none";
//     }
// }
// function toggleAddEntry(clic_phase, clic_week, clic_day) {
//     phase = clic_phase;
//     week = clic_week;
//     day = clic_day;
//     var x = document.getElementById("add-entry-modal");
//     if (x.style.display === "none" || !x.style.display) {
//         x.style.display = "flex";
//     } else {
//         x.style.display = "none";
//     }
// };




// // ---------------------------------------------------------------------------------------------------------------------


// // set last week to selected color

// var selectedWeek;



// // ---------------------------------------------------------------------------------------------------------------------
// // display days table

// function displayTable() {
//     days = new Array();
//     days = Array.from(dayOptions).sort();

//     $('.dayTable').each(function () {
//         $(this).css("display", "none");
//     });
//     for (index in days) {
//         $('#Phase' + selectedPhase + 'Week' + selectedWeek + 'Day' + days[index]).css("display", "block");
//     }

// }
// // ---------------------------------------------------------------------------------------------------------------------
// // display days option

// getDayOptions();
// function getDayOptions() {
//     dayOptions = new Set();
//     $('.dayOption').each(function () {
//         $(this).css('display', 'none');
//     })
//     $('.OptionPhase' + selectedPhase + 'Week' + selectedWeek).each(function () {
//         option = $(this)
//         option.css("display", "block");
//         id = option.attr('id');
//         option.css({ 'background-color': '#787878', 'color': '#f4eb49' });
//         if (id !== 'button') {
//             dayOptions.add(id);
//         }
//     })
//     if (dayOptions.size === 0) {
//         $('.multiselect').css('display', 'none');
//     }
//     else {
//         $('.multiselect').css('display', 'inline-block');
//     }
// }
// // ---------------------------------------------------------------------------------------------------------------------
// // phase/week button clicked

// function phaseClicked() {
//     if (!phaseStatus) {
//         // change the button color
//         $('.selectPhaseButton').css({ "background-color": "#787878", 'color': '#f4eb49' });
//         $('.selectWeekButton').css({ "background-color": "#9C9C9C", 'color': 'black' });
//         phaseStatus = true;
//         // change from weeks to phases
//         $('.weekSelectorWrapper').css("display", "none");
//         $('.phaseSelectorWrapper').css("display", "inline-block");

//     }

// }
// function weekClicked() {
//     if (phaseStatus) {
//         //set the last week to be active

//         // change the button color
//         $('.selectPhaseButton').css({ "background-color": "#9C9C9C", 'color': 'black' });
//         $('.selectWeekButton').css({ "background-color": "#787878", 'color': '#f4eb49' });
//         phaseStatus = false;
//         // change from phase to weeks
//         $('.phaseSelectorWrapper').css("display", "none");
//         $('#' + selectedPhase + '.weekSelectorWrapper').css("display", "inline-block");

//     }
// }
// // ---------------------------------------------------------------------------------------------------------------------

// // selecting phase
// function phaseSelected(id) {
//     if (id != selectedPhase) {
//         $('#' + id + '.phaseButton').css({ "background-color": "#787878", 'color': '#f4eb49' });
//         $('#' + selectedPhase + '.phaseButton').css({ "background-color": "#9C9C9C", 'color': 'black' });
//         selectedPhase = id;
//         setLastWeek();
//         setContentTitle();
//         getDayOptions();
//         displayTable();
//     }
//     weekClicked();
// }

// // ---------------------------------------------------------------------------------------------------------------------
// // selecting week
// function weekSelected(id) {
//     if (id != selectedWeek) {
//         $('#' + id + '.weekButton' + selectedPhase).css({ "background-color": "#787878", 'color': '#f4eb49' });
//         $('#' + selectedWeek + '.weekButton' + selectedPhase).css({ "background-color": "#9C9C9C", 'color': 'black' });

//         selectedWeek = id;
//         setContentTitle();
//         getDayOptions();
//         displayTable();

//     }
// }

// // ---------------------------------------------------------------------------------------------------------------------
// // day select box
// var expanded = false;

// function showCheckboxes() {
//     var checkboxes = document.getElementById("checkboxes");
//     if (!expanded) {
//         checkboxes.style.display = "block";
//         expanded = true;
//         $('.innerSelectBox').css({ 'border-bottom-left-radius': '0px', 'border-bottom-right-radius': '0px' });
//     } else {
//         checkboxes.style.display = "none";
//         expanded = false;
//         $('.innerSelectBox').css("border-radius", "5px");
//     }
// }

// function dayClicked(elem) {
//     dayOption = $(elem);
//     if (dayOptions.length !== 0) {
//         id = dayOption.attr('id');
//         if (dayOptions.has(id)) {
//             dayOptions.delete(id);
//             dayOption.css({ 'background-color': '#888888', 'color': 'black' });
//         }
//         else {
//             dayOption.css({ 'background-color': '#787878', 'color': '#f4eb49' });
//             dayOptions.add(id);
//         }
//     }
//     else {
//         dayOption.css({ 'background-color': '#787878', 'color': '#f4eb49' });
//         dayOptions.add(id);
//     }
//     displayTable();
// }
// // ---------------------------------------------------------------------------------------------------------------------
