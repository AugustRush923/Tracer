var btnSms = document.getElementById("btnSms");
var phone_number = document.getElementById("id_phone_number");
btnSms.onclick = function () {
    $(".err-msg").empty()

    $.ajax({
        url: '/user/send_sms/',
        type: 'POST',
        dataType: 'json',
        data: {'tpl': 'login', 'phone_number': phone_number.value}
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

var btnSubmit = document.getElementById("submit");
btnSubmit.onclick = function () {
    $(".err-msg").empty()
    var phone_number = document.getElementById("id_phone_number");
    if ($.isEmptyObject(phone_number.value)) {
        $("#id_phone_number").next().text("手机号不能为空")
    } else if (!(/^1[3456789]\d{9}$/.test(phone_number.value))) {
        $("#id_phone_number").next().text("手机号格式错误")
    }
    var code = document.getElementById("id_code");
    if ($.isEmptyObject(code.value)) {
        $("#id_code").next().text("验证码不能为空")
    }

    $.ajax({
        url: 'handler/',
        type: 'POST',
        dataType: "json",
        data: {
            "phone_number": phone_number.value,
            "code": code.value
        }
    }).done(function (msg) {
        $("#id_" + msg.key).next().text(msg.errmsg)
    }).fail(function () {
        alert('服务器访问失败，请稍后再试！')
    })
    console.log(phone_number.value, code.value);
}