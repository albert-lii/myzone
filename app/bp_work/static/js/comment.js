
/**
 * 添加评论
 */
function addComment() {
    if(serverData.isLogin == "True") {
        httpPostByJson(serverData.addCommentUrl,
            {article_id: serverData.articleId, content: $('#comment-input').val()},
            function(data){
                if(data.code == 0){
                   $("#comment-input").val("");
                   window.location.reload();
                }
            },
            function(error){
                console.log(error)
            }
        );
    }else{
        // 没有登录，则直接前往登录页面
        // window.location.href = window.location.protocol + "//" + window.location.host + serverData.loginUrl;
        window.location.href = serverData.loginUrl;
    }
}

/**
 * 取消评论
 */
function cancelComment() {
    $("#comment-input").val("");
}

/**
 * 显示评论回复框
 *
 * commentLv: 评论等级
 * parentId: 父级评论 id
 * repliedId: 被回复的评论 id
 */
function showReplyCommentBox(commentLv, parentId, repliedId) {
    if(serverData.isLogin == "True") {
        $(".comment-replay-box").html("");
        var dom = $("#"+repliedId).find(".comment-body").find(".comment-replay-box").first();
        if(commentLv == 2){
            dom = $("#"+repliedId).find(".comment-replay-box")
        }
        dom.html(
            '<div class="form-group comment-box">'+
                '<textarea id="reply-comment-input" class="form-control" rows="4" placeholder="写点什么吧..."></textarea>'+
                 '<div class="row comment-box-btn">'+
                    '<button id="cancel" type="button" class="btn cancel-btn" onclick="cancelReply()">取消</button>'+
                    '<button id="submit" type="button" class="btn btn-primary publish-btn" onclick="replyComment(2, '+parentId+', '+repliedId+')">发布</button>'+
                 '</div>'+
            '</div>'
        );
    }else{
        // 没有登录，则直接前往登录页面
//        window.location.href =window.location.protocol + "//" + window.location.host + serverData.loginUrl;
        window.location.href = serverData.loginUrl;
    }
}

/**
 * 回复评论
 *
 * commentLv: 评论等级
 * parent_id: 父级评论 id
 * replied_id: 被回复的评论 id
 */
function replyComment(commentLv, parentId, repliedId) {
    var content = $("#"+repliedId).find(".comment-body").find(".comment-replay-box").find('#reply-comment-input').val();
    if(commentLv == 2){
        content = $("#"+repliedId).find(".comment-replay-box").find('#reply-comment-input').val();
    }
    httpPostByJson(serverData.replyCommentUrl,
        {parent_id: parentId, replied_id: repliedId, content: content},
        function(data){
            if(data.code == 0){
                $(".comment-replay-box").html("");
                window.location.reload();
            }
        },
        function(error){
            console.log(error);
        }
    );
}

/**
 * 取消评论回复
 */
function cancelReply() {
    $(".comment-replay-box").html("");
}





