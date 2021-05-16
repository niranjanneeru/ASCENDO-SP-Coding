from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.views import View

from ascendo_web_page.user_profile.models import Profile
from .brainfuck import evaluate
from .forms import AnswerForm, ResponseForm
from .models import Question, Challenge


class QuestionView(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                return redirect('user_profile:redirect')

            if profile.has_completed:
                message = "Completed"
                return render(request, 'game/end.html', {"flag": 1, "message": message})

            q = Question.objects.all()[0]

            if not q.is_active:
                context = {'code': -1}
                return render(request, 'game/result.html', context)

            if not profile.language:
                context = {'question': q, 'form': AnswerForm()}
                return render(request, 'game/question.html', context)

            if not profile.code:
                return redirect('game:code')


        else:
            return redirect('home')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                return redirect('user_profile:redirect')

            if not profile.language:
                context = {'message': "Invalid Answer", 'code': 0}
                form = AnswerForm(request.POST)
                if form.is_valid():
                    answer = form.data.get('answer')
                    question = Question.objects.all()[0]
                    if answer:
                        answer = answer.replace(' ', '')
                        if answer.lower() == question.answer:
                            profile.language = True
                            profile.last_submission = now()
                            profile.save()
                            context['message'] = "Congo, You Found the Language"
                            context['code'] = 1
                            return render(request, 'game/result.html', context)
                return render(request, 'game/result.html', context)

        else:
            return redirect('home')


question_view = QuestionView.as_view()


class CodeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                return redirect('user_profile:redirect')

            if profile.has_completed:
                message = "Completed"
                return render(request, 'game/end.html', {"flag": 1, "message": message})

            q = Challenge.objects.all()[0]

            if not q.is_active:
                context = {'code': -1}
                return render(request, 'game/result.html', context)

            if not profile.language:
                return redirect('game:question')

            if not profile.code:
                context = {'code': q, 'form': ResponseForm()}
                return render(request, 'game/code.html', context)

        else:
            return redirect('home')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                return redirect('user_profile:redirect')

        if not profile.code:
            form = ResponseForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                answer = form.answer
                answer = "\n".join([a.strip() for a in answer.split("\n") if not a.strip().startswith("//")])
                print(answer)
                out, code = evaluate(answer)
                context = {'code': 0}
                if code == -1:
                    context['message'] = "Your Code Has an Input Statement"
                    form.answer = context['message']
                elif code == 1:
                    context['message'] = "Compilation Error"
                    form.answer = context['message']
                elif code == 0:
                    c = Challenge.objects.all()[0]
                    if c.answer.strip() == out.strip():
                        context['message'] = "Completed"
                        context['code'] = 1
                        profile.code = True
                        profile.has_completed = True
                        profile.last_submission = now()
                        profile.save()
                        form.answer = out
                        form.status = 1
                    else:
                        context['message'] = "Wrong Output"
                form.user = request.user.profile
                form.create_date = now()
                form.save()
                return render(request, 'game/result.html', context)


code_view = CodeView.as_view()
