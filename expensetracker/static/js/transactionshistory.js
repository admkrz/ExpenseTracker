$.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {
        var filter_category = $('#filterCategory').val();
        var row_category = data[2]; // use data for the age column

        if (filter_category === "all")
            return true;

        return filter_category === row_category;
    }
);

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    var target = $(".nav-link.active")
    var select = $('select.custom-select')
    console.log(target)
    console.log(target.data('transactions'))
    console.log(target.data('transactions') == 0)

    if (target.data('transactions') == 0) {
        $('#filterCategories').hide()
    }
    else
        $('#filterCategories').show()

    select.val("all")
});

$(document).ready(function () {
    var table = $('table.table').DataTable();

    $('select.custom-select').on('change', function () {
        table.draw();
    });

    var date_input = $('input[name="date"]'); //our date input has the name "date"
    var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
    var options = {
        format: 'yyyy-mm-dd',
        container: container,
        todayHighlight: true,
        autoclose: true,
        todayBtn: 'linked'
    };
    date_input.datepicker(options);
})

// While the Rename modal is showing set the old name field
$('#editModal').on('show.bs.modal', function (event) {
    if (event.namespace === 'bs.modal') {
        var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
        var button = $(event.relatedTarget) // Button that triggered the modal
        var budgetName = button.data('budget')
        var description = button.data('description')
        var category = button.data('category')
        var date = button.data('date')
        var amount = button.data('amount')
        var idValue = button.data('id')
        var budgetInput = document.getElementById('budget')
        var descriptionInput = document.getElementById('description')
        var categoryInput = document.getElementById('category')
        var dateInput = document.getElementById('date')
        var amountInput = document.getElementById('amount')
        var submit = document.getElementById('editTransaction')
        var id = document.getElementById('id')
        submit.hidden = true
        id.hidden = true
        budgetInput.value = budgetName
        descriptionInput.value = description
        categoryInput.value = category
        $('input[name="date"]').datepicker("setDate", date)
        dateInput.value = date
        amountInput.value = amount
        id.value = idValue
    }
})

//Submit rename form on button click
$('#saveChanges').click(function () {
    document.getElementById('editTransaction').click()
})

// While the delete modal is showing set the old name field and hide it
$('#deleteModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var id = button.data('id') // Extract info from data-* attributes
    var input = document.getElementById('item_to_delete')
    var submit = document.getElementById('deleteFormButton')
    submit.hidden = true
    input.value = id
    input.hidden = true
})

//Submit rename form on button click
$('#deleteTransaction').click(function () {
    document.getElementById('deleteFormButton').click()
})

