#! -*- coding:utf-8 -*-
from django import forms
from django.forms import fields, widgets
from django.utils.safestring import mark_safe
from django.utils.text import force_unicode

class UploadWidget(widgets.TextInput):

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'vTextField'
        input = super(UploadWidget, self).render(name, value, attrs=attrs)
        value = ('<a href="%s" target="_blank">view</a>' % value.url) if value and getattr(value, 'url') else value
        onchange = r'''
            f = this.files[0];
            this.value = '';
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/simple_upload/' + f.name, true);
            xhr.setRequestHeader('X-CSRFToken', this.form.csrfmiddlewaretoken.value);
            xhr.upload.status = this.parentNode.firstChild.nextElementSibling; // <span>
            xhr.upload.status.innerHTML = 'pending...';
            xhr.upload.onprogress = function(e){
                this.status.innerHTML = Math.round(100 * e.loaded / e.total) + '% uploaded'
            };
            xhr.send(f);
            xhr.onload = function(){
              this.upload.status.innerHTML = '<a href=\'/media/' + encodeURI(this.responseText) + '\' target=_blank>view</a>';
              this.upload.status.previousElementSibling.value = this.responseText; // <input type=hidden>
            };'''
        # assert '"' not in onchange
        return mark_safe('<p>%s<span>%s</span><br><input type="file" onchange="%s" value="upload"></p>' % (input, value, onchange))


class AjaxUploadWidget(forms.FileInput):
    """
        must be used with jquery.fileupload.js
    """
    file_type_dict = {
        'apk': '.apk',
        'img': '.jpg,.png,.jpeg',
    }

    def __init__(self, *args, **kwargs):
        super(AjaxUploadWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        output = []
        f_type = 'apk' if 'download_path' in attrs['id'] else 'img'
        output.append((r"""
                <div style="margin-bottom: 20px;" class="">
                    <button type="button" class="btn btn-primary js-upload-photos">
                    <span class="glyphicon glyphicon-cloud-upload"></span>点击上传</button>
                    <input id="fileupload" type="file" name="%s" class="fileupload"
                        style="display: none;"
                    data-url="/admin/progress-bar-upload/" accept="%s">
                    <div class="imgbox" style="float:right;margin-left: 10px"></div>
                    <input name="%s" class="valstorage" type="text" style="display: none;">
                </div>
                <div class="modal fade" id="modal-progress" data-backdrop="static" data-keyboard="false">
                    <div class="modal-dialog">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h4 class="modal-title">上传中...</h4>
                        </div>
                        <div class="modal-body">
                          <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: 0;">0</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
            """ % (force_unicode(name),
                   force_unicode(self.file_type_dict[f_type]),
                   force_unicode('id_'+name))))
        return mark_safe(u''.join(output))
    
    class Media:
        js = (
            '/static/admin/js/jquery-3.1.1.min.js',
            '/static/admin/js/jquery-file-upload/vendor/jquery.ui.widget.js',
            '/static/admin/js/jquery-file-upload/jquery.fileupload.js',
            '/static/admin/js/jquery-file-upload/jquery.iframe-transport.js',
            '/static/admin/js/progress-bar-upload.js',
            '/static/admin/js/bootstrap.min.js',
        )       # 必须按该顺序加载js， 否则控件不能正常工作
        css = {
            # declarations:all,aural,braille,embossed,handheld,print,projection,screen,tty,tv
            'all': (
                'admin/css/bootstrap.min.css',
                'admin/css/changelists.css',
            )
        }


