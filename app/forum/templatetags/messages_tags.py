import datetime
from django.utils import timezone
from django import template


register = template.Library()


@register.filter
def minutes_ago(time, minutes):
    return timezone.now() - time < datetime.timedelta(minutes=minutes)
