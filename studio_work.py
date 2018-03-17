import json
import os

from flask import Flask, request, Response
from flask_cors import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import *
from sqlalchemy.orm import *
from werkzeug.security import generate_password_hash, check_password_hash

from support.config import appconfig
from support.handle import handler, standard, all_methods
from support.sql_table import leave_note, meetingrecord, notice, detailinfo, freetime, Basicinfo

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = '*8p.3y?1t!h@o#n$8%^5&7*9'
engine = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}?charset=utf8'.format(appconfig.user, appconfig.password, appconfig.host,
                                                          appconfig.dbname), encoding="utf-8", echo=True)
DBSession = sessionmaker(bind=engine)

'''
李盼盼部分：

'''
# login模块设置：
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"


# session过期时间设置（无用）：
# session.permanent = True
# app.permanent_session_lifetime = datetime.timedelta(minutes=30)

@login_manager.user_loader
def load_user(user_id):
    session = DBSession()
    user = session.query(Basicinfo).filter(Basicinfo.id == user_id).first()
    session.close()
    return user


# 添加一个新用户
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        a = request.get_data()
        print(a)
        a = str(a, encoding='utf-8')
        a = json.loads(a)
        student_id = a.get('student_id')
        name = a.get('name')
        department = a.get('department')
        zhiwei = a.get('zhiwei')
        password = '123456'
        print(student_id, name, password)
        session = DBSession()
        new_user = Basicinfo(id=student_id, name=name, department=department, zhiwei=zhiwei,
                             password=generate_password_hash(password)[20:])
        print(new_user)
        session.add(new_user)
        session.commit()
        session.close()
        return Response(response=json.dumps(dict(is_success=True)), mimetype='application/json', status=200)
    else:
        return 'Request method error!'


# judt for test
@app.route('/test/', methods=['GET'])
def test():
    id = 6103115049
    session = DBSession()
    student = session.query(Basicinfo).filter(Basicinfo.id == id).first()
    login_user(student, remember=True)
    print(student.id)
    return 'OK'


# 登入
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        a = request.get_json()
        a = str(a, encoding='utf-8')
        a = json.loads(a)
        student_id = a.get('student_id')
        password = a.get('password')

        session = DBSession()
        student = session.query(Basicinfo).filter(Basicinfo.id == student_id).first()
        session.close()

        if student != None and check_password_hash('pbkdf2:sha256:50000$' + student.password, password):
            login_user(student, remember=True)

            return Response(response=json.dumps(dict(is_success=True)), mimetype='application/json', status=200)
        else:
            return Response(response=json.dumps(dict(is_success=False)), mimetype='application/json', status=200)

    else:
        return 'Request method error!'


@app.route('/check', methods=['GET', "POST"])
def check():
    print(current_user.id)
    return str(current_user.id)


# 登出
@app.route('/logout')
def logout():
    logout_user()
    return Response(response=json.dumps(dict(is_success=True)), mimetype='application/json', status=200)


# 修改密码
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        a = request.get_json()
        a = str(a, encoding='utf-8')

        a = json.loads(a)
        student_id = a.get('student_id')
        name = a.get('name')
        tel = a.get('tel')
        old_password = a.get('old_password')
        new_password = a.get('new_password')
        session = DBSession()
        get_data = session.query(detailinfo).filter(detailinfo.id == student_id).first()
        get_data2 = session.query(Basicinfo).filter(Basicinfo.id == student_id).first()
        exist_data = all_methods.exist_data(get_data2)
        test_data = all_methods.test_data(get_data, name, tel)
        if exist_data == 1 and test_data == 1 and check_password_hash('pbkdf2:sha256:50000$' + get_data2.password,
                                                                      old_password):
            session.query(Basicinfo).filter(Basicinfo.id == student_id).update(
                {'password': generate_password_hash(new_password)[20:]})
            session.commit()
            session.close()
            return Response(response=json.dumps(dict(is_success=True)), mimetype='application/json', status=200)
        else:
            session.close()
            return Response(response=json.dumps(dict(is_success=False)), mimetype='application/json', status=200)


