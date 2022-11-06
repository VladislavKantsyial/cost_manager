from django.urls import path

from .views import QueryDateRangeView, QueryCategoryView, QueryDayGraph, QueryWeekGraph, QueryMonthGraph, \
    QueryMostRecentView, QueryNetView

urlpatterns = [
    path("query-date-range/", QueryDateRangeView.as_view(), name="query_date_range"),
    path("query-category/", QueryCategoryView.as_view(), name="query_category"),
    path("query-day-graph/", QueryDayGraph.as_view(), name="query_day_graph"),
    path("query-week-graph/", QueryWeekGraph.as_view(), name="query_week_graph"),
    path("query-month-graph/", QueryMonthGraph.as_view(), name="query_month_graph"),
    path(
        "query-most-recent-expenses/",
        QueryMostRecentView.as_view(),
        name="query_most_recent_expenses",
    ),
    path("query-net/", QueryNetView.as_view(), name="query_net"),
]
