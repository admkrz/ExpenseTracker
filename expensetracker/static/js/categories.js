// While the Rename modal is showing set the old name field
$('#renameModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var category = button.data('category') // Extract info from data-* attributes
    var input = document.getElementById('old_name')
    var submit = document.getElementById('submitFormButton')
    submit.hidden = true
    input.value = category
    input.setAttribute("readOnly", true)

})

// As the Rename modal becomes hidden, clear the new name field
$('#renameModal').on('hide.bs.modal', function () {
    document.getElementById('new_name').value = ""
})

//Submit rename form on button click
$('#saveChanges').click(function () {
    document.getElementById('submitFormButton').click()
})

// While the delete modal is showing set the old name field and hide it
$('#deleteModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var category = button.data('category') // Extract info from data-* attributes
    var input = document.getElementById('item_to_delete')
    var submit = document.getElementById('deleteFormButton')
    submit.hidden = true
    input.value = category
    input.hidden = true
    var modal=$(this)
    modal.find('.modal-title').text("Delete category '" + category + "'")
})

//Submit rename form on button click
$('#btnDeleteCategory').click(function () {
    document.getElementById('deleteFormButton').click()
})