# 忘记密码
@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        a = request.get_json()
        a = str(a, encoding='utf-8')

        a = json.loads(a)
        student_id = a.get('student_id')
        name = a.get('name')
        tel = a.get('tel')
        new_password = a.get('new_password')
        session = DBSession()
        get_data = session.query(detailinfo).filter(detailinfo.id == student_id).first()
        get_data2 = session.query(Basicinfo).filter(Basicinfo.id == student_id).first()
        exist_data = all_methods.exist_data(get_data2)
        change_data = all_methods.test_data(get_data, name, tel)
        if exist_data == 1 and change_data == 1:
            session.query(Basicinfo).filter(Basicinfo.id == student_id).update(
                {'password': generate_password_hash(new_password)[20:]})
            session.commit()
            session.close()
            return Response(response=json.dumps(dict(is_success=True)), mimetype='application/json', status=200)
        else:
            session.close()
            return Response(response=json.dumps(dict(is_success=False)), mimetype='application/json', status=200)


'''
石立军部分：
请假条填写（部员）
request_nrnote[post](json:request_name,request_time,request_text)[retu](json:is_success)

请假条查看（管理员查看并且审核，部员审核状态）
show_request_note[post](json:)[return](json:list[json:request_id,request_name,request_time,request_text,request_status]
show_request_note_admin[post](json:)[return](json:list[json:request_id,request_name,request_time,request_text,request_status])
check_request_note[post](json:request_id,request_opinion)[return](json:is_success)

会议记录填写（管理员权限）
add_meeting_notes[post](json:time,host,recordperson,late,leave,join, recordtext)[return](json:is_success)

会议记录查看（部员）
show_meeting_notes[post](json:)[return](json:list[id,time,host,recordperson,late,leave,join, recordtext])

公告发布（管理员）
add_notice[post](json:name,time,notice)[return](json:is_success)

公告查看（全部公告，管理员公告）
show_notice[post](json:)[return](json:list[id,time,name,notice])
show_my_notice[post](json:)[return](json: list[id,time,name,notice])
'''


# 请假条填写（部员）
@app.route('/request_note', methods=["POST"])
def request_note():
    if request.method == 'POST':
        connect = DBSession()

        # 得到数据
        try:
            post_data = request.get_json()
            post_data = str(post_data, encoding='utf-8')

            post_data = json.loads(post_data)
            request_name = post_data.get('request_name')
            request_time = post_data.get('request_time')
            request_text = post_data.get('request_text')
        except:
            return Response(response=json.dumps(dict(is_success=False)), mimetype="application/json", status=200)

        # 获取最后一个请假条的数据（用于记录id）
        all_note = connect.query(leave_note).all()
        final_note = all_note[-1]

        try:
            new_request = leave_note(num_id=final_note.num_id + 1, person=request_name, time=request_time,
                                     notetext=request_text, status=0)
            connect.add(new_request)
            connect.commit()
        except:
            return Response(response=json.dumps(dict(is_success=False)), mimetype="application/json", status=200)
        return Response(response=json.dumps(dict(is_success=True)), mimetype="application/json", status=200)


# 请假条查看
@app.route('/show_request_note', methods=["POST"])
def show_request_note():
    if request.method == 'POST':
        connect = DBSession()
        data = connect.query(leave_note).filter(leave_note.person ==
                                                (connect.query(Basicinfo).filter(
                                                    Basicinfo.id == current_user.id).first()).name).all()
        data = handler.handle_note(data)

        return Response(response=json.dumps(data), mimetype="application/json", status=200)


# 请假条查看（管理员）
@app.route('/show_request_note_admin', methods=["POST"])
def show_request_note_admin():
    if request.method == 'POST':
        connect = DBSession()

        data = connect.query(leave_note).filter().all()
        data = handler.handle_note(data)

        return Response(response=json.dumps(data), mimetype="application/json", status=200)


