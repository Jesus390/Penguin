from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.professional import professional_bp
from app.decorators import role_required
from app.models.professional import Professional
from app.extensions import db

@professional_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('professional')
def profile():
    existing = Professional.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        profession = request.form['profession']
        location = request.form['location']
        bio = request.form['bio']

        if existing:
            existing.profession = profession
            existing.location = location
            existing.bio = bio
        else:
            new_profile = Professional(
                user_id=current_user.id,
                profession=profession,
                location=location,
                bio=bio
            )
            db.session.add(new_profile)
        
        db.session.commit()
        flash('Perfil profesional actualizado.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('professional/profile.html', professional=existing)
