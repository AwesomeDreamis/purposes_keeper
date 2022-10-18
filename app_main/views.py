from django.db.models import QuerySet
from django.views import View
from django.shortcuts import render
from app_goals.models import Goal, UserImpact


class MainView(View):
    def get(self, request):
        user = request.user
        if request.user.is_authenticated:
            goals: QuerySet = Goal.objects.filter(participants__in=[user])
            goals_dict = {}
            for goal in goals:
                impacts: QuerySet = UserImpact.objects.filter(goal=goal)
                sum_impacts: int = sum(user.impact for user in impacts)
                complete_percent: int = round(sum_impacts * 100 / goal.value, 2)
                goals_dict[goal]: int = complete_percent

            context = {
                'have_goals': len(goals_dict.keys()),
                'goals': goals_dict,
                'goals_count': goals.count()
            }
        else:
            context = {}
        return render(request, 'main.html', context=context)
