from category.models import Category
from expense.models import Expense
from expense.serializers import ExpenseSerializer
from income.models import Income
from income.serializers import IncomeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import INCOME, EXPENSE, current_month
from core.helpers import get_trunc_week


# Получить все расходы за диапазон дат (from_date и to_date в интерфейсе)
class QueryDateRangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        select = request.GET.get("select")
        try:
            if select == EXPENSE:
                filtered_expense = (
                    Expense.objects.filter(user=request.user)
                    .filter(date__range=(from_date, to_date))
                    .order_by("-id")
                )
                serializer = ExpenseSerializer(filtered_expense, many=True)
                expense_sum = Expense.get_expense_total(
                    from_date, to_date, request.user
                )
                json_data = {"filtered": serializer.data, "total": expense_sum}
                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)

            if select == INCOME:
                filtered_income = (
                    Income.objects.filter(user=request.user)
                    .filter(date__range=(from_date, to_date))
                    .order_by("-id")
                )
                serializer = IncomeSerializer(filtered_income, many=True)
                income_sum = Income.get_income_total(from_date, to_date, request.user)
                json_data = {"filtered": serializer.data, "total": income_sum}

                if json_data:
                    return Response(json_data, status=status.HTTP_200_OK)

        except:
            return Response(
                data={"message": "Результаты не найдены, неверные параметры"},
                status=status.HTTP_404_NOT_FOUND,
            )


# последние 7 дней
class QueryDayGraph(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(
                {"filtered": Expense.get_expenses_daily_for_the_week(request.user)},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                data={"message": "Невозможно получить ежемесячные расходы за неделю"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Запрос каждую неделю месяца
class QueryWeekGraph(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(
                {"filtered": get_trunc_week(user=request.user)},
                status=status.HTTP_200_OK,
            )

        except:
            return Response(
                data={"message": "Невозможно получить ежемесячные расходы за месяц"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Месячные расходы
class QueryMonthGraph(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = Expense.get_expenses_monthly_for_the_year(request.user)
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Невозможно получить ежемесячные расходы за год"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class QueryMostRecentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            filtered = (
                Expense.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .order_by("-id")[:5]
            )
            serializer = ExpenseSerializer(filtered, many=True)
            return Response({"filtered": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Не удалось получить последние расходы"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class QueryNetView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            category_count = (
                Category.objects.filter(user=request.user)
                .filter(date__month=str(current_month))
                .all()
                .count()
            )

            data = Expense.get_net_expenses_for_the_month(request.user)
            data[0]["categoryCount"] = category_count

            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Невозможно получить чистые расходы"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class QueryCategoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            categories = Category.objects.filter(user=request.user).filter(
                date__month=str(current_month)
            )
            data = []
            for i in categories:
                data.append({"category": i.name, "amount": i.total_expense_cost})
            return Response({"filtered": data}, status=status.HTTP_200_OK)
        except:
            return Response(
                data={"message": "Невозможно сгруппировать по категориям"},
                status=status.HTTP_400_BAD_REQUEST,
            )
