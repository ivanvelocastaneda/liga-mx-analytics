from django.shortcuts import render
from django.db import connection

def dashboard_view(request):
    # Helper to format view names
    def format_view_name(view_name):
        return view_name.replace('_', ' ').title()

    # 1️⃣ Get all view names
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_schema = DATABASE()
        """)
        view_names = [row[0] for row in cursor.fetchall()]

    # Pair real name with formatted display name
    view_names = [(view, format_view_name(view)) for view in view_names]

    # 2️⃣ See if user asked for a particular view
    selected = request.GET.get('view')  # e.g. ?view=Team_MVPs
    view_data = None

    if selected and selected in [view for view, _ in view_names]:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{selected}` LIMIT 100")
            cols = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        view_data = {
            'name': format_view_name(selected),
            'columns': cols,
            'rows': rows,
        }

    # 3️⃣ Render everything
    return render(request, 'dashboard.html', {
        'view_names': view_names,  # List of (real_name, display_name)
        'view_data': view_data,
    })