# 请假条审批
@app.route('/check_request_note', methods=["POST"])
def check_requexitest_note():
    if request.method == 'POST':
        # 得到json数据
        post_data = request.get_json()
        post_data = str(post_data, encoding='utf-8')

        post_data = json.loads(post_data)
        request_id = post_data.get("request_id")
        request_opinion = post_data.get("request_opinion")

        connect = DBSession()

        # 尝试通过查询请假条
        try:
            old_note = connect.query(leave_note).filter(leave_note.num_id == request_id).first()
            # 尝试修改审查状态
            old_note.status = request_opinion
            connect.commit()
        except:
            return Response(response=json.dumps(dict(is_success=False)), mimetype="application/json", status=200)

        return Response(response=json.dumps(dict(is_success=True)), mimetype="application/json", status=200)


# 会议记录填写
@app.route('/add_meeting_notes', methods=["POST"])
def add_meeting_notes():
    if request.method == "POST":
        connect = DBSession()

        # 得到数据
        try:
            post_data = request.get_json()

            post_data = str(post_data, encoding='utf-8')
            post_data = json.loads(post_data)
            request_time = post_data.get('time')

            request_host = post_data.get('host')
            request_recordperson = post_data.get('recordperson')
            request_late = post_data.get("late")
            request_leave = post_data.get("leave")
            request_join = post_data.get("join")
            request_recordtext = post_data.get("recordtext")
        except:
            return Response(response=json.dumps(dict(is_success=False)), mimetype="application/json", status=200)

        # 获取最后一个会议记录的数据（用于记录id）
        all_meeting = connect.query(meetingrecord).all()
        final_meeting = all_meeting[-1]

        try:
            new_request = meetingrecord(id=final_meeting.id + 1, time=request_time, host=request_host,
                                        recordperson=request_recordperson, late=request_late, leave=request_leave,
                                        join=request_join, recordtext=request_recordtext)
            connect.add(new_request)
            connect.commit()
        except:
            return Response(response=json.dumps(dict(is_success=False)), mimetype="application/json", status=200)
        return Response(response=json.dumps(dict(is_success=True)), mimetype="application/json", status=200)


# 会议记录查看
@app.route('/show_meeting_notes', methods=["POST"])
def show_meeting_notes():
    if request.method == "POST":
        connect = DBSession()

        data = connect.query(meetingrecord).filter().all()
        data = handler.handle_meeting(data)

        return Response(response=json.dumps(data), mimetype="application/json", status=200)


# 公告填写
@app.route('/add_notice', methods=["POST"])
def add_notice():
    if request.method == "POST":
        connect = DBSession()

        try:
            data = request.get_json()
            data = str(data, encoding='utf-8')
            data = json.loads(data)

            request_time = data.get("time")
            request_name = data.get("name")
            request_notice = data.get("notice")

            # 获取最后一个公告的数据（用于记录id）
            all_notice = connect.query(notice).all()
            final_notice = all_notice[-1]

            new_notice = notice(id=final_notice.id + 1, time=request_time, person=request_name,
                                noticetext=request_notice)
            connect.add(new_notice)
            connect.commit()
        except:
            return Response(response=json.dumps(dict(is_success=False)), mimetype="application/json", status=200)

        return Response(response=json.dumps(dict(is_success=True)), mimetype="application/json", status=200)


# 公告查看
@app.route('/show_notice', methods=["POST"])
def show_notice():
    if request.method == 'POST':
        connect = DBSession()

        data = connect.query(notice).filter().all()
        data = handler.handle_notice(data)

        return Response(response=json.dumps(data), mimetype="application/json", status=200)


# 查看自己发布的公告（管理员）
@app.route('/show_my_notice', methods=["POST"])
def show_my_notice():
    if request.method == 'POST':
        connect = DBSession()
        data = connect.query(notice).filter(notice.person ==
                                            (connect.query(Basicinfo).filter(
                                                Basicinfo.id == current_user.id).first()).name).all()

        data = handler.handle_notice(data)

        return Response(response=json.dumps(data), mimetype="application/json", status=200)


'''
刘臻部分：
####show_student_info：
return json:student_id,name,department,student_class,school,position,sex,email,tel,qq,picture_id,native_place，free_time(list),is_success

####change_student_base_info：
post json:student_class,school,tel,qq,email,native_place
return json:is_success

####change_student_free_time：
post json:freetime:(list)
return json:is_success

####change_student_picture：
post"file":图片
return json:is_success
'''


