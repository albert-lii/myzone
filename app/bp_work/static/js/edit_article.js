
// 添加/修改文章封面图片按钮的点击事件
function articleCoverClick() {
    $("#cover").click();
}

// 选择文章封面图片并预览
function selectArticleCover(event){
    var files = event.target.files, file;
    if (files && files.length > 0) {
        // 获取目前上传的文件
        file = files[0];// 文件大小校验的动作
        if(file.size > 1024 * 1024 * 2) {
            alert('图片大小不能超过 2MB!');
            return false;
        }
        // 获取 window 的 URL 工具
        var URL = window.URL || window.webkitURL;
        // 通过 file 生成指向的目标 url
        var imgURL = URL.createObjectURL(file);
        // 用 attr 将 img 的 src 属性改成获得的 url
        $("#article-cover").attr("src", imgURL);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
}

// 删除文章封面图片按钮的点击事件
function deleteArticleCoverClick() {
   $("#article-cover").attr("src", serverData.selectDefaultPic); // 清除预览图片
   $("#select-article-cover").attr("value", ""); // 清除 file
}
