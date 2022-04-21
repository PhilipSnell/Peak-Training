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


// Alert accept popup
function tempAcceptAlert(msg) {
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

// ////////////////////////////////////////////////////////////
// Delete Entry

function deleteEntry(id, e) {

    // stops button press counting as edit entry press on row
    if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();


    $.ajax({
        type: "POST",
        url: "/dashboard/deleteentry/",
        data: {
            id: id,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            var x = document.getElementById("add-entry-modal");
            x.style.display = "none";
            if (data['success']) {
                $('#' + id).remove();
                tempAlert(data['success'], 4000, 1);
            } else {
                tempAlert(data['error'], 4000, 0);
                var target = ".addEntryButtonWrapper" + day;
                // console.log(target);
                $(data).insertBefore(target);
            }

        },
        failure: function () {
            tempAlert('Error deleting entry', 4000, 0);
        }
    });
}

// Style on hover
function startStyleHover() {
    $(".exerciseCellName").mouseover(function () {
        $(this).parent().css("border-radius", "2px");
        $(this).parent().css("border", "2px solid #787878");
    }).mouseout(function () {
        $(this).parent().css("border", "none");
        $(this).parent().css("border-radius", "0");
    });

    $(".deleteEntryButtonWrapper").mouseover(function () {
        $(this).parent().parent().css("border-bottom", "1px solid #787878");
    }).mouseout(function () {
        $(this).parent().parent().css("border-bottom", "none");
    });
}
startStyleHover();


// submit add entry
$('#addEntryForm').on('submit', function (e) {
    e.preventDefault();
    console.log($('#exercisefield').val())
    $.ajax({
        type: "GET",
        url: "/dashboard/addentry/",
        data: {
            phase: phase,
            week: week,
            day: day,
            exercise: $('#exercisefield').val(),
            reps: $('#repfield').val(),
            weight: $('#weightfield').val(),
            sets: $('#setfield').val(),
            comment: $('#commentfield').val(),
            csrfmiddlewaretoken: '{{ csrf_token }}',
            dataType: "json",
        },
        success: function (data) {
            var x = document.getElementById("add-entry-modal");
            x.style.display = "none";
            if (data['error']) {
                tempAlert(data['error'], 4000, 0);
            } else {

                var target = ".addEntryButtonWrapper" + day;
                // console.log(target);
                $(data).insertBefore(target);
                tempAlert("successfully added entry", 4000, 1);
                $('#exercisefield').val('');
                $('#repfield').val('');
                $('#weightfield').val('');
                $('#setfield').val('');
                $('#commentfield').val('');
            }


        },
        failure: function () {
            tempAlert('Error adding entry', 4000, 0);
        }

    });
});

function toggleAddEntry(clic_phase, clic_week, clic_day) {
    phase = clic_phase;
    week = clic_week;
    day = clic_day;
    var x = document.getElementById("add-entry-modal");
    if (x.style.display === "none" || !x.style.display) {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }
};
$('.close_addentry').on('click', function (e) {
    var x = document.getElementById("add-entry-modal");
    var y = document.getElementById("edit-entry-modal");
    x.style.display = "none";
    y.style.display = "none";
});


///////////////////////////////////////////////////////////////////////
// Custom Dropdown

// $('.navbar').append('<div class="custom-select" style="width:200px;"><select><option value="0">Select car:</option><option value="1">Audi</option><option value="2">BMW</option></select></div>')
if ($('.navbar').find('.custom-select-phase').length != 0) {
    $('.custom-select-phase').html('')
} else {
    $('.navbar').append('<div class="custom-select custom-select-phase"><select><option value="0" title="add phase">+</option></select></div>')
}

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
getPhaseDropdown();

if ($('.navbar').find('.custom-select-week').length != 0) {
    $('.custom-select-week').html('')
} else {
    $('.navbar').append('<div class="custom-select custom-select-week"><select><option value="0" title="add week">+</option></select></div>')
}
function updateTableTitle() {
    $('.contentTitle').html(`Phase ${selectedPhase} Week ${selectedWeek}`);
    $.ajax({
        type: "POST",
        url: '/dashboard/checkActiveWeek/',
        data: {
            phase: selectedPhase,
            week: selectedWeek,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            if (data['true']) {
                $('.toggleActiveIcon').attr('class', 'fas fa-toggle-on  toggleOn toggleActiveIcon')
                $('.toggleOff').on('click', function () {
                    tempAcceptAlert('Make this the active week?');
                });
            } else {
                $('.toggleActiveIcon').attr('class', 'fas fa-toggle-off toggleOff toggleActiveIcon')
                $('.toggleOff').on('click', function () {
                    tempAcceptAlert('Make this the active week?');
                });
            }
        }



    });

}

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
            updateTableTitle();
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
    for (index = 0; index < numberOfOptions; index++) {
        option = document.createElement('div');
        option.innerHTML = options[index].innerHTML;
        if (index == 0) {
            if (target == 'custom-select-week') {
                option.setAttribute('title', 'add week');
            } else if (target == 'custom-select-phase') {
                option.setAttribute('title', 'add phase');
            }

        }
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
                            updateTableTitle();
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
            week: selectedWeek
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
        url: '/dashboard/getDayData/',
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
                startStyleHover();
                monitorRowDrag();
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

$('.bg-modal').on('click', function (e) {
    if (e.target !== this)
        return;
    var clone = document.getElementById("clone-modal");
    var x = document.getElementById("add-entry-modal");
    var y = document.getElementById("edit-entry-modal");
    x.style.display = "none";
    y.style.display = "none";
    clone.style.display = 'none';
});

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);


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


// // reorder table
var table;


var draggingEle;
var draggingRowIndex;
var placeholder;
var list;
var isDraggingStarted = false;

// The current position of mouse relative to the dragging element
var x = 0;
var y = 0;

// Swap two nodes
swap = function (nodeA, nodeB) {
    const parentA = nodeA.parentNode;
    const siblingA = nodeA.nextSibling === nodeB ? nodeA : nodeA.nextSibling;

    // Move `nodeA` to before the `nodeB`
    nodeB.parentNode.insertBefore(nodeA, nodeB);

    // Move `nodeB` to before the sibling of `nodeA`
    parentA.insertBefore(nodeB, siblingA);
};

// Check if `nodeA` is above `nodeB`
isAbove = function (nodeA, nodeB) {
    // Get the bounding rectangle of nodes
    const rectA = nodeA.getBoundingClientRect();
    const rectB = nodeB.getBoundingClientRect();

    return rectA.top + rectA.height / 2 < rectB.top + rectB.height / 2;
};

cloneTable = function () {
    const rect = table.getBoundingClientRect();
    const width = parseInt(window.getComputedStyle(table).width);

    list = document.createElement('div');
    list.classList.add('clone-list');
    list.style.position = 'relative';
    // list.style.left = `${ rect.left } px`;
    // list.style.top = `${ rect.top } px`;
    table.parentNode.insertBefore(list, table);

    // Hide the original table
    table.style.display = 'none';

    table.querySelectorAll('tr').forEach(function (row) {
        // Create a new table from given row
        const item = document.createElement('div');
        item.classList.add('draggable');

        const newTable = document.createElement('table');
        newTable.setAttribute('class', 'clone-table');
        newTable.style.width = `${width}px`;

        const newRow = document.createElement('tr');
        const cells = [].slice.call(row.children);
        cells.forEach(function (cell) {
            const newCell = cell.cloneNode(true);
            newCell.style.width = cell.style.width;
            newRow.appendChild(newCell);
        });

        newTable.appendChild(newRow);
        item.appendChild(newTable);
        list.appendChild(item);
    });
};
mouseDownHandlerJ = function (e) {
    // Get the original row
    event.stopPropagation();
    const originalRow = e.parentNode;
    draggingRowIndex = [].slice.call(table.querySelectorAll('tr')).indexOf(originalRow);
    console.log(draggingRowIndex)
    // Determine the mouse position
    if (draggingRowIndex !== 0 && draggingRowIndex !== 1) {
        x = e.clientX;
        y = e.clientY;

        // Attach the listeners to `document`
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);

    }
};
mouseDownHandler = function (e) {
    // Get the original row
    event.stopPropagation();
    const originalRow = e.target.parentNode;
    draggingRowIndex = [].slice.call(table.querySelectorAll('tr')).indexOf(originalRow);
    console.log(draggingRowIndex)
    // Determine the mouse position
    if (draggingRowIndex !== 0 && draggingRowIndex !== 1) {
        x = e.clientX;
        y = e.clientY;

        // Attach the listeners to `document`
        var editwindow = document.getElementById("edit-entry-modal");
        console.log(editwindow.style.display);

        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);

    }
};