# 学生信息显示
# print(os.path.dirname(os.path.abspath(__file__))+'\\templates\photo\\')
@app.route('/show_student_info/', methods=['POST', 'GET'])
def show_student_info():
    # try:
    student_id = current_user.id
    connect = DBSession()
    # datas = request.get_data()
    print(student_id)
    detailinfos = connect.query(detailinfo).filter(detailinfo.id == student_id).first()
    # freetimes = connect.query(freetime).filter(freetime.id == student_id).first()
    # free_time = standard.freetime(freetimes)
    # print(free_time)
    data = standard.detailinfo(detailinfos)
    # data["free_time"] = free_time
    data["is_success"] = True
    connect.close()
    return Response(response=json.dumps(data), mimetype="application/json", status=200)


# except:
#     return Response(response=json.dumps({"is_success": False}), mimetype="application/json", status=200)


# 个人信息修改
@app.route('/change_student_base_info/', methods=['POST'])
def change_student_base_info():
    # post json:student_class,school,tel,qq,email,native_place
    # return json:is_success
    try:
        student_id = current_user.id
        datas = request.get_data()
        data = str(datas, encoding='utf-8')
        datas = json.loads(datas)
        connect = DBSession()
        detailinfos = connect.query(detailinfo).filter(detailinfo.id == student_id).first()
        datas = standard.change_detailinfo(detailinfos, datas)
        connect.add(datas)
        connect.commit()
        connect.close()
        return Response(response=json.dumps({"is_success": True}), mimetype="application/json", status=200)
    except:
        return Response(response=json.dumps({"is_success": False}), mimetype="application/json", status=200)


# 空闲时间修改
@app.route('/change_student_free_time/', methods=['POST'])
def change_student_free_time():
    # 没有计入空闲时间的为零
    # post json:freetime:(list)
    # return json:is_success
    student_id = current_user.id
    if student_id == None:
        return Response(response=json.dumps({"is_success": False}), mimetype="application/json", status=200)
    data = request.get_data()
    data = str(data, encoding='utf-8')
    datas = json.loads(data)
    connect = DBSession()
    new_freetime = [student_id]
    new_freetime.extend(data["freetime"])
    try:
        old_freetime = connect.query(freetime).filter(freetime.id == student_id).first()
        new_freetimes = standard.change_freetime(old_freetime, new_freetime)
    except:
        new_freetimes = freetime(id=new_freetime[0], timea=new_freetime[1], timeb=new_freetime[2],
                                 timec=new_freetime[3], timed=new_freetime[4], timee=new_freetime[5],
                                 timef=new_freetime[6], timeg=new_freetime[7], timeh=new_freetime[8],
                                 timei=new_freetime[9], timej=new_freetime[10], timek=new_freetime[11],
                                 timel=new_freetime[12], timem=new_freetime[13], timen=new_freetime[14])
    connect.add(new_freetimes)
    connect.commit()
    connect.close()
    return Response(response=json.dumps({"is_success": True}), mimetype="application/json", status=200)


# <div class="col-md-4">
#     <form action="" method=post enctype=multipart/form-data>
#         <input type=file name=file><br/>
#         <input type=submit value=Upload>
#     </form>
# </div>
# 获取图片的前段方式，写不来路由
@app.route('/change_student_picture/', methods=['POST'])
def change_student_picture():
    # post"file":图片
    # return json:is_success

    try:
        student_id = current_user.id
        photo = request.files['file']
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\templates\photo\\{}'.format(photo.filename),
                  'wb') as f:
            f.write(photo.read())
        connect = DBSession()
        detailinfos = connect.query(detailinfo).filter(freetime.id == student_id).first()
        detailinfos.image = photo.filename
        connect.add(detailinfos)
        connect.commit()
        connect.close()
        return Response(response=json.dumps({"is_success": True}), mimetype="application/json", status=200)
    except:
        return Response(response=json.dumps({"is_success": False}), mimetype="application/json", status=200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
