from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)

class student(db.Model):
    student_id = db.Column(db.Integer(),primary_key = True,autoincrement= True)
    roll_number = db.Column(db.String(),unique= True,nullable = False)
    first_name = db.Column(db.String(),nullable= False)
    last_name = db.Column(db.String())
    courses= db.relationship("course",backref = "student",secondary="enrollments")
class course(db.Model):
    course_id = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    course_code = db.Column(db.String(25),unique= True,nullable = False)
    course_name = db.Column(db.String(),nullable= False)
    course_description = db.Column(db.String())

class enrollments(db.Model):
    enrollment_id = db.Column(db.Integer(),primary_key = True,autoincrement = True)
    estudent_id = db.Column(db.Integer(),db.ForeignKey(student.student_id),nullable = False)
    ecourse_id = db.Column(db.Integer(),db.ForeignKey(course.course_id),nullable = True)

app.app_context().push()

@app.route("/")
def index():
    all_std = student.query.all()
    return render_template("index.html",all_std = all_std)

@app.route("/student/create",methods=['GET','POST'])
def add_student():
    if request.method =="GET":
        return render_template("add_student.html")
    if request.method == "POST":
        roll = request.form.get('roll')
        s = student.query.filter_by(roll_number=roll).first()
        if s:
            return render_template('already.html')
        else:
            f_name = request.form.get('f_name')
            l_name = request.form.get('l_name')
            courses = request.form.getlist()
            new_s = student(roll_number=roll,first_name = f_name ,last_name = l_name)
            db.session.add()
            db.session.commit()
            for course in courses:
                s_id = new_s.student_id
                new_e = enrollments(estudent_id = s_id,ecourse_id = int(course))
                db.session.add(new_e)
                db.session.commit()
        return redirect("/")
    
@app.route('/student/<int:student>/update')
def up_add(student):
    to_update = student.query.filter_by(student_id = student).first()
    if request.method== "GET":
        return render_template('update_s.html',to_updt = to_update)
    if request.method == "POST":
        f_name = request.form.get("f_name")
        l_name = request.form.get("l_name")
        courses = request.form.getlist("courses")  


        to_update.f_name = f_name
        to_update.l_name = l_name
        to_update.courses = []

        for course in courses:
            s_id = to_update.student_id
            new_e = enrollments(estudent_id=s_id, ecourse_id=int(course))
            db.session.add(new_e)

        db.session.commit()
        return redirect('/')
    
@app.route('/student/<int:s>/delete')
def Del(s):
    to_delete = student.query.get(s)  # Search by primary key
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/student/<int:s>')
def details(s):
    # Student info and the courses he is enrolled in
    infor = student.query.get(s)
    his_courses = infor.courses
    print(his_courses)
    return render_template("student_courses.html", infor=infor, his_courses=his_courses)
if __name__ == "__main__":
    app.run(debug=True)
