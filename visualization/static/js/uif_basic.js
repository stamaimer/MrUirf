function print_error(error_str){
    $("#error-screen a").html(error_str)
    $("#error-screen a").css('color', "#fff")
    $("body>nav").css('background-color', '#d9534f')
    $("body>nav").css('border-color', '#d43f3a')
}

function clear_error(){
    $("#error-screen a").empty()
    $("body>nav").css('background-color', '#222')
    $("body>nav").css('border-color', '#080808')
}

// disable submit button
$('button[type="submit"]').focus(function(){
    select_value = $("select[name='user_id']").val()
    if(select_value=='0'){
        err= "<span class='glyphicon glyphicon-remove'></span>"
        err+="&nbsp;Please select user!"
        print_error(err)
        $(this).attr("disabled", "disabled")
    }
    else clear_error()
})
// reuse submit button
$('select[name="user_id"]').click(function(){
    $("button[type='submit']").removeAttr('disabled')
})
//active tooltip
$('[data-toggle="tooltip"]').tooltip();
//active popover
$('[data-toggle="popover"]').popover();
