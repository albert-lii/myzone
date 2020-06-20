
$(function(){
    if(serverData.isLogin == "True"){
        if(serverData.likeData.status==0){
            $("#like-icon").attr("src", serverData.likeUnSelImg)
        }else{
            $("#like-icon").attr("src", serverData.likeSelImg)
        }
    }
});

/**
 * 喜欢操作
 **/
function likeClick() {
    var action = 0;
    if(serverData.likeData.status == 0){
        action = 1;
    }else{
        action = 0;
    }
    httpPostByJson(serverData.doLikeUrl,
        {article_id:serverData.articleId, action:action},
            function(data){
                if(data.code == 0){
                    if($("#like-icon").attr("src").indexOf(serverData.likeUnSelImg)!=-1 ){
                        $("#like-icon").attr("src", serverData.likeSelImg)
                    }else{
                        $("#like-icon").attr("src", serverData.likeUnSelImg)
                    }
                }else{
                    toastr.error(data.msg)
                }
            },
            function(error){
                toastr.error("喜欢操作失败")
            }
        );
}