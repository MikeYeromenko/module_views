import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required

# Create your views here.
from modshop import models
from modshop.forms import MyUserCreationForm, BuyingForm, GoodsUpdateForm
from modshop.models import MyUser


class RegisterUser(CreateView):
    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'registration.html'

    def get_success_url(self):
        return reverse_lazy('shopping')


def start_page(request):
    return render(request, 'shopping.html')


class LoginUser(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('shopping')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


class GoodsListView(ListView):
    model = models.Goods
    queryset = models.Goods.objects.all().values('id', 'title', 'quantity', 'price').order_by('title')
    template_name = 'shopping.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dict_permissions = system_permissions(self.request.user.groups.all())
        context.update(dict_permissions)
        return context


# first decided to differ permissions using groups
def system_permissions(groups):
    result = {}
    for group in groups:
        if str(group).lower() == 'users':
            result.update({'buying_form': BuyingForm})
    return result


class PurchaseCreateView(LoginRequiredMixin, View):

    def post(self, *args, **kwargs):
        user = get_object_or_404(models.MyUser, pk=self.request.user.id)
        # getting id of goods
        pk = kwargs.get('pk')
        # getting entered by user quantity of goods
        form = BuyingForm(self.request.POST)
        user_quantity = int(form.data['quantity'])
        # getting goods object
        goods_object = get_object_or_404(models.Goods, pk=pk)

        users_money = user.wallet

        if check_conditions_for_buying(self.request, user_quantity, users_money, goods_object.price,
                                       goods_object.quantity):
            total_price = user_quantity * goods_object.price
            # query = Q()
            purchase = models.Purchase(id_user=user, id_goods=goods_object,
                                       quantity=user_quantity, total_price=total_price)
            purchase.save()
            goods_object.quantity -= user_quantity
            goods_object.save()

            user.wallet -= total_price
            user.save()

        return HttpResponseRedirect(reverse_lazy('shopping'))


def check_conditions_for_buying(request, user_quantity, users_money, price, goods_quantity):
    total_sum = user_quantity * price
    result = True
    if total_sum > users_money:
        messages.warning(request, f"You haven't got enough money for this buying. You have {users_money} hrn. "
                                  f"But you need {total_sum} hrn")
        result = False
    if goods_quantity < user_quantity:
        messages.warning(request, f"We haven't got enough goods. We have {goods_quantity} pc. "
                                  f"But you want {user_quantity} pc.")
        result = False
    return result


class PurchesListView(LoginRequiredMixin, ListView):
    model = models.Purchase
    paginate_by = 20
    template_name = 'purchase.html'

    def get_queryset(self):
        user = self.request.user
        query = Q(id_user=user.id)
        return models.Purchase.objects.filter(query).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        column_names = ['Goods', 'quantity', 'total price', 'date of purchase', 'was returned',
                        'return accepted']
        context = super().get_context_data(**kwargs)
        context.update({
            'column_names': column_names
        })
        return context


class GoodsReturnView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        # user = self.request.user
        pk = kwargs['pk']
        purchase = get_object_or_404(models.Purchase, pk=pk)
        time_now = datetime.datetime.now(datetime.timezone.utc)
        time_ok = time_now - datetime.timedelta(minutes=3)
        if purchase.date_time > time_ok:

            if not purchase.was_returned:

                goods_return = models.Goods_Return(id_purchase=purchase)
                goods_return.save()
                purchase.was_returned = True

            else:

                purchase.was_returned = False
                goods_return = get_object_or_404(models.Purchase, pk=pk)
                goods_return.delete()

            purchase.save()
        else:

            if purchase.was_returned:

                purchase.was_returned = False
                goods_return = get_object_or_404(models.Purchase, pk=pk)
                goods_return.delete()
                purchase.save()

            messages.info(self.request, f"Dear customer! According to our rules purchase can be "
                                        f"cancelled in 3 minutes after it was done. You made a purchase at "
                                        f"{purchase.date_time.strftime('%Y-%m-%d %H:%M:%S')}, but now it's "
                                        f"{time_now.strftime('%H:%M:%S')}. So unfortunatelly "
                                        f"3 minutes had passed and its impossible to make return.")

        return HttpResponseRedirect(reverse_lazy('purchases'))


class GoodsUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Goods
    form_class = GoodsUpdateForm
    template_name = 'update_goods.html'
    # fields = ['title', 'price', 'quantity', 'description']
    # success_url = 'goods_update/'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('goods_update', kwargs={'pk': pk})

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return super().form_valid(form)


class GoodsCreateView(CreateView):
    model = models.Goods
    form_class = GoodsUpdateForm
    template_name = 'update_goods.html'

    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('goods_add')


class GoodsReturnAdminView(ListView):
    model = models.Goods_Return
    template_name = 'goods_return.html'

    def get_queryset(self):
        goods_return = models.Goods_Return.objects.prefetch_related('id_purchase').all()
        return goods_return


class WorkWithReturnView(LoginRequiredMixin, View):

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        goods_return = get_object_or_404(models.Goods_Return, pk=pk)
        id_purchase = goods_return.id_purchase_id
        purchase = get_object_or_404(models.Purchase, pk=id_purchase)
        id_goods = purchase.id_goods_id
        goods = get_object_or_404(models.Goods, pk=id_goods)
        id_user_bought = purchase.id_user_id
        user_bought = get_object_or_404(models.MyUser, pk=id_user_bought)
        if 'accept' in self.request.POST:
            # returning quantity of goods bought to goods object
            goods.quantity += purchase.quantity
            goods.save()
            # returning sum of money user paid
            user_bought.wallet += purchase.total_price
            user_bought.save()
            # deleting a purchase
            purchase.delete()
        if 'refuse' in self.request.POST:
            # when creating a Goods_Return we changed the status of was retuned to True
            # now let's change it back to False
            purchase.was_returned = False
            purchase.save()
            # deleting a goods_return object, because admin refused
            goods_return.delete()
        return HttpResponseRedirect(reverse_lazy('goods_return'))
