
/**
 * 获取用户注册验证码，30s 倒计时
 */
function getRegisterCaptcha(){
    // 倒计时剩下的秒数
    const COUNTDOWN = 30;
    var restTime = COUNTDOWN;
    var btn = $("#getCaptcha");
    var name = $("#username").val();
    var email = $("#email").val();
    if(restTime == COUNTDOWN){
        var timer = setInterval(function(){
            if(restTime == 0){
                $("#getCaptcha").html("获取验证码");
                btn.removeAttr("disabled");
                restTime = COUNTDOWN;
                clearInterval(timer);
            }else{
                btn.attr("disabled","true");
                btn.html("重新发送("+restTime+")");
                restTime--;
            }
        }, 1000);
        httpPostByJson(serverData.getCaptchaUrl,
            {captcha_type:1, name:name, email:email},
            function(data){
                if(data.code == 0){
                    // 验证码发送成功
                    toastr.success(data.msg)
                }else{
                    // 发送验证码失败，则直接停止倒计时
                    restTime = 0;
                    toastr.error(data.msg)
                }
            },
            function(error){
                // 发送验证码失败，则直接停止倒计时
                restTime = 0;
                toastr.error("发送验证码失败")
            }
        );
    }
}


/**
 * 获取忘记密码验证码，30s 倒计时
 */
function getForgetPwdCaptcha(){
    // 倒计时剩下的秒数
    const COUNTDOWN = 30;
    var restTime = COUNTDOWN;
    var btn = $("#getCaptcha");
    var email = $("#email").val();
    if(restTime == COUNTDOWN){
        var timer = setInterval(function(){
            if(restTime == 0){
                $("#getCaptcha").html("获取验证码");
                btn.removeAttr("disabled");
                restTime = COUNTDOWN;
                clearInterval(timer);
            }else{
                btn.attr("disabled","true");
                btn.html("重新发送("+restTime+")");
                restTime--;
            }
        }, 1000);
        httpPostByJson(serverData.getCaptchaUrl,
            {captcha_type:2, email:email},
            function(data){
                if(data.code == 0){
                    // 验证码发送成功
                    toastr.success(data.msg)
                }else{
                    // 发送验证码失败，则直接停止倒计时
                    restTime = 0;
                    toastr.error(data.msg)
                }
            },
            function(error){
                // 发送验证码失败，则直接停止倒计时
                restTime = 0;
                toastr.error("发送验证码失败")
            }
        );
    }
}

