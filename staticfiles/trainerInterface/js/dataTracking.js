var x = document.getElementById("add-entry-modal");
x.style.display = "none";
var activeindex = 0;
var addFieldCount = 0;
var activeState;
function toggleAddEntry() {
    var x = document.getElementById("add-entry-modal");
    if (x.style.display === "none" || x.style.display) {
      x.style.display = "flex";
    } else {
      x.style.display = "none";
    }
}
var y = document.getElementById("edit-group-modal");
y.style.display = "none";
function toggleEditEntry(index) {
    activeindex = index
    console.log(activeindex);

    var x = document.getElementById("edit-group-modal");


    if (x.style.display === "none" || x.style.display) {
        x.style.display = "flex";
    } else {
        x.style.display = "none";
    }
    var y = document.getElementById("edit-group-form-" + index);
    if (y.style.display === "none" || y.style.display) {
        y.style.display = "block";
    } else {
        y.style.display = "none";
    }



}

function changeFieldToggle(elem) {

    if (elem.innerHTML==='<i class="fas fa-toggle-on" style="color: green" aria-hidden="true"></i>') {
        elem.innerHTML='<i class="fas fa-toggle-off" style="color: darkred" aria-hidden="true"></i>';

    }
    else {
        elem.innerHTML ='<i class="fas fa-toggle-on" style="color: green" aria-hidden="true"></i>';
    }
}
$('.close_addentry').on('click', function(e) {
    var x = document.getElementById("add-entry-modal");
    x.style.display = "none";
    var y = document.getElementById("edit-group-modal");
    y.style.display = "none";

    var z = document.getElementById("edit-group-form-"+activeindex);
    z.style.display = "none";
  //toggleEditEntry(activeindex);
});
function removeDiv(elem){
    var parent = $(elem).parent().parent().parent().parent();
    if (parent.attr("id") !== "field-0") {
        parent.remove();
    }

}
function removeDivEdit(elem){
    // elem.style.display = "none";

    var table = $(elem).parent().parent().parent().parent();
    table.css('display','none');
    var curID = table.attr("id");
    table.attr("id",curID+"-delete");

}

$('.bg-modal').on('click', function(e) {
  if (e.target !== this)
    return;
  var x = document.getElementById("add-entry-modal");
  x.style.display = "none";
  var y = document.getElementById("edit-group-modal");
  y.style.display = "none";
  var z = document.getElementById("edit-group-form-"+activeindex);
  z.style.display = "none";
});
$('.add_field_button').on('click', function(e) {
  e.preventDefault();
  var x = $("#fields");
  var table = $("#field-0").clone(true);

  addFieldCount = addFieldCount + 1;
  newID = "field-"+addFieldCount;
  table.find('#fieldname').at = "";
  table.attr("id",newID);
  table.appendTo(x)
});
$('.add_field_button1').on('click', function(e) {
  e.preventDefault();

  var x = $("#editfields-"+activeindex);
  var table = $("#field-0").clone(true);

  addFieldCount = addFieldCount + 1;
  newID = '';
  table.attr("id",newID);
  table.find('#fieldname').value = "";
  table.find('#fieldname').attr("id","editfieldname");
  table.find('#fieldSelect').attr("id","editfieldSelect");
  table.find('#fieldToggle').attr("class", "editfieldToggle editfieldToggle-"+activeindex);
  table.appendTo(x)
});
$('.add-group-form').on('submit', function(e){
 e.preventDefault();

    var fieldnames = $("[id=fieldname]").map(function() {
        return $(this).val();
    }).get();
    var classifications = $("[id=fieldSelect]").map(function() {
        return $(this).val();
    }).get();

    var toggleElem = document.getElementsByClassName("fieldToggle");;
    var toggles = [];
    for (let i = 0; i < toggleElem.length; i++) {
        console.log(toggleElem[i].innerHTML)
        if (toggleElem[i].innerHTML.includes('green')) {
            toggles.push('True');
        } else {
            toggles.push('False');
        }
    }
    fieldnames = JSON.stringify({fieldnames });
    classifications = JSON.stringify({classifications });
    toggles = JSON.stringify({toggles });
   $.ajax({
        type : "POST",
        url: "{% url 'add_group' %}",
        data: {

         name : $('#groupname').val(),
         fieldnames: fieldnames,
         classifications: classifications,
         toggles: toggles,
         csrfmiddlewaretoken: '{{ csrf_token }}',
         dataType: "json",
        },
        success: function(data){
            location.reload();
        },
        failure: function() {
        }
    });

   window.location.reload();
   var x = document.getElementById("add-entry-modal");
   x.style.display = "none";
});
$('.submit-edit-button').on('click', function(f) {

    var fieldnames = [];

    $("#edit-group-form-" + activeindex).find("[id^=editfieldname]").each(function() {
        fieldnames.push($(this).val());
    });
    var fieldIds = [];

    $("#edit-group-form-" + activeindex).find(".addGroupTable").each(function() {
        fieldIds.push($(this).attr('id'));
    });
    var classifications = [];
    $("#edit-group-form-" + activeindex).find("[id^=editfieldSelect]").each(function() {
        classifications.push($(this).val());
    });


    var toggleElem = document.getElementsByClassName("editfieldToggle-"+activeindex);
    var toggles = [];
    for (let i = 0; i < toggleElem.length; i++) {
        if (toggleElem[i].innerHTML.includes('green')) {
            toggles.push('True');
        } else {
            toggles.push('False');
        }
    }
    console.log($('.edit-group-name-'+activeindex).attr('id'));

    fieldnames = JSON.stringify({fieldnames });
    fieldIds = JSON.stringify({fieldIds });
    classifications = JSON.stringify({classifications });
    toggles = JSON.stringify({toggles });
   $.ajax({
        type : "POST",
        url: "{% url 'edit_group' %}",
        data: {

         name : $('.edit-group-name-'+activeindex).val(),
         groupId : $('.edit-group-name-'+activeindex).attr('id'),
         fieldIds : fieldIds,
         fieldnames: fieldnames,
         classifications: classifications,
         toggles: toggles,
         csrfmiddlewaretoken: '{{ csrf_token }}',
         dataType: "json",
        },
        success: function(data){
            {#location.reload();#}
        },
        failure: function() {
        }
    });

   window.location.reload();
   var x = document.getElementById("edit-group-modal");
   x.style.display = "none";
});