
from django import forms
from .models import AttendanceInfo
from facedata.models import FaceData
from django.forms import widgets
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput
User = get_user_model()



class ImageWidget(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s"><img width="100px" height="100px" src="%(initial_url)s"></a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )

    template_with_clear = ''

class AttendanceInfoForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super(AttendanceInfoForm, self).__init__(*args, **kwargs)
        role = user.roles.first().name  # 能登录的人都有角色
        if role == '系统管理员':
            self.fields['facedata'].queryset = FaceData.objects.all()
        elif role == '公司级管理员':
            self.fields['facedata'].queryset = FaceData.objects.filter(department__tree_id=user.department.tree_id)

    class Meta:
        model = AttendanceInfo
        fields = '__all__'
        widgets = {
            'facedata': widgets.Select(
                attrs={"class": " select2", "name": "owner", "id": "facedata__id", 'style': 'width:50%;'}),

        }


class AttendanceInfoCreateForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super(AttendanceInfoCreateForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            # department = user.department
            # post = user.post
            # if post == '部门安全管理员':
            #     self.fields['owner'].queryset = User.objects.filter(department=department)
            # else:
            #     self.fields['owner'].queryset = User.objects.filter(pk=user.id)
            pass

    class Meta:
        model = AttendanceInfo
        fields = '__all__'
        widgets = {
            'facedata': widgets.Select(attrs={"class": " select2", "name": "owner", 'style': 'width:100%;'}),
            'recorded_datetime':widgets.Input(attrs={"class": "form-control pull-right form_datetime ",'readonly': 'readonly'}, ),
            # 'image': widgets.ClearableFileInput(attrs={'class': "form-control", 'rows': "3"}),

        }
        error_messages = {
            "owner": {"required": "请选择对应人员"},

        }

class AttendanceInfoUpdateForm(forms.ModelForm):
    def __init__(self, *args, user, **kwargs):
        super(AttendanceInfoUpdateForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            # department = user.department
            # post = user.post
            # if post == '部门安全管理员':
            #     self.fields['owner'].queryset = User.objects.filter(department=department)
            # else:
            #     self.fields['owner'].queryset = User.objects.filter(pk=user.id)
            pass


    class Meta:
        model = AttendanceInfo
        fields = '__all__'
        widgets = {
            'facedata': widgets.Select(attrs={"class": " select2", "name": "owner", 'style': 'width:100%;'}),
            'recorded_datetime': widgets.Input(
                attrs={"class": "form-control pull-right form_datetime ", 'readonly': 'readonly'}, ),
            # 'image': widgets.ClearableFileInput(attrs={'class': "form-control", 'rows': "3"}),

        }
        error_messages = {
            "owner": {"required": "请选择对应人员"},

        }