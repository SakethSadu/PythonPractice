from flask import Blueprint, render_template, request, flash, jsonify #this package has bunch of URLs 
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views',__name__) #defining the Blueprint and naming it as views

@views.route('/',methods = ['GET','POST']) #defining the route - whenever we hit the root which is / here, the following home page code will be executed.
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 2 :
            flash("Note is too short",category='error')

        else:
            new_note = Note(dataNotes=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added successfully", category = 'success')

    return render_template("home.html",user=current_user)


@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

