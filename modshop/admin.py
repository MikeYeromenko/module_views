from django.contrib import admin


from modshop import models


# Register your models here.
from modshop.models import MyUser


class PurchaseInline(admin.TabularInline):
    model = models.Purchase
    max_num = 5


class GReturnInline(admin.TabularInline):
    model = models.Goods_Return


class AdminScreen(admin.ModelAdmin):
    list_display = ['username', 'groups_list']
    inlines = [
        PurchaseInline,
        GReturnInline,
    ]
    list_per_page = 10

    def groups_list(self, obj):
        groups = obj.groups.all()
        result = []
        for g in groups:
            result.append(g)
        return result


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'quantity', 'updated_at', 'id_last_manager']

    # def id_last_manager(self, obj):
    #

    # def some_info(self, obj):
    #     username = obj.id_last_manager
    #     # return obj.first_name
    #     result = MyUser.objects.get(username=username)
    #     result.first_name = 'sgsdfg'
    #     result.save()
    #     return result.first_name


admin.site.register(models.MyUser, AdminScreen)
admin.site.register(models.Purchase)
admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.Goods_Return)
