from rest_framework.serializers import ModelSerializer

from expense.models import Expense, Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name', 'type', 'icon'


class ExpenseModelSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'price', 'category', 'description', 'user']
        extra_kwargs = {
            'user': {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryModelSerializer(
            instance=Category.objects.filter(id=data.get('category')).first()).data
        return data


class DeleteExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = 'id', 'price', 'description'


class UpdateExpenseSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = 'id', 'price', 'description'


class ExpenseListModelSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = 'id', 'price', 'description', 'category'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryModelSerializer(
            instance=Category.objects.filter(id=data.get('category')).first()).data
        return data


class AdminCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name', 'icon','type'

