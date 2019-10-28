$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

function submit(file_name, path){
	$("#file_name").val(file_name)
	$("#path").val(path)
	$('#form').submit();
}