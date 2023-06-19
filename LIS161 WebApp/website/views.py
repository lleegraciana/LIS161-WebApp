from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Deliverable
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        task = request.form.get('task')
        category = request.form.get('category1')
        notes = request.form.get('notesarea')
        duedate = request.form.get('ddl')

        if len(task) <1 or category is None or notes is None or duedate is None:
            flash ('task information missing', category='error')
            return redirect('/dashboard')  

        else:
            new_deliverable = Deliverable(
                entry=task, 
                category=category, 
                notes = notes, 
                duedate = duedate, 
                user_id=current_user.id)
            db.session.add(new_deliverable)
            db.session.commit()
            flash ('Added task', category='success')
   
    return render_template('dashboard.html', user=current_user)

#route for updating task
@views.route('/deliverables/<int:deliverable_id>/update', methods=['GET', 'POST'])
@login_required
def update_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)

    if request.method == 'POST':
        # Update the deliverable with the new values
        deliverable.entry = request.form.get('entry')
        deliverable.duedate = request.form.get('duedate')
        deliverable.category = request.form.get('category')
        deliverable.notes = request.form.get('notes')
        db.session.commit()
        flash('Deliverable updated', category='success')
        return redirect(url_for('views.dashboard'))  # Redirect to the dashboard route

    return render_template('update.html', deliverable=deliverable)

# Route for deleting a task
@views.route('/deliverables/<int:deliverable_id>/delete', methods=['POST'])
def delete_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    db.session.delete(deliverable)
    db.session.commit()
    flash('Task deleted', category='success')
    return redirect('/dashboard')