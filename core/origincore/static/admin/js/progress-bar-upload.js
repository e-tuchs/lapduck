$(function () {

  $(".js-upload-photos").click(function () {
    $(this).next(".fileupload").click();
  });

  $(".fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        if (data.result.type=='img') {
          val_storate = $(this).parent().find('.valstorage');
          val_storate.val('/static/images/'+data.result.name);
          $(this).after('<img src="/static/images/'+data.result.name+'" height="60" width="60""/>');
        }
        else if(data.result.type=='apk'){
           var appdatailinfo = '<div>'
           $.each(data.result.content, function (key, value) {
               appdatailinfo += '<input type="text" id="id_'+key
               +' for="id_'+key+'" name="'+key+'"'
               +'" value="'+value+'" style="display: none;">';
           })
           appdatailinfo += '<div>'
            +'<p><td>包名    ：'+data.result.content.app_akp_name+'</td></p>'
            +'<p><td>版本号  ：'+data.result.content.app_version_name+'</td></p>'
            +'<p><td>版本编号 :'+data.result.content.app_version_code+'</td></p>'
            +'<p><td>MD5值   :'+data.result.content.app_apk_hash+'</td></p>'
            +'<p><td>权限列表 ：'+data.result.content.app_other_permission+'</td></p>'
            +'</div>';
          $(this).after(appdatailinfo);
        }
      }
    }
  });
});