function mouseMoveHandler(e) {
    if (!isDraggingStarted) {
        isDraggingStarted = true;

        cloneTable();

        draggingEle = [].slice.call(list.children)[draggingRowIndex];
        draggingEle.classList.add('dragging');

        // Let the placeholder take the height of dragging element
        // So the next element won't move up
        placeholder = document.createElement('div');
        placeholder.classList.add('placeholder');
        draggingEle.parentNode.insertBefore(placeholder, draggingEle.nextSibling);
        placeholder.style.height = `${draggingEle.offsetHeight}px`;
    }

    // Set position for dragging element
    draggingEle.style.position = 'absolute';
    draggingEle.style.top = `${draggingEle.offsetTop + e.clientY - y}px`;
    draggingEle.style.left = `${draggingEle.offsetLeft + e.clientX - x}px`;

    // Reassign the position of mouse
    x = e.clientX;
    y = e.clientY;

    // The current order
    // prevEle
    // draggingEle
    // placeholder
    // nextEle
    const prevEle = draggingEle.previousElementSibling;
    const nextEle = placeholder.nextElementSibling;

    // The dragging element is above the previous element
    // User moves the dragging element to the top
    // We don't allow to drop above the header
    // (which doesn't have `previousElementSibling`)
    if (prevEle && prevEle.previousElementSibling && prevEle.previousElementSibling.previousElementSibling && isAbove(draggingEle, prevEle)) {
        // The current order    -> The new order
        // prevEle              -> placeholder
        // draggingEle          -> draggingEle
        // placeholder          -> prevEle
        swap(placeholder, draggingEle);
        swap(placeholder, prevEle);
        return;
    }

    // The dragging element is below the next element
    // User moves the dragging element to the bottom
    if (nextEle && nextEle.nextElementSibling && isAbove(nextEle, draggingEle)) {
        // The current order    -> The new order
        // draggingEle          -> nextEle
        // placeholder          -> placeholder
        // nextEle              -> draggingEle
        swap(nextEle, placeholder);
        swap(nextEle, draggingEle);
    }
};

