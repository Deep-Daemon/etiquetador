let allowedExtensions = ['json'];

$(function () {
    $('input:file').change(
        function () {
            if ($(this).val()) {
                let fileName = getExtensionFileName($(this).val());
                console.log(fileName);
                if (allowedExtensions.includes(fileName)) {
                    enableButtonSubmit(true);
                    $("#messages").html('');
                } else {
                    $("#messages").html('Archivo no permitido');
                    enableButtonSubmit(false);
                }
            }
        }
    );
});

function getExtensionFileName(filePath) {
    return filePath.substr(filePath.lastIndexOf('\\') + 1).split('.')[1].toLowerCase();
}

function enableButtonSubmit(value) {
    let submitButton = $('input:submit');
    submitButton.attr('disabled', !value);
}