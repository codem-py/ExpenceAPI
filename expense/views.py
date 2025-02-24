from django.db.models.aggregates import Sum
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from expense.models import Expense, Category
from expense.serializers import ExpenseModelSerializer, DeleteExpenseSerializer, ExpenseListModelSerializer, \
    AdminCategorySerializer, CategoryModelSerializer


# Create your views here.

@extend_schema(tags=["expense"], request=ExpenseModelSerializer, responses=ExpenseModelSerializer)
class ExpenseListCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseModelSerializer


@extend_schema(tags=["expense"], responses=DeleteExpenseSerializer)
class ExpenseDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
        except Expense.DoesNotExist:
            return Response({"detail": "Not found!"}, status=HTTP_404_NOT_FOUND)

        response_data = DeleteExpenseSerializer(expense).data
        expense.delete()
        return Response(response_data, status=HTTP_200_OK)


@extend_schema(tags=["expense"])
class ExpenseUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseModelSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


@extend_schema(tags=["expense"])
class ExpenseAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=["expense"])
class ExpenseListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseListModelSerializer



@extend_schema(tags=["expense"])
class BalanceApiview(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        amounts = Expense.objects.filter(user=self.request.user)
        total = sum(amounts.values_list('price', flat=True))
        income_sum = sum(amounts.filter(type='income').values_list('price', flat=True))
        expenses_sum = sum(amounts.filter(type='payments').values_list('price', flat=True))

        response = {
            'total': total,
            'income': income_sum,
            'payments': expenses_sum,
        }
        return Response(response, status=HTTP_200_OK)



@extend_schema(tags=["category"],responses=CategoryModelSerializer)
class CategoryTypeListApiView(ListAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    lookup_field = 'type'

    def get_queryset(self):
        type = self.kwargs['type']
        return Category.objects.filter(type=type)





# ========================== ADMIN ======================

@extend_schema(tags=["admin"], responses=AdminCategorySerializer, request=AdminCategorySerializer)
class AdminCategoryCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer


@extend_schema(tags=["admin"])
class AdminCategoryUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    lookup_field = 'pk'

@extend_schema(tags=["admin"], responses=AdminCategorySerializer)
class AdminCategoryDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found!"}, status=HTTP_404_NOT_FOUND)

        response_data = AdminCategorySerializer(category).data
        category.delete()
        return Response(response_data, status=HTTP_200_OK)