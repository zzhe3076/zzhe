from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.utils import timezone
from welcome_app.models import Student, Announcement, FAQ, College, Major


class AdminIndexView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Student.objects.count()
        checked_in = Student.objects.filter(status='checked_in').count()
        pending = total - checked_in
        check_in_rate = round(checked_in / total * 100, 1) if total > 0 else 0

        context['stats'] = {
            'total': total,
            'checked_in': checked_in,
            'pending': pending,
            'check_in_rate': check_in_rate
        }

        context['college_stats'] = list(
            Student.objects.values('major__college__name')
            .annotate(
                total=Count('id'),
                checked_in=Count('id', filter=Q(status='checked_in'))
            )
            .order_by('-total')[:10]
        )

        context['province_stats'] = list(
            Student.objects.values('origin_province')
            .annotate(
                total=Count('id'),
                checked_in=Count('id', filter=Q(status='checked_in'))
            )
            .order_by('-total')[:10]
        )

        from welcome_app.models import CheckIn
        context['recent_check_ins'] = CheckIn.objects.select_related('student', 'student__major')[:10]

        context['colleges'] = College.objects.all()

        return context


class AdminCheckinView(TemplateView):
    template_name = 'frontend/checkin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Student.objects.count()
        checked_in = Student.objects.filter(status='checked_in').count()
        pending = total - checked_in

        context['stats'] = {
            'total': total,
            'checked_in': checked_in,
            'pending': pending
        }

        today = timezone.now().date()
        from welcome_app.models import CheckIn
        today_checked = CheckIn.objects.filter(created_at__date=today).count()
        context['today_checked'] = today_checked
        context['today_rate'] = round(today_checked / total * 100, 1) if total > 0 else 0

        return context


class AdminStudentsView(TemplateView):
    template_name = 'frontend/students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colleges'] = College.objects.all()
        context['majors'] = Major.objects.select_related('college').all()
        return context
