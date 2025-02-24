from django.urls import path

from expense.serializers import CategoryModelSerializer
from expense.views import ExpenseListCreateAPIView, ExpenseDeleteAPIView, ExpenseUpdateAPIView, ExpenseListAPIView, \
    AdminCategoryCreateAPIView, AdminCategoryUpdateAPIView, AdminCategoryDeleteAPIView, ExpenseAPIView, BalanceApiview, \
    CategoryTypeListApiView

urlpatterns = [
    path('expence/', ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('deleteexpense/<int:pk>', ExpenseDeleteAPIView.as_view(), name='expense-delete'),
    path('expenceupdate/<int:pk>', ExpenseUpdateAPIView.as_view()),
    path('expense/<int:pk>', ExpenseAPIView.as_view()),
    path('expense/list', ExpenseListAPIView.as_view()),
    path('balance', BalanceApiview.as_view()),
    path('category/<int:type>', CategoryTypeListApiView.as_view()),
]


urlpatterns += [
    path('category/create', AdminCategoryCreateAPIView.as_view(), name='category-create'),
    path('category/update/<int:pk>', AdminCategoryUpdateAPIView.as_view(), name='category-update'),
    path('category/delete/<int:pk>', AdminCategoryDeleteAPIView.as_view(), name='category-delete'),
]

