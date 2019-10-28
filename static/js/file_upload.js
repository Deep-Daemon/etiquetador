let allowedExtensions = ['zip', 'rar', '7z'];


$(function () {
    createAjaxForm();
});

$(function () {
    $('input:file').change(
        function () {
            if ($(this).val()) {
                let fileName = getFileName($(this).val());
                if (allowedExtensions.includes(fileName)) {
                    enableButtonSubmit(true);
                    $("#status").html('');
                } else {
                    $("#status").html('Archivo no permitido');
                    enableButtonSubmit(false);
                }
            }
        }
    );
});

$(function () {
    if (!$('input:file').val()) {
        enableButtonSubmit(false);
    }
});

function createAjaxForm() {
    let bar = $(".bar");
    let percent = $('.percent');
    let status = $("#status");

    $('form').ajaxForm({
        beforeSend: function () {
            status.empty();
            let percentVal = '0%';
            bar.width(percentVal);
            percent.html(percentVal);
        },
        uploadProgress: function (event, position, total, percentComplete) {
            let percentVal = percentComplete + '%';
            bar.width(percentVal);
            percent.html(percentVal);
            if (percentComplete === 100) {
                status.html('Se está procesando tu archivo, espera un momento');
            }
        },
        complete: function (xhr) {
            status.html(xhr.responseText);
        },
        clearForm: true,
        resetForm: true
    })
}

$(".custom-file-input").on("change", function () {
    let fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});


function enableButtonSubmit(value) {
    let submitButton = $('input:submit');
    submitButton.attr('disabled', !value);
}

function getFileName(filePath) {
    return filePath.substr(filePath.lastIndexOf('\\') + 1).split('.')[1].toLowerCase();
}

function getBack() {
    window.location = '/etiquetador';
}

function enableCancelButton(value) {
    $('#cancelButton').attr('disabled', !value);
}

function cancelUpload() {
    let form = $('#formFile').ajaxForm();
    let xhr = form.data('jqxhr');
    xhr.abort();
    $(".bar").width(0);
    $('.percent').html('');
    enableCancelButton(false);
    createAjaxForm();
}