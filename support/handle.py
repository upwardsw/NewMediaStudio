'''
数据处理类：
handler：
处理请假条、会议记录、公告
'''

class handler:
    @staticmethod
    def handle_note(data):
        new_data = []

        for i in data:
            b = dict(request_id = i.num_id,
                     request_name = i.person,
                     request_time = str(i.time),
                     request_text = i.notetext,
                     request_status = i.status)
            new_data.append(b)

        return new_data

    @staticmethod
    def handle_meeting(data):
        new_data = []

        for i in data:
            b = dict(id = i.id,
                     time = str(i.time),
                     host = i.host,
                     recordperson = i.recordperson,
                     late = i.late,
                     leave = i.leave,
                     join = i.join,
                     recordtext = i.recordtext)
            new_data.append(b)

        return new_data

    @staticmethod
    def handle_notice(data):
        new_data = []

        for i in data:
            b = dict(id = i.id,
                     time = str(i.time),
                     name = i.person,
                     notice = i.noticetext)
            new_data.append(b)

        return new_data

'''
数据处理类：
standard：
处理空闲时间、个人信息、
'''

class standard:
    @staticmethod
    def freetime(data):
        new_data=[data.timea,data.timeb,data.timec,data.timed,data.timee,
                  data.timef,data.timeg,data.timeh,data.timei,data.timej,
                  data.timek,data.timel,data.timem,data.timen]
        return new_data

    @staticmethod
    def detailinfo(data):
        new_data = {"student_id":data.id, "name": data.name, "department": data.department,
                "student_class": data.Class, "school": data.school, "position": data.position,
                "sex": data.sex, "email": data.email, "tel": data.tel, "qq": data.qq,
                "picture_id": data.image,"native_place":data.place}
        return new_data


    @staticmethod
    def change_detailinfo(data,datas):
        data.Class=datas["student_class"]
        data.school=datas["school"]
        data.tel=datas["tel"]
        data.qq=datas["qq"]
        data.email=datas["email"]
        data.place=datas["native_place"]
        return data

    @staticmethod
    def change_freetime(data,datas):
        data.timea = datas[1]
        data.timeb = datas[2]
        data.timec = datas[3]
        data.timed = datas[4]
        data.timee = datas[5]
        data.timef = datas[6]
        data.timeg = datas[7]
        data.timeh = datas[8]
        data.timei = datas[9]
        data.timej = datas[10]
        data.timek = datas[11]
        data.timel = datas[12]
        data.timem = datas[13]
        data.timen = datas[14]
        return data


class all_methods:
    # 登入部分
    # 修改密码部分
    @staticmethod
    def exist_data(data):
        if data == None:
            return 2
        else:
            # 用户存在
            return 1

    # 修改密码和忘记密码
    @staticmethod
    def test_data(data, name, tel):
        # print(data.tel, tel)
        # print(data.name, name)
        if data.tel == tel and data.name == name:
            # 可修改密码
            return 1
        else:
            # 修改密码失败
            return 2