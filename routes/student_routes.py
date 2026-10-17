from flask import (
    Blueprint, 
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
    )
from database import (
    get_all_students,
    add_student,
    get_student_by_id,
    update_student,
    delete_student as delete_student_db,
    filter_students,
    get_filtered_student_count,
    get_all_courses,
    assign_course,
    get_student_courses,
    remove_student_course
    )
from auth import login_required, admin_required
from werkzeug.utils import secure_filename
from forms import StudentForm, EditStudentForm, AssignCourseForm
import os
import uuid

student_bp = Blueprint(
    "student",
    __name__
)


ALLOWED_EXTENSIONS = {'png','jpg','jpeg','gif'}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
        )

@student_bp.route("/students")
@login_required
def student_list():
    page = request.args.get("page",1,type=int)

    search = request.args.get("search","")

    course = request.args.get("course","")

    if page < 1:
        page = 1

    per_page = 10

    offset = (page - 1) * per_page

    students = filter_students(search, course, per_page, offset)

    total_students = get_filtered_student_count(search,course)

    total_pages = max(1,(total_students + per_page - 1) // per_page) 

    if page > total_pages:
        page = total_pages

    return render_template(
        "students.html",
        students=students,
        search=search,
        course=course,
        page=page,
        total_pages=total_pages
    )

@student_bp.route("/add-student",methods=['GET','POST'])
@admin_required
def add_student_page():

    form = StudentForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        course = form.course.data.strip()

        file = form.photo.data

        photo = ""

        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Invalid file type","danger")
                return redirect(url_for("student.add_student_page"))
            
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit(".",1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{extension}"

            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"],filename))

            photo = filename

        add_student(name,course,photo)

        flash("Student Added Successfully","success")

        return redirect(url_for('student.student_list'))

    return render_template("add_student.html",form=form)

@student_bp.route("/student/<int:id>")
@login_required
def student_details(id):
    student = get_student_by_id(id)

    if student is None:
        return render_template("404.html"),404

    courses = get_student_courses(id)

    return render_template("student.html",student=student,courses=courses)

@student_bp.route("/edit-student/<int:id>",methods=['GET','POST'])
@admin_required
def edit_student(id):
    student = get_student_by_id(id)

    if student is None:
        return render_template("404.html"),404

    form = EditStudentForm()

    if request.method == "GET":
        form.name.data = student["name"]
        form.course.data = student["course"]

    if form.validate_on_submit():
        name = form.name.data.strip()
        course = form.course.data.strip()
        file = form.photo.data
        new_photo = None

        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Invalid file type","danger")
                return redirect(url_for("student.edit_student",id=id))
            
            original_filename = secure_filename(file.filename)
            extension = original_filename.rsplit(".",1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{extension}"

            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"]
            ,new_filename))

            new_photo = new_filename

            # delete old photo
            if student["photo"]:
                old_photo_path = os.path.join(current_app.config["UPLOAD_FOLDER"],student["photo"])

                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)

        update_student(id,name,course,new_photo)

        flash("Student Updated Successfully","success")

        return redirect(url_for("student.student_details",id=id))
    return render_template("edit_student.html",student=student, form=form)

@student_bp.route("/delete-student/<int:id>", methods=["POST"])
@admin_required
def delete_student(id):
    student = get_student_by_id(id)

    if student is None:
        return render_template("404.html"), 404

    # Step 1: Remember the student's photo filename
    photo = student["photo"]

    # Step 2: Delete course assignments and student record
    delete_student_db(id)

    # Step 3: Delete photo after successful database deletion
    if photo:
        filename = os.path.basename(photo)

        photo_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

        if os.path.isfile(photo_path):
             os.remove(photo_path)

    # Step 4: Display success message
    flash("Student Deleted Successfully", "danger")

    return redirect(url_for("student.student_list"))


@student_bp.route(
    "/student/<int:id>/assign-course",
    methods=["GET", "POST"]
)
@admin_required
def assign_student_course(id):

    student = get_student_by_id(id)

    if student is None:
        return render_template("404.html"), 404

    courses = get_all_courses()

    form = AssignCourseForm()

    form.course_id.choices = [
        (course["id"], course["name"])
        for course in courses
    ]

    if form.validate_on_submit():

        try:

            assign_course(
                id,
                form.course_id.data
            )

            flash(
                "Course Assigned Successfully",
                "success"
            )

        except Exception:

            flash(
                "Course is already assigned.",
                "danger"
            )

        return redirect(
            url_for(
                "student.student_details",
                id=id
            )
        )

    return render_template(
        "assign_course.html",
        student=student,
        courses=courses,
        form=form
    )


@student_bp.route("/student/<int:student_id>/remove-course/<int:course_id>",methods=["POST"])
@admin_required
def remove_course(student_id,course_id):
    remove_student_course(
        student_id,course_id
    )
    flash("Course removed Successfully","success")

    return redirect(url_for("student.student_details",id=student_id))