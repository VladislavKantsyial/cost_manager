from django.urls import path
from .views import ExpenseListView, ExpenseDetailView, ExportExpenseExcel, ExportExpenseCsv, ExportExpensePdf

urlpatterns = [
    path("expense/", ExpenseListView.as_view(), name="expense_list"),
    path("expense/<int:pk>/", ExpenseDetailView.as_view(), name="expense_detail"),
    path("expense/export-excel/", ExportExpenseExcel.as_view(), name="export_excel"),
    path("expense/export-csv/", ExportExpenseCsv.as_view(), name="export_csv"),
    path("expense/export-pdf/", ExportExpensePdf.as_view(), name="export_pdf"),
]
