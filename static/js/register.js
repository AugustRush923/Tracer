var btnSms = document.getElementById("btnSms");
var phone_number = document.getElementById("id_phone_number");
btnSms.onclick = function () {
    $.ajax({
        url: 'send_sms/',
        type: 'POST',
        dataType: 'json',
        data: {'tpl': 'register', 'phone_number': phone_number.value}
    }).done(function (errmsg) {
        alert('ajax调用成功！')
    }).fail(function () {
        alert('服务器访问失败，请稍后再试！')
    })
}