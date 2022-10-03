from django.views import View
from django.shortcuts import render
from app_goals.models import Goal, UserImpact


class MainView(View):
    def get(self, request):
        user = request.user
        if request.user.is_authenticated:
            goals = Goal.objects.filter(participants__in=[user])
            goals_dict = {}
            for goal in goals:
                impacts = UserImpact.objects.filter(goal=goal)
                sum_impacts = sum(user.impact for user in impacts)
                complete_percent = round(sum_impacts * 100 / goal.value, 2)
                goals_dict[goal] = complete_percent

            context = {
                'have_goals': len(goals_dict.keys()),
                'goals': goals_dict,
                'goals_count': goals.count()
            }
        else:
            context = {}
        return render(request, 'main.html', context=context)
