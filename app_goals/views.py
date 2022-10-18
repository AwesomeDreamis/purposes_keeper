from datetime import date
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import GoalForm, GoalUpdateForm
from .models import Goal, UserImpact, Operation


class GoalCreateView(View):
    """Представление создания цели"""

    def get(self, request):
        form = GoalForm
        context = {'form': form}
        return render(request, 'goals/create_goal.html', context=context)

    def post(self, request):
        form = GoalForm(request.POST)
        user = request.user
        participants = request.POST.getlist('participants')
        if form.is_valid():
            goal_instance = form.save(commit=False)
            goal_instance.author = user
            goal_instance.save()

            for participant_id in participants:
                participant = User.objects.get(id=int(participant_id))
                goal_instance.participants.add(participant)
                UserImpact.objects.create(goal=goal_instance, user=participant, impact=0)

            goal_instance.participants.add(user)
            UserImpact.objects.create(goal=goal_instance, user=user, impact=0)
            goal_instance.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'goals/create_goal.html', {'form': form})


class GoalDetailView(DetailView):
    """Детальное представление цели"""

    model = Goal
    context_object_name = 'goal'
    template_name = 'goals/goal_detail.html'

    def get_context_data(self, **kwargs):
        context = super(GoalDetailView, self).get_context_data(**kwargs)
        goal = self.get_object()
        impacts = UserImpact.objects.filter(goal=goal)
        sum_impacts: int = sum(user.impact for user in impacts)
        complete: int = int(sum_impacts * 100 / goal.value)
        timeleft: int = (goal.deadline - date.today()).days
        context['timeleft'] = timeleft
        context['impacts'] = impacts
        context['sum_impacts'] = sum_impacts
        context['complete']: int = range(complete)
        context['left']: int = range(100 - complete)
        context['complete_percent']: int = round(sum_impacts * 100 / goal.value, 2)
        context['history'] = Operation.objects.filter(goal=goal).order_by('-created_at')[:30]

        return context

    def post(self, request, pk):
        goal = Goal.objects.get(id=pk)
        impact = request.POST.get('impact')

        Operation.objects.create(
            goal=goal,
            user=request.user,
            impact=impact
        )

        user_impact = UserImpact.objects.get(user=request.user, goal=goal)
        user_impact.impact += int(impact)
        user_impact.save()

        return redirect('goal_detail', pk)


class GoalsListView(ListView):
    """Представление списка целей пользователя"""

    model = Goal
    template_name = 'goals/goals_list.html'
    context_object_name = 'goals'

    def get_context_data(self, **kwargs):
        context = super(GoalsListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self) -> QuerySet:
        user = self.request.user

        if self.request.GET.get('search'):
            query = self.request.GET.get('search')
            queryset = Goal.objects.filter(participants__in=[user], title__icontains=query)
        else:
            queryset = Goal.objects.filter(participants__in=[user])

        return queryset


class GoalUpdateView(View):
    """Представление изменения цели"""

    def get(self, request, pk):
        goal = Goal.objects.get(id=pk)
        default_data = {
            'title': goal.title,
            'value': goal.value,
            'deadline': goal.deadline,
        }
        context = {
            'form': GoalUpdateForm(default_data),
            'goal': goal
        }
        return render(request, 'goals/goal_update.html', context=context)

    def post(self, request, pk):
        goal = Goal.objects.get(id=pk)
        goal.title = request.POST.get('title')
        goal.value = request.POST.get('value')
        goal.deadline = request.POST.get('deadline')
        goal.save()

        return redirect('goal_detail', pk)


class LeaveFromGoal(View):
    """Представление выхода из цели"""
    def get(self, request, pk):
        user = request.user
        goal = Goal.objects.get(id=pk)

        UserImpact.objects.get(goal=goal, user=user).delete()
        operations = Operation.objects.filter(goal=goal, user=user)
        for operation in operations:
            operation.delete()

        if goal.participants.count() == 1:
            goal.delete()
        else:
            goal.participants.remove(user)
            goal.save()

        return HttpResponseRedirect('/')
