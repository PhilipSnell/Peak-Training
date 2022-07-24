
// add tools to navbar
navbar = $('.navbar');
week = 0;
var today = new Date();
today.setHours(0, 0, 0, 0);

var week_start = new Date(today);
if (week_start.getDay() === 0) {
    week_start.setDate(week_start.getDate() - 6)
} else {
    week_start.setDate(week_start.getDate() - week_start.getDay() + 1)
}
var week_end = new Date(today);
week_end.setDate(week_start.getDate() + 6)

if (navbar.find('.graph-tools').length != 0) {
    $('.graph-tools').html('')
} else {
    tools = $('<div></div>').attr({
        'class': 'graph-tools',
    });
    tools.appendTo(navbar);
    week_selector = $('<div></div>').attr({
        'class': 'graph-week-selector',
    });
    week_selector.appendTo(tools);
    left_arrow = $('<i class="fa-solid fa-chevron-left left-week"></i>');
    left_arrow.appendTo(week_selector);
    week_display = $('<div>This Week</div>').attr({
        'class': 'week-display',
    });
    week_display.appendTo(week_selector);
    right_arrow = $('<i class="fa-solid fa-chevron-right right-week"></i>');
    right_arrow.hide();
    right_arrow.appendTo(week_selector);
    $('.graph-tools').prepend('<div class="custom-select custom-select-data"><select></select></div>')
}



$('.right-week').on('click', function () {
    if (week < 0) {
        week += 1;
        week_start.setDate(week_start.getDate() + 7);
        week_end.setDate(week_end.getDate() + 7);
        updateWeekText();
        getGraphData();
        handleGraph();
    }
});
$('.left-week').on('click', function () {
    week -= 1;
    week_start.setDate(week_start.getDate() - 7);
    week_end.setDate(week_end.getDate() - 7);
    updateWeekText();
    getGraphData();
    handleGraph();
});




nth = function (d) {
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

}

if ($('.exercise-tools').find('.custom-select-data').length != 0) {
    $('.custom-select-data').html('')
} else {

}
function getFields(group) {
    $.ajax({
        type: "GET",
        url: '/dashboard/getfields/',
        data: {
            session_id: sessionStorage.getItem("session_id"),
            group: group,
        },
        success: function (data) {
            $('.field-options').html(data);
            $('.field-checkbox').each(function(index){
                $(this).css({'accent-color':`${colors[index]}`});
                $(this).css({'color':`${colors[index]}`});
                $(this).css({'background-color':`${colors[index]}`});
            });
            getGraphData();
            $('.field-checkbox').on('click', function() {
                handleGraph();
            });
        }
    })
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
            session_id: sessionStorage.getItem("session_id"),
            date: formatted,
        },
        success: function (data) {
            $('.custom-select-data').html(data);
            handleDropdown('custom-select-data');
            group = $('.custom-select-data').find(':selected').val();
            getFields(group);
        }

    })
}
getData();

$('.fields-tab').on('click', function () {
    if (!$('.field-options').html()) {
        $('.side-content').animate({ width: 'toggle' });

    }
    // group = $('.custom-select-data').find(':selected').val();
    // getFields(group);
    $('.side-content').animate({ width: 'toggle' });
})

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
                    group = $('.custom-select-data').find(':selected').val();
                    getFields(group);

                }

            }
            h.click();
            handleGraph();
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
};

var data_vals;
var y_axis;
var x_axis = ['6.3%','20.5%','34.7%','48.9%','63.1%','77.3%','91.5%']
var data_y_pos;
var colors = ['#fcba03','#fc7f03', '#aed656', '#56d6b0', '#54a1d1', '#8454d1', '#bc54d1', '#cc769a']
var selected_y_axis = 0;
var empty_y_axis = ['', '', '', '', '', '', '', '', '', ''];
function handleGraph() {
    $('.data-point').each(function(){
        $(this).parent().remove();
    })
    $('.field-checkbox').each(function (index) {
        if ($(this).is(':checked')) {
            if (index === selected_y_axis){
                if (JSON.stringify(y_axis[selected_y_axis]) == JSON.stringify(empty_y_axis)){
                    raise_Y_index();
                }
                else{

                    set_y_axis(y_axis[index], index);
                    
                }
                
            }
            set_data_points(data_vals[index],data_y_pos[index],index);
        }
        else{
            if (index === selected_y_axis){
                raise_Y_index();
            }
            set_data_points(['','','','','','',''], ["0","0","0","0","0","0","0"],index);
        }
    });
};

