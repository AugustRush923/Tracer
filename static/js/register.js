var btnSms = document.getElementById("btnSms");
var phone_number = document.getElementById("id_phone_number");
btnSms.onclick = function () {
    // $(".err-msg").empty()

    $.ajax({
        url: 'send_sms/',
        type: 'POST',
        dataType: 'json',
        data: {'tpl': 'register', 'phone_number': phone_number.value}
    }).done(function (msg) {
        console.log(msg)
        if (msg.status == 200000) {
            console.log(msg.errmsg)
        } else {
            $("#id_"+ msg.key).next().text(msg.errmsg)
        }
    }).fail(function () {
        alert('服务器访问失败，请稍后再试！')
    })
}