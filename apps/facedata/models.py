from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
import imghdr

class FaceData(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='姓名')
    face_id = models.CharField(max_length=30, blank=True,null=True,unique=True, verbose_name="人脸样本ID")  # unique=True, 这个字段在表中必须有唯一值.
    face_name = models.CharField(max_length=30, verbose_name="人脸拼音名称")
    face_cname = models.CharField(max_length=30, verbose_name="人脸中文名称")
    face_image = models.ImageField( upload_to="facedata/%Y/%m", null=True, blank=True,verbose_name="人脸图片")
    ifsync = models.BooleanField(verbose_name='是否同步数据',default=False)
    def __str__(self):
        return self.face_cname

    class Meta:
        verbose_name = '人脸样本信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

