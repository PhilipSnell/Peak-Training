
// add tools to navbar
navbar = $('.navbar');
week = 0;
var today = new Date();
today.setHours(0, 0, 0, 0);
console.log(today);
var week_start = new Date(today);
week_start.setDate(week_start.getDate() - week_start.getDay() + 1)
console.log(week_start);
var week_end = new Date(today);
week_end.setDate(week_end.getDate() - week_end.getDay() + 7)
console.log(week_end);


if (navbar.find('.exercise-tools').length != 0) {
    $('.exercise-tools').html('')
} else {

    tools = $('<div></div>').attr({
        'class': 'exercise-tools',
    });
    tools.appendTo(navbar);
    week_selector = $('<div></div>').attr({
        'class': 'graph-week-selector',
    });
    week_selector.appendTo(tools);
    left_arrow = $('<i class="fa-solid fa-chevron-left"></i>');
    left_arrow.appendTo(week_selector);
    week_display = $('<div>This Week</div>').attr({
        'class': 'week-display',
    });
    week_display.appendTo(week_selector);
    right_arrow = $('<i class="fa-solid fa-chevron-right"></i>');
    right_arrow.hide();
    right_arrow.appendTo(week_selector);

}
$('.fa-chevron-right').on('click', function () {
    if (week < 0) {
        week += 1;
        week_start.setDate(week_start.getDate() + 7);
        week_end.setDate(week_end.getDate() + 7);
        updateWeekText();
    }

});
$('.fa-chevron-left').on('click', function () {
    week -= 1;
    week_start.setDate(week_start.getDate() - 7);
    week_end.setDate(week_end.getDate() - 7);
    updateWeekText();
});
const months = {
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

const nth = function (d) {
    if (d > 3 && d < 21) return 'th';
    switch (d % 10) {
        case 1: return "st";
        case 2: return "nd";
        case 3: return "rd";
        default: return "th";
    }
}
function updateWeekText() {

    start_date = week_start.getDate();
    start_month = week_start.getMonth();
    start_string = `${start_date}${nth(start_date)} ${months[start_month]}`;

    end_date = week_end.getDate();
    end_month = week_end.getMonth();
    end_string = `${end_date}${nth(end_date)} ${months[end_month]}`;
    if (week == 0) {
        right_arrow.hide();
        week_display.text('This Week');
    } else if (week == -1) {
        right_arrow.show();
        week_display.text('Last Week');
    } else {
        week_display.text(`${start_string} - ${end_string}`);
    }
    getGraphData()

}

if ($('.exercise-tools').find('.custom-select-data').length != 0) {
    $('.custom-select-data').html('')
} else {
    $('.exercise-tools').prepend('<div class="custom-select custom-select-data"><select></select></div>')
}

function getData() {
    date = week_start.getDate();
    month = week_start.getMonth() + 1;
    year = week_start.getFullYear();
    formatted = `${date}/${month}/${year}`;
    $.ajax({
        type: "GET",
        url: '/dashboard/getdata/',
        data: {
            date: formatted,
        },
        success: function (data) {
            $('.custom-select-data').html(data);
            handleDropdown('custom-select-data');

        }


    })
}
getData();
function handleDropdown(target) {
    var dropdown, options, option, numberOfOptions, selectedOption, selectedElement, optionMenu, index
    dropdown = document.getElementsByClassName(target)[0];
    options = dropdown.getElementsByTagName("select")[0].options;
    numberOfOptions = dropdown.getElementsByTagName("select")[0].length;
    selectedElement = document.createElement("div");
    selectedElement.setAttribute('class', 'select-selected');
    if (numberOfOptions > 0) {
        selectedOption = options[0]
        if (target == 'custom-select-week') {
            selectedWeek = options[0].value;
        } else if (target == 'custom-select-phase') {
            selectedPhase = options[0].value;
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

        option.setAttribute('value', options[index].value);
        option.addEventListener('click', function () {
            var y, i, k, h, yl;
            var selectElement = dropdown.getElementsByTagName("select")[0];
            h = this.parentNode.previousSibling;
            for (i = 0; i < numberOfOptions; i++) {

                if (options[i].innerHTML == this.innerHTML) {

                    selectElement.selectedIndex = i;
                    h.innerHTML = this.innerHTML;
                    y = this.parentNode.getElementsByClassName("same-as-selected");
                    yl = y.length;
                    for (k = 0; k < yl; k++) {
                        y[k].removeAttribute("class");
                    }
                    this.setAttribute("class", "same-as-selected");
                    getGraphData();


                }

            }
            h.click();
        });
        optionMenu.appendChild(option);
    }
    dropdown.appendChild(optionMenu);
    getGraphData();
    selectedElement.addEventListener('click', function (e) {
        e.stopPropagation();
        closeAllSelect(this);
        this.nextSibling.classList.toggle("select-hide");
        this.classList.toggle("select-arrow-active");
    })
}


function getGraphData() {
    date = week_start.getDate();
    month = week_start.getMonth() + 1;
    year = week_start.getFullYear();
    formatted = `${date}/${month}/${year}`;
    console.log(formatted);
    $.ajax({
        type: "POST",
        url: '/dashboard/getGraphData/',
        data: {
            option: $(".select-selected").text(),
            date: formatted,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            if (data['error']) {
                tempAlert(data['error'], 4000, 0);
            } else {
                console.log(data['data']);
                console.log(data['positions']);
                $('.data-point').each(function (index) {
                    if (data['positions'][index] == '0') {
                        $(this).css('visibility', 'hidden');
                    } else {
                        // $(this).css('--yPos', '0');
                        // $(this).css('--xPos', `${(index * 10) + 40}%`);
                        $(this).css('--xPos', data['positions'][index]);
                        $(this).find('.data-label').text(data['data'][index])
                    }
                })
                $('.label-value').each(function (index) {
                    $(this).text(data['display'][index]);
                })
                $('.data-point').on('mouseover', function () {
                    $(this).find('.data-label').stop(true, true).slideToggle();
                })
                $('.data-point').on('mouseout', function () {
                    $(this).find('.data-label').stop(true, true).slideToggle();
                })
            }
        },
        failure: function () {
            tempAlert('Could not load data!', 4000, 0);
        }
    })
};

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