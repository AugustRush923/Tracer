var btnSms = document.getElementById("btnSms");
var phone_number = document.getElementById("id_phone_number");
btnSms.onclick = function () {
    $(".err-msg").empty()

    $.ajax({
        url: '/user/send_sms/',
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

var btnSubmit = document.getElementById("submit");
btnSubmit.onclick = function () {
    $(".err-msg").empty()
    var username = document.getElementById("id_username");
    if ($.isEmptyObject(username.value)) {
        $("#id_username").next().text("用户名不能为空")
    }
    var email = document.getElementById("id_email");
    if ($.isEmptyObject(email.value)) {
        $("#id_email").next().text("邮箱不能为空")
    } else if (!(/^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/.test(email.value))) {
        $("#id_email").next().text("邮箱格式错误")
    }
    var password = document.getElementById("id_password");
    if ($.isEmptyObject(password.value)) {
        $("#id_password").next().text("密码不能为空")
    }
    var confirm_password = document.getElementById("id_confirm_password");
    if ($.isEmptyObject(confirm_password.value)) {
        $("#id_confirm_password").next().text("密码不能为空")
    } else if (password.value !== confirm_password.value) {
        $("#id_confirm_password").next().text("两次输入的密码不匹配")
    }
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
            'username': username.value,
            "email": email.value,
            "password": password.value,
            "confirm_password": confirm_password.value,
            "phone_number": phone_number.value,
            "code": code.value
        }
    }).done(function (msg) {
        $("#id_" + msg.key).next().text(msg.errmsg)
    }).fail(function () {
        alert('服务器访问失败，请稍后再试！')
    })
    console.log(username.value, email.value, password.value, confirm_password.value, phone_number.value, code.value);
}