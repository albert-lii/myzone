/**
 * post 方式请求接口
 *
 * url: 请求接口
 * data: 提交的 json 参数
 */
function httpPostByJson(url, params, successFunc, errorFunc) {
    $.ajax({
        url: url,
  　　  type: "post",
  　　  dataType: "json",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(params),
  　　  success: function(data){
            successFunc(data);
        },
        error: function(xhr, status, error){
            errorFunc(error);
       },
   });
}