function mouseUpHandler() {
    // Remove the placeholder
    placeholder && placeholder.parentNode.removeChild(placeholder);

    draggingEle.classList.remove('dragging');
    draggingEle.style.removeProperty('top');
    draggingEle.style.removeProperty('left');
    draggingEle.style.removeProperty('position');

    // Get the end index
    const endRowIndex = [].slice.call(list.children).indexOf(draggingEle);

    isDraggingStarted = false;

    // Remove the `list` element
    list.parentNode.removeChild(list);

    // Move the dragged row to `endRowIndex`
    let rows = [].slice.call(table.querySelectorAll('tr'));
    draggingRowIndex > endRowIndex
        ? rows[endRowIndex].parentNode.insertBefore(rows[draggingRowIndex], rows[endRowIndex])
        : rows[endRowIndex].parentNode.insertBefore(
            rows[draggingRowIndex],
            rows[endRowIndex].nextSibling
        );

    // Bring back the table
    table.style.display = "table";

    // Remove the handlers of `mousemove` and `mouseup`
    document.removeEventListener('mousemove', mouseMoveHandler);
    document.removeEventListener('mouseup', mouseUpHandler);
    var idOrder = [];
    table.querySelectorAll('tr.entryRow').forEach(function (row) {
        idOrder.push(row.id);
    });
    idOrder = JSON.stringify({ idOrder });
    $.ajax({
        type: "POST",
        url: "dashboard/changeOrder/",
        data: {
            idOrder: idOrder,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {

            if (data['success']) {
                tempAlert(data['success'], 4000, 1);
            } else {
                tempAlert("order not updated - refresh", 4000, 0);

            }

        },
        failure: function () {
            tempAlert('Error deleting entry', 4000, 0);
        }
    });
    console.log(idOrder);

};
function getRows() {
    table.querySelectorAll('tr').forEach(function (row, index) {
        // Ignore the header
        // We don't want user to change the order of header

        if (index === 0) {

        }
        else if (row.firstElementChild.id === "addentry") {


        }
        else {

            const firstCell = row.firstElementChild;
            firstCell.classList.add('draggable');
            firstCell.addEventListener('mousedown', mouseDownHandler);
        }
    });
};
function monitorRowDrag() {
    $('td.exerciseCell').mousedown(function () {
        event.stopPropagation();
        var tableId = $(this).parents("table").attr("id");

        table = document.getElementById(tableId);
        getRows();
        var cell = $(this).children("td").get(0);
        console.log(cell)
        mouseDownHandlerJ($(this).get(0));
    });
}
monitorRowDrag();
// //////////////////////////////////////////////////////////////
// Editing an entry 

function editEntry(name, reps, weight, sets, comment, id) {
    event.stopPropagation();
    var y = document.getElementById("edit-entry-modal");
    $('#editExerciseField').val(name);
    $('#editRepField').val(reps);
    $('#editWeightField').val(weight);
    $('#editSetField').val(sets);
    $('#editCommentField').val(comment);
    $('#idField').val(id);
    y.style.display = "flex";
}
// submit edit entry
$('#editEntryForm').on('submit', function (e) {
    e.preventDefault();
    var id = $('#idField').val();
    var exercise = $('#editExerciseField').val();
    var reps = $('#editRepField').val();
    var weight = $('#editWeightField').val();
    var sets = $('#editSetField').val();
    var comment = $('#editCommentField').val();
    $.ajax({
        type: "POST",
        url: "dashboard/editentry/",
        data: {
            id: id,
            exercise: exercise,
            reps: reps,
            weight: weight,
            sets: sets,
            comment: comment,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            if (data['success']) {
                tempAlert(data['success'], 4000, 1);
                htmlContents = `<td class='exerciseCell exerciseCellName draggable'>${exercise}</td><td class='editCell' onclick='editEntry("${exercise}","${reps}","${weight}","${sets}","${comment}","${id}")'>${reps}</td><td class='editCell' onclick='editEntry("${exercise}","${reps}","${weight}","${sets}","${comment}","${id}")'>${weight}</td><td class='editCell' onclick='editEntry("${exercise}","${reps}","${weight}","${sets}","${comment}","${id}")'>${sets}</td><td class='editCell' onclick='editEntry("${exercise}","${reps}","${weight}","${sets}","${comment}","${id}")'>${comment}</td><td style='width: 50px'><button class='deleteEntryButtonWrapper' type='button' name='button' onclick='deleteEntry(${id})'><div class='deleteEntryButton'>+</div></button></td>`;
                $(`#${id}.entryRow`).html(htmlContents);
                $('#idField').val('');
                $('#editExerciseField').val('');
                $('#editRepField').val('');
                $('#editWeightField').val('');
                $('#editSetField').val('');
                $('#editCommentField').val('');
            } else {
                tempAlert(data['error'], 4000, 0);
            }
            monitorRowDrag();
            startStyleHover();

        },
        failure: function () {
            tempAlert('Error deleting entry', 4000, 0);
        }
    });

    var x = document.getElementById("edit-entry-modal");
    x.style.display = "none";
});

// toggle confirmation

// // ---------------------------------------------------------------------------------------------------------------------
// clone week dropdown
function monitorClientClick() {
    $(".clientCloneOption").on('click', function (e) {
        clicked_client = $(this);
        console.log(clicked_client);
        if (clicked_client.hasClass('selectedOption')) {
            $('.cloneOptions').html(phaseOptionsHtml);
            $('.fa-user').parent().removeClass('selected-clone-icon');
            $('.fa-list').parent().addClass('selected-clone-icon');
            return
        } else {
            $('.clientCloneOption').each(function () {
                $(this).removeClass('selectedOption');
            });
            clicked_client.addClass('selectedOption');
            cloneClientHtml = $('.cloneOptions').html();
            selected_client = clicked_client.html()
            $.ajax({
                type: "POST",
                url: "/dashboard/getClonePhases/",
                data: {
                    selected_client: selected_client,
                    csrfmiddlewaretoken: csrf_token,
                    dataType: "json",
                },
                success: function (data) {

                    if (data['error']) {
                        tempAlert(data['error'], 4000, 0);
                    } else {

                        $('.cloneOptions').html(data);
                        phaseOptionsHtml = data;
                        $('.fa-user').parent().removeClass('selected-clone-icon');
                        $('.fa-list').parent().addClass('selected-clone-icon');
                    }

                },
                failure: function () {
                    tempAlert('Error deleting entry', 4000, 0);
                }
            });
        }
    });
}
$('.cloneWeekIcon').on('click', function (e) {
    e.preventDefault();
    var cloneOptions = document.getElementById("cloneOptionsWrapper");
    if (!cloneExpanded) {
        cloneOptions.style.display = "block";
        cloneExpanded = true;
        $('.innerCloneBox').css({ 'border-bottom-left-radius': '0px', 'border-bottom-right-radius': '0px' });
        $('.cloneWeek').css('background-color', '#D6D6D6')
    } else {
        cloneOptions.style.display = "none";
        cloneExpanded = false;
        $('.cloneWeek').css('background-color', 'transparent')
    }
});
// close clone dropdown
$(document).mouseup(function (e) {
    var container = $(".cloneWeek");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0 && cloneExpanded) {
        $('.cloneOptionsWrapper').css('display', 'none');
        container.css('background-color', 'transparent');
        cloneExpanded = false;
    }
});
$('.selectHeaderIconWrapper').on('click', function (e) {
    var clickedIcon = $(this)
    if (clickedIcon.hasClass('selected-clone-icon')) {
        return;
    } else {
        clickedIcon.addClass('selected-clone-icon');
        // console.log($('.fa-list:first-child').parent());
        if (clickedIcon.children(":first").hasClass('fa-user')) {

            $('.fa-list').parent().removeClass('selected-clone-icon');
            $('.cloneOptions').html(cloneClientHtml);
            monitorClientClick();
        } else {
            $('.fa-user').parent().removeClass('selected-clone-icon');
            $('.cloneOptions').html(phaseOptionsHtml);
        }
    }
})

