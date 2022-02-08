
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import user_logged_in
from . import db
from .models import Userlog, User,manlog
from flask_login import login_required, current_user

import json
views = Blueprint("views", __name__)

@views.route('/')
def rehome():
    return render_template("home.html", user=current_user)

@views.route('/home')
def home():
    check = manlog.query.all()
    if len(check) == 0:
        load_database(manlog)

    return render_template("home.html",user=current_user)

def load_database(manlog):
    
    file = open("website/static/Error_Files.json","r")
    use_json = json.load(file)

    for keys in use_json:
        new_log = manlog(num=keys, header=use_json[keys][0], message=use_json[keys][1])
        db.session.add(new_log)
        db.session.commit()

@views.route('/viewuserlog', methods=['POST','GET'])
@login_required
def view_user_log():
    data_obj = db.session.query(
        Userlog.id, #0
        Userlog.error_num, #1 
        Userlog.operator, #2
        Userlog.date, #3
        Userlog.circumstances, #4 
        Userlog.actions, #5
        Userlog.equipment, #6 
        Userlog.prevent #7
        )
    
    list_dict = {}
    
    for entries in data_obj:
        list_dict[entries[0]] = entries
    
    final_dict = {}

    for logs in list_dict:
        num = int(list_dict[logs][2])
        print("Here is our num : " , num)
        date= list_dict[logs][3]
        error_num = list_dict[logs][1] 
        operator = db.session.query(User.firstName).filter(User.id==num)
        circumstance = list_dict[logs][4]
        actions = list_dict[logs][5]
        equipment = list_dict[logs][6]
        prevent= list_dict[logs][7]
        
        final_dict[logs] = [logs, error_num, 
                            operator[0][0],
                            date, 
                            circumstance, 
                            actions, 
                            equipment, 
                            prevent]

    if request.method == "POST":
        num = int(request.form['hidden'])
        return render_template(
            "viewUserLog.html",
            user=current_user, 
            final_dict=final_dict, 
            entry=final_dict[num]
            )

    return render_template(
        "viewUserLog.html",
        user=current_user, 
        final_dict=final_dict, 
        entry=0
        )


@views.route('/viewlog', methods=['POST','GET'])
@login_required
def view_log():
    data_obj = db.session.query(manlog.num, manlog.message, manlog.header)
    use_dict={}

    for err_nums in data_obj:
        use_dict[err_nums[0]]=(err_nums[1], err_nums[2])
    
    if request.method == "POST":
        message_text = use_dict[request.form['hidden']][0]
        header_text = use_dict[request.form['hidden']][1]
        num_text = request.form['hidden']
        
        return render_template("viewlog.html",
                                user=current_user, 
                                use_dict=use_dict, 
                                message_text=message_text, 
                                header_text=header_text,
                                num_text=num_text
                                )    

    return render_template("viewlog.html",
                            user=current_user, 
                            use_dict=use_dict
                            )

@views.route('/createlog', methods=['POST','GET'])
@login_required
def create_log():
    if request.method == 'POST':

        circumstances = request.form.get('circumstance')
        actions = request.form.get('actions')
        error_num = request.form.get('error_num')
        prevent = request.form.get('prevent')
        damage = request.form.get('dmg')
        equipment = request.form.get('equip')
        operator = current_user.id

        if len(circumstances)<=1 or len(actions)<=1 or len(prevent)<=1 or len(error_num)<=1:
            flash("Please fill out all fields", category="error") 
            return render_template("createLog.html", user=current_user)

        if not error_num.isnumeric():
            flash("Please enter a number in the error number field", category="error") 
            return render_template("createLog.html", user=current_user)

        new_user_log = Userlog(
            error_num = error_num,
            is_equipment_broken = damage,
            equipment = equipment,
            circumstances = circumstances,
            actions = actions,
            prevent = prevent,
            operator =operator)

        db.session.add(new_user_log)
        db.session.commit()
        
        return redirect(url_for("views.home"))

    return render_template("createLog.html", user=current_user)