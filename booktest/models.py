from re import T
from django.db import models


# Create your models here.
class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, db_column='title')
    bpub_date = models.DateField()
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)  # 软删除标记

    class Meta:
        db_table = 'bookinfo'


class AreaInfo(models.Model):
    atitle = models.CharField(verbose_name='local', max_length=20)
    aParent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self) -> str:
        return self.atitle 

    def title(self):
        return self.atitle
    
    title.admin_order_field = 'atitle'
    title.short_description = '地区'

    def parent(self):
        if self.aParent is None:
            return ''
        return self.aParent.atitle
    parent.short_description = 'father'


class PicTest(models.Model):
    goods_pic = models.ImageField(upload_to='booktest')


