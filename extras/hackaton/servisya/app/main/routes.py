from flask import render_template
from flask_login import login_required, current_user
from app.main import main_bp

from app.extensions import db


from app.models.professional import Professional
from app.models.user_search_history import UserSearchHistory
from app.models.user import User
from flask import request

from flask import redirect, url_for, flash
from datetime import datetime
from app.models.service_request import ServiceRequest

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('main/dashboard.html', user=current_user)


@main_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    results = []

    if query:
        results = Professional.query.filter(Professional.profession.ilike(f'%{query}%')).all()

    results = []

    if query:
        results = Professional.query.filter(Professional.profession.ilike(f'%{query}%')).all()

        if current_user.is_authenticated:
            history = UserSearchHistory(user_id=current_user.id, search_term=query)
            db.session.add(history)
            db.session.commit()

    return render_template('main/search_results.html', query=query, results=results)


# @main_bp.route('/search')
# def search():
#     query = request.args.get('q', '').strip()
#     results = []

#     if query:
#         results = Professional.query.filter(Professional.profession.ilike(f'%{query}%')).all()

#         if current_user.is_authenticated:
#             history = UserSearchHistory(user_id=current_user.id, search_term=query)
#             db.session.add(history)
#             db.session.commit()

#     return render_template('main/search_results.html', query=query, results=results)


@main_bp.route('/request_service/<int:professional_id>', methods=['POST'])
@login_required
def request_service(professional_id):
    description = request.form.get('description', '')
    new_request = ServiceRequest(
        user_id=current_user.id,
        professional_id=professional_id,
        description=description
    )
    db.session.add(new_request)
    db.session.commit()
    flash('Solicitud enviada al profesional.')
    return redirect(url_for('main.index'))

@main_bp.route('/respond_request/<int:request_id>/<string:action>', methods=['POST'])
@login_required
def respond_request(request_id, action):
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.professional.user_id != current_user.id:
        flash('No tienes permiso para responder a esta solicitud.')
        return redirect(url_for('main.dashboard'))

    if action in ['accepted', 'rejected']:
        service_request.status = action
        service_request.responded_at = datetime.utcnow()
        db.session.commit()
        flash(f'Solicitud {action}.')
    else:
        flash('Acción no válida.')

    return redirect(url_for('main.dashboard'))