function getDayPreview(phase, week) {
    $.ajax({
        type: "POST",
        url: '/dashboard/getDayData/',
        data: {
            phase: phase,
            week: week,
            client: selected_client,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            if (data['error']) {
                $('.alertPopupAccept').remove();
                tempAlert(data['error'], 4000, 0);
            } else {
                var preview = document.createElement('div')
                preview.setAttribute('class', 'bg-modal2')
                preview.style.zIndex = '0';
                document.body.appendChild(preview)
                $('.tableWrapper').html(data);
            }


        },
        failure: function () {
            $('.alertPopupAccept').remove();
            tempAlert('Could not load days!', 4000, 0);
        }

    })
};
// ---------------------------------------------------------------------------------------------------------------------
// clone confirmation

function cloneConfirmation(phase, week) {
    $('.cloneOptionsWrapper').css('display', 'none');
    $(".cloneWeek").css('background-color', 'transparent');
    cloneExpanded = false;
    getDayPreview(phase, week);
    var el = document.createElement("div");
    el.setAttribute("class", "alertPopupAccept");
    el.innerHTML = 'Accept the week clone as below?';
    el.style.zIndex = '1';
    el.style.width = '30%';
    el.style.marginLeft = '42.5%'
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
        $('.bg-modal2').remove();
        $(".alertPopupAccept").css('animation', 'slideC 1s');
        setTimeout(function () {
            $(".alertPopupAccept").remove();
        }, 1000);

        $.ajax({
            type: "POST",
            url: "/dashboard/cloneWeek/",
            data: {
                phaseTo: selectedPhase,
                weekTo: selectedWeek,
                phaseFrom: phase,
                weekFrom: week,
                selected_client: selected_client,
                csrfmiddlewaretoken: csrf_token,
                dataType: "json",
            },
            success: function (data) {
                if (data['error']) {
                    tempAlert(data['error'], 4000, 0);
                    getDays();
                    getDayData();

                } else {
                    $('.tableWrapper').html(data);
                    tempAlert('successfully cloned week!', 4000, 1);
                }

            },
            failure: function () {
                tempAlert('Error cloning week!', 4000, 0);
                getDayData();

            }
        });

    });
    $(".cancelToggle").on('click', function (e) {
        $('.bg-modal2').remove();
        $(".alertPopupAccept").css('animation', 'slideC 1s');
        setTimeout(function () {
            $(".alertPopupAccept").remove();
        }, 1000);
        getDayData();
    });
    // var y = document.getElementById("clone-modal");
    // y.style.display = "flex";

    // $('#cloneFromWeek').html('Week ' + week);
    // $('#cloneFromPhase').html('Phase ' + phase);
    // $('#cloneFromWeek').attr('name', week);
    // $('#cloneFromPhase').attr('name', phase);
    // $('#cloneToWeek').html('Week ' + selectedWeek[parseInt(selectedPhase) - 1]);
    // $('#cloneToPhase').html('Phase ' + selectedPhase);
};





    // var dayOptions = new Set();
    // // set last phase to selected color
    // var lastPhase = $('.phaseButton:nth-last-child(2)'); // second last phaseButton since the add button is also a phaseButton
    // lastPhase.css({ "background-color": "#787878", 'color': '#f4eb49' });
    // var selectedPhase = lastPhase.attr('id');

    // // ---------------------------------------------------------------------------------------------------------------------


    // // set if week or phase should be shown on page load

    // // ---------------------------------------------------------------------------------------------------------------------

    // // set last week to selected color

    // var selectedWeek = Array.apply(null, Array(parseInt(selectedPhase))).map(function () { });
    // console.log(selectedWeek);
    // setLastWeek();
    // function setLastWeek() {
    //     console.log(typeof selectedWeek[parseInt(selectedPhase) - 1] === 'undefined');
    //     if (typeof selectedWeek[parseInt(selectedPhase) - 1] === 'undefined') {
    //         var lastWeek = $("#" + selectedPhase + ".weekSelectorWrapper .weekButton:nth-last-child(2)"); // second last phaseButton since the add button is also a phaseButton
    //         lastWeek.css({ "background-color": "#787878", 'color': '#f4eb49' });
    //         weekSelected(lastWeek.attr('id'));
    //     }
    // }
    // // ---------------------------------------------------------------------------------------------------------------------
    // // delete Entry
    // //         function triggerMouseEvent (node, eventType) {
    // //             var clickEvent = document.createEvent ('MouseEvents');
    // //             clickEvent.initEvent (eventType, true, true);
    // //             node.dispatchEvent (clickEvent);
    // //         }


    // // ---------------------------------------------------------------------------------------------------------------------
    // // set content title to phase and week
    // setContentTitle();
    // var phaseTitle;
    // var weekTitle;
    // function setContentTitle() {
    //     if (typeof selectedPhase === 'undefined') {
    //         phaseTitle = 'Phase 0';
    //     } else {
    //         phaseTitle = 'Phase ' + selectedPhase;
    //     }
    //     if (typeof selectedWeek[parseInt(selectedPhase) - 1] === 'undefined') {
    //         weekTitle = ' Week 0';
    //     }
    //     else {
    //         weekTitle = ' Week ' + selectedWeek[parseInt(selectedPhase) - 1];
    //     }
    //     $('.contentTitle').html(phaseTitle + weekTitle);
    // }

    // // ---------------------------------------------------------------------------------------------------------------------
    // // display days table

    // function displayTable() {
    //     days = new Array();
    //     days = Array.from(dayOptions).sort();

    //     $('.dayTable').each(function () {
    //         $(this).css("display", "none");
    //     });
    //     for (index in days) {
    //         $('#Phase' + selectedPhase + 'Week' + selectedWeek[parseInt(selectedPhase) - 1] + 'Day' + days[index]).css("display", "block");
    //     }

    // }
    // // ---------------------------------------------------------------------------------------------------------------------
    // // display days option


    // function getDayOptions() {
    //     dayOptions = new Set();
    //     $('.dayOption').each(function () {
    //         $(this).css('display', 'none');
    //     })
    //     $('.OptionPhase' + selectedPhase + 'Week' + selectedWeek[parseInt(selectedPhase) - 1]).each(function () {
    //         option = $(this)
    //         option.css("display", "block");
    //         id = option.attr('id');
    //         option.css({ 'background-color': '#787878', 'color': '#f4eb49' });
    //         if (id !== 'button') {
    //             dayOptions.add(id);
    //         }
    //     })
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

    //     if (id !== selectedWeek[parseInt(selectedPhase) - 1]) {
    //         $('#' + id + '.weekButton' + selectedPhase).css({ "background-color": "#787878", 'color': '#f4eb49' });
    //         $('#' + selectedWeek[parseInt(selectedPhase) - 1] + '.weekButton' + selectedPhase).css({ "background-color": "#9C9C9C", 'color': 'black' });

    //         selectedWeek[parseInt(selectedPhase) - 1] = id;
    //         console.log(selectedWeek);
    //         setContentTitle();
    //         getDayOptions();
    //         displayTable();
    //         toggleActive();
    //     }

    // }
    // function toggleActive() {

    //     if ($('#' + selectedWeek[parseInt(selectedPhase) - 1] + '.weekButton' + selectedPhase).attr('name') === 'True') {


    //     }
    //     else {
    //         $('.toggleActiveIcon').removeClass('toggleOn');
    //         $('.toggleActiveIcon').removeClass('fa-toggle-on');
    //         $('.toggleActiveIcon').addClass('toggleOff');
    //         $('.toggleActiveIcon').addClass('fa-toggle-off');
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
    // // display modals




    // // ---------------------------------------------------------------------------------------------------------------------



    // // ---------------------------------------------------------------------------------------------------------------------

    // // ---------------------------------------------------------------------------------------------------------------------



    // $('#toggleWeekForm').on('submit', function (e) {
    //     e.preventDefault();


    //     var x = document.getElementById("toggle-modal");
    //     x.style.display = "none";
    // });