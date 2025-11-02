from django import template
register = template.Library()

@register.filter
def get_mark_for_assignment(marks_queryset, assignment_id):
    """
    Returns the Mark object for a specific assignment if exists, else None.
    """
    try:
        return marks_queryset.filter(assignment_id=assignment_id).first()
    except Exception:
        return None
