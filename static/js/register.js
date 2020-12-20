var btnSms = document.getElementById("btnSms");
var phone_number = document.getElementById("id_phone_number");
btnSms.onclick = function () {
    $(".err-msg").empty()

    $.ajax({
        url: 'send_sms/',
        type: 'POST',
        dataType: 'json',
        data: {'tpl': 'register', 'phone_number': phone_number.value}
    }).done(function (msg) {
        if (msg.status === 200000) {
            sendSmsRemind();
            console.log(msg.errmsg)
        } else {
            $("#id_" + msg.key).next().text(msg.errmsg)
        }
    }).fail(function () {
        alert('服务器访问失败，请稍后再试！')
    })
}

function sendSmsRemind() {
    var $smsBtn = $("#btnSms");
    $smsBtn.prop("disabled", true);
    var time = 60;
    var interval = setInterval(function () {
        $smsBtn.val(time + '秒后可重新发送');
        console.log($smsBtn.value);
        time = time - 1;
        if (time === 0) {
            clearInterval(interval);
            $smsBtn.val('点击获取验证码').prop('disabled', false);
        }
    }, 1000)
}