$('.right-y').on('click', function () {
    find_higher();
});
$('.left-y').on('click', function () {
    find_lower();
});
function find_higher(){
    original_index = selected_y_axis;
    while (true){
        raise_Y_index();
        if (selected_y_axis == original_index) break;
        if (JSON.stringify(y_axis[selected_y_axis]) != JSON.stringify(empty_y_axis)) break;
    }
    handleGraph();
};
function find_lower(){
    original_index = selected_y_axis;
    while (true){
        
        lower_Y_index();
        if (selected_y_axis == original_index) break;
        if (JSON.stringify(y_axis[selected_y_axis]) != JSON.stringify(empty_y_axis)) break;
    }
    handleGraph();
};
function raise_Y_index(){
    selected_y_axis +=1;
    if (selected_y_axis === $('.field-checkbox').length) selected_y_axis=0;
}
function lower_Y_index(){
    selected_y_axis -=1;
    if (selected_y_axis < 0) selected_y_axis = $('.field-checkbox').length-1;
}

function set_y_axis(vals,i) {
    $('.label-value').each(function (index) {
        $(this).text(vals[index]);
    })
    $('.color-marker').css('background-color',`${colors[i]}`);
};
function remove_data_points(){
    $('.data-point').each(function(){
        $(this).parent().remove();
    })
}

// new ResizeObserver(handleGraph).observe($());
function set_data_points(vals, y_pos, index) {
    for(let i=0; i< vals.length; i++){
        item = $("<li>");
        div = $("<div>");
        div.attr('class','data-point');
        div.css({'left':`calc(${x_axis[i]} - 7px)`,'bottom':`0`});
        label = $("<div>").text(vals[i]);
        label.attr('class','data-label');
        label.css({'left':`calc(${x_axis[i]} + 7px)`,'bottom':`0`,'display':'none'});
        if (y_pos[i] !== "0"){
            div.css({'bottom':`calc(${y_pos[i]} - 7px)`,'background-color':`${colors[index]}`});
            label.css({'bottom':`calc(${y_pos[i]} + 7px)`,'background-color':`${colors[index]}`});
        }
        else{
            div.css({'display':'none'});
            label.css({'display':'none'});
        }
        
        line = $("<div>");
        line.attr('class','line-segment');
        item.append(div);
        item.append(label);
        if (i+1 < vals.length){
            var found_point =false
            for(let j=i+1; j<vals.length; j++){
                if(vals[j] != ''){
                    var x = (j-i)*14.2;
                    var y = parseInt(y_pos[j])-parseInt(y_pos[i]);
                    found_point = true
                    break;
                }
            }
            if (found_point){
                var graph_width = $('.graphContent').width();
                var graph_height = $('.graphContent').height();
                x = graph_width*(x/100);
                y = graph_height*(y/100);
                h = Math.sqrt(x*x+y*y)
                
                angle = -Math.asin(y/h)*(180/Math.PI);
                h = (h/graph_width)*100;
                line.css({'width':`${h}%`});
                line.css({'left':`calc(${x_axis[i]})`,'bottom':`0`,'transform':`rotate(calc(${angle}deg))`,'transform-origin': 'left bottom','background-color':`${colors[index]}`});
                if (y_pos[i] !== "0"){
                    line.css({'bottom':`calc(${y_pos[i]})`});
                }
                else{
                    line.css({'display':'none'});
                }
                item.append(line);
            }
        }
        
        // console.log(angle);
        // }
        
        
        
        $(".line-chart").append(item);
        showLabels();
    }
    // $('.label-value').each(function (index) {
    //     $(this).text(vals[index]);
    // })
};

function showLabels(){
    $('.data-point').mouseenter( function(){
        $(this).parent().find('.data-label').css('display','block');
    }).mouseleave( function(){
        $(this).parent().find('.data-label').css('display','none');
    });
}

function getGraphData() {

    date = week_start.getDate();
    month = week_start.getMonth() + 1;
    year = week_start.getFullYear();
    formatted = `${date}/${month}/${year}`;


    $('.data-point').each(function (index) {
        $(this).css('visibility', 'hidden');
    })
    fields = [];
    $('.field-checkbox').each(function () {
        fields.push($(this).attr('id'));
    })
    fields = JSON.stringify({ fields });
    
    $.ajax({
        type: "POST",
        url: '/dashboard/getGraphData/',
        data: {
            session_id: sessionStorage.getItem("session_id"),
            fields: fields,
            date: formatted,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",
        },
        success: function (data) {
            
            if (data['error']) {
                $('.alertWait').slideUp(600);
                tempAlert(data['error'], 4000, 0);
            } else {
                data_vals = data['datavals'];
                y_axis = data['y_axis'];
                data_y_pos = data['data_y_pos'];
                $('.alertWait').slideUp(600);
                handleGraph();
                content = document.querySelector(".graphContent");
                ResizeSensor(content, function(){ 
                    handleGraph();
                });
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

// Alert popup
function waitAlert(msg, duration) {
    var el = document.createElement("div");
    el.setAttribute("class", "alertWait");
    el.innerHTML = msg;
    document.body.appendChild(el);
}

// side options //

// $(".fields").on('click', function () {

// })