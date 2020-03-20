from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from modshop.models import MyUser
from modshop import models


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', ]

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        group = Group.objects.get(name='Users')
        if commit:
            user.save()
            user.groups.add(group)
        return user

    # def save(self, commit=True):
    #     # code here
    #     return super(MyForm, self).save(commit)


class BuyingForm(forms.Form):
    quantity = forms.IntegerField(min_value=0, initial=1)


class GoodsUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Goods
        fields = '__all__'


# class PurchaseCreationForm:
#     class Meta:
#         model = Purchase
#         fields = ['id_user', 'id_goods', 'quantity', 'total_price']
#
#     def save(self, commit=True):
#         purchase = super(PurchaseCreationForm, self).save(commit=False)
#         purchase.quantity = self.cleaned_data['quantity']
#         purchase.total_price = self.cleaned_data['total_price']
#         purchase.id_user = self.cleaned_data['id_user']
#         purchase.id_goods = self.cleaned_data['id_goods']
#         if commit:
#             purchase.save()
#         return purchase


# GROUPS = Group.objects.get()
#
# ORDER = (
#     ('text', 'By text'),
#     ('created_at', 'By date')
# )
#
#
# class GroupsAdminChange(forms.Form):
#     change_group = forms.ChoiceField(choices=ORDER)
#     Submit = forms.S
#
#
# def make_group_choices():
#     groups_query = Group.objects.get()
#     my_tuple = ()
#     i = 0
#     for group in groups_query:
#         my_tuple += (group, i)
#         i += 1
#
#     return my_tuple
