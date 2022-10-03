from django.urls import path
from .views import GoalCreateView, GoalDetailView, GoalsListView, GoalUpdateView, LeaveFromGoal


urlpatterns = [
    path('create_goal/', GoalCreateView.as_view(), name='create_goal'),
    path('<int:pk>/', GoalDetailView.as_view(), name='goal_detail'),
    path('<int:pk>/goals_list/', GoalsListView.as_view(), name='goals_list'),
    path('goal_edit/<int:pk>/', GoalUpdateView.as_view(), name='goal_update'),
    path('goal_leave/<int:pk>/', LeaveFromGoal.as_view(), name='goal_leave'),
]
