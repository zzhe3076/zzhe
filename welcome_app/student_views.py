from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models
from django.urls import reverse
from .models import Student, DormitoryAssignment, Payment, Announcement, FAQ, CheckIn


def student_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('student-login')
        return view_func(request, *args, **kwargs)
    return wrapper


class StudentLoginView(View):
    template_name = 'student/login.html'

    def get(self, request):
        if request.session.get('student_id'):
            return redirect('student-dashboard')
        return render(request, self.template_name)

    def post(self, request):
        student_id = request.POST.get('student_id')
        phone = request.POST.get('phone')

        if not student_id or not phone:
            return render(request, self.template_name, {'error': '请输入学号和手机号'})

        try:
            student = Student.objects.get(student_id=student_id, phone=phone)
            request.session['student_id'] = student.id
            request.session['student_name'] = student.name
            request.session['student_number'] = student.student_id
            return redirect('student-dashboard')
        except Student.DoesNotExist:
            return render(request, self.template_name, {'error': '学号或手机号错误'})
        except Student.MultipleObjectsReturned:
            return render(request, self.template_name, {'error': '系统错误，请联系管理员'})


class StudentLogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('student-login')


class StudentDashboardView(TemplateView):
    template_name = 'student/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('student-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.session.get('student_id')

        if student_id:
            try:
                student = Student.objects.select_related('major__college').get(id=student_id)
                context['student'] = student

                if student.status == 'checked_in':
                    checkin_record = CheckIn.objects.filter(student=student).first()
                    context['checkin_record'] = checkin_record

                try:
                    dormitory = DormitoryAssignment.objects.get(student=student)
                    context['dormitory'] = dormitory
                except DormitoryAssignment.DoesNotExist:
                    context['dormitory'] = None

                payments = Payment.objects.filter(student=student)
                context['payments'] = payments
                context['total_amount'] = sum(p.amount for p in payments)
                context['paid_amount'] = sum(p.amount for p in payments.filter(status='paid'))
                context['pending_amount'] = sum(p.amount for p in payments.filter(status='pending'))

            except Student.DoesNotExist:
                pass

        return context


class StudentDormitoryView(TemplateView):
    template_name = 'student/dormitory.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('student-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.session.get('student_id')

        if student_id:
            try:
                student = Student.objects.select_related('major__college').get(id=student_id)
                context['student'] = student

                assignment = DormitoryAssignment.objects.select_related('room__building').get(student=student)
                context['assignment'] = assignment
            except Student.DoesNotExist:
                context['error'] = '学生信息不存在'
            except DormitoryAssignment.DoesNotExist:
                context['error'] = '暂未分配宿舍'

        return context


class StudentPaymentView(TemplateView):
    template_name = 'student/payment.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('student-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.session.get('student_id')

        if student_id:
            try:
                student = Student.objects.select_related('major__college').get(id=student_id)
                context['student'] = student

                payments = Payment.objects.filter(student=student).order_by('-created_at')
                context['payments'] = payments
                context['total_amount'] = sum(p.amount for p in payments)
                context['paid_amount'] = sum(p.amount for p in payments.filter(status='paid'))
                context['pending_amount'] = sum(p.amount for p in payments.filter(status='pending'))

            except Student.DoesNotExist:
                context['error'] = '学生信息不存在'

        return context


class StudentAnnouncementView(TemplateView):
    template_name = 'student/announcement.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('student-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.session.get('student_id')

        if student_id:
            try:
                student = Student.objects.select_related('major__college').get(id=student_id)
                context['student'] = student

                announcements = Announcement.objects.filter(
                    is_published=True
                ).filter(
                    models.Q(target_audience='all') |
                    models.Q(target_college=student.major.college) |
                    models.Q(target_major=student.major)
                ).order_by('-published_at')

                context['announcements'] = announcements

            except Student.DoesNotExist:
                context['error'] = '学生信息不存在'

        return context


class StudentFAQView(TemplateView):
    template_name = 'student/faq.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('student-login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.session.get('student_id')

        if student_id:
            try:
                student = Student.objects.select_related('major__college').get(id=student_id)
                context['student'] = student

                faqs = FAQ.objects.filter(
                    is_published=True,
                    is_answered=True
                ).order_by('-created_at')

                context['faqs'] = faqs

            except Student.DoesNotExist:
                context['error'] = '学生信息不存在'

        return context
