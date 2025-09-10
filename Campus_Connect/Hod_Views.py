from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, Session_Year, CustomUser, Student, Staff, Subject, Session_Year, Staff_Notification, Staff_Leave, Staff_Feedback, Student_Notification, Student_Feedback, Student_Leave, Attendance, Attendance_Report, Auditorium_Booking, Timetable
from django.contrib import messages

# Login Decorator for login Access Prevention
@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender = 'Male').count()
    student_gender_female = Student.objects.filter(gender = 'Female').count()


    context = {
        'student_count' : student_count,
        'staff_count' : staff_count,
        'course_count' : course_count,
        'subject_count' : subject_count,
        'student_gender_male' : student_gender_male,
        'student_gender_female': student_gender_female,
    }
    return render(request, 'Hod/home.html',context)

# Added Student Here
@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')              # Here are files for image
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email Is Already Taken")
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username Is Already Taken")
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3,
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id = course_id)
            session_year = Session_Year.objects.get(id = session_year_id)

            student = Student(
                admin = user,
                address = address,
                session_year_id = session_year,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name + ' ' + user.last_name + ' Successfully Added')
            return redirect('add_student')

        # print(profile_pic,first_name,last_name,email,username,password,address,gender,course_id,session_year_id)

    context ={
        'course' : course,
        'session_year' : session_year,
    }

    return render(request, 'Hod/add_student.html',context)

# Added View Student Here
@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student' : student,
    }
    return render(request, 'Hod/view_student.html',context)

# Added Edit Student Here
@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()


    context = {
        'student' : student,
        'course' : course,
        'session_year' : session_year,
    }
    return render(request, 'Hod/edit_student.html',context)

# Added Update Student Here
@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')              #Here are files for image
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        user = CustomUser.objects.get(id = student_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender

        course = Course.objects.get(id = course_id)
        student.course_id = course

        session_year = Session_Year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.save()

        messages.success(request,'Records Are Successfully Updated..!')
        return redirect('view_student')

    return render(request, 'Hod/edit_student.html')

# Added Delete Student Here
@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request, 'Record Are Successfully Deleted..!')
    return redirect('view_student')

# Added Courses Here
@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')

        course = Course(
            name = course_name,
        )
        course.save()
        messages.success(request,'Course Is Successfully Created')
        return redirect('add_course')

    return render(request, 'Hod/add_course.html')

# Added View Course Here
@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course' : course,
    }
    return render(request, 'Hod/view_course.html',context)

# Added Edit Course Here
@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id = id)
    context = {
        'course' : course,
    }
    return render(request, 'Hod/edit_course.html',context)

# Added Update Course Here
@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id = course_id)
        course.name = course_name
        course.save()
        messages.success(request, 'Course Is Successfully Updated')
        return redirect('view_course')
    return render(request, 'Hod/edit_course.html')

# Added Delete Course Here
@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Course Is Successfully Deleted..!')
    return redirect('view_course')

# Added Staff Here
@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == 'POST':
        # staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')              #Here are files for image
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request, "Email Is Already Taken..!")
            return redirect('add_staff')
        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request,"Username Is Already Taken..!")
            return redirect('add_staff')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 2,
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = gender
            )
            staff.save()

            messages.success(request, user.first_name + ' ' + user.last_name + ' Successfully Added')
            return redirect('add_staff')

    return render(request, 'Hod/add_staff.html')

# Added View Staff Here
@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff' : staff,
    }
    return render(request, 'Hod/view_staff.html',context)

# Added Edit Staff Here
@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id = id)
    context={
        'staff' : staff,
    }
    return render(request, 'Hod/edit_staff.html',context)

# Added Update Staff Here
@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')  # files for img
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id = staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password != None and password != '':
            user.set_password(password)
        if profile_pic != None and profile_pic != '':
            user.profile_pic = profile_pic

        user.save()

        staff = Staff.objects.get(admin = staff_id)
        staff.address = address
        staff.gender = gender

        staff.save()

        messages.success(request,'Staff Is Successfully Updated..!')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')

# Added Delete Staff Here
@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    staff = CustomUser.objects.get(id = admin)
    staff.delete()
    messages.success(request, 'Record Are Successfully Deleted..!')
    return redirect('view_staff')

# Added Subject Here
@login_required(login_url='/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request,'Subject Is Successfully Added..!')
        return redirect('add_subject')

    context = {
        'course' : course,
        'staff' : staff,
    }
    return render(request, 'Hod/add_subject.html',context)

# Added View Subject Here
@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()
    context = {
        'subject' : subject,
    }
    return render(request, 'Hod/view_subject.html',context)

# Added Edit Subject Here
@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()

    context = {
        'subject' : subject,
        'course': course,
        'staff': staff,
    }
    return render(request, 'Hod/edit_subject.html',context)

# Added Update Subject Here
@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)
        subject = Subject(
            id = subject_id,
            name = subject_name,
            course = course,
            staff = staff,
        )
        subject.save()
        messages.success(request, 'Subjects Is Successfully Updated..!')
    return redirect('view_subject')

# Added Delete Subject Here
@login_required(login_url='/')
def DELETE_SUBJECT(request,id):
    subject = Subject.objects.filter(id = id)
    subject.delete()
    messages.success(request, 'Subject Is Successfully Deleted..!')
    return redirect('view_subject')

# Added Session Here
@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Is Successfully Created..!')
        return redirect('add_session')
    return render(request,'Hod/add_session.html')

# Added View Session Here
@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context = {
        'session' : session,
    }
    return render(request,'Hod/view_session.html',context)

# Added Edit Session Here
@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session = Session_Year.objects.filter(id = id)
    context = {
        'session' : session,
    }
    return render(request,'Hod/edit_session.html',context)

# Added Update Session Here
@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request, 'Session Is Successfully Updated..!')
    return redirect('view_session')

# Added Delete Session Here
@login_required(login_url='/')
def DELETE_SESSION(request, id):
    session = Session_Year.objects.get(id = id)
    session.delete()
    messages.success(request, 'Session Is Successfully Deleted..!')
    return redirect('view_session')

# Added Staff Send-Notification Here
@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    seen_notification = Staff_Notification.objects.all().order_by('-id')[0:5] # [0:5] It is to display latest 5 Notifications only..
    context = {
        'staff' : staff,
        'seen_notification' : seen_notification,
    }
    return render(request,'Hod/staff_notification.html',context)

# Added Save-Satff-Notification Here
@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request,'Notification Is Successfully Sent')
        return redirect('staff_send_notification')

# Added Save-All-Staff-Notification Here
@login_required(login_url='/')
def SAVE_ALL_STAFF_NOTIFICATION(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        staff_members = Staff.objects.all()
        # Iterate over each staff member and save notification
        # for staff_member in staff_members:
        #     notification = Staff_Notification.objects.create(
        #         staff_id=staff_member,
        #         message=message,
        #     )
        for staff_member in staff_members:
            # print(f'Sending notification to {staff_member.admin.first_name} {staff_member.admin.last_name}: {message}')
            # print(f'Sending notification to {staff_member.admin.id} : {message}')
            notification = Staff_Notification(
                staff_id= staff_member,
                message=message,
            )
            notification.save()
        messages.success(request, 'Notification sent to all staff members successfully.')
        return redirect('staff_send_notification')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('staff_send_notification')

# Added Staff Leave View Here
@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_Leave.objects.all()
    context = {
        'staff_leave' : staff_leave,
    }
    return render(request,'Hod/staff_leave.html',context)

# Added Staff Approve Leave Here
@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request,id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')

# Added Satff Disapprove Here
@login_required(login_url='/')
def STAFF_DISAPPROVE_LEAVE(request,id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

# Added Satff Feedback Reply Here
@login_required(login_url='/')
def STAFF_FEEDBACK_REPLY(request):
    feedback = Staff_Feedback.objects.all()
    feedback_history = Staff_Feedback.objects.all().order_by('-id')[0:5]  # It is  to get latest feedback first..

    context = {
        'feedback' : feedback,
        'feedback_history' : feedback_history
    }
    return render(request, 'Hod/staff_feedback.html',context)

# Added Staff Feedback Reply Save Here
@login_required(login_url='/')
def STAFF_FEEDBACK_REPLY_SAVE(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()

        return redirect('staff_feedback_reply')

# Added Send Student Notification Here
@login_required(login_url='/')
def SEND_STUDENT_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context = {
        'student' : student,
        'notification' : notification,
    }

    return render(request, 'Hod/student_notification.html',context)

# Added Save Student Notification
@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        student = Student.objects.get(admin = student_id)
        notification = Student_Notification(
            student_id = student,
            message = message,
        )
        notification.save()
        messages.success(request,'Notification Is Successfully Sent')
        return redirect('send_student_notification')

# Added Save All Student Notification Here
@login_required(login_url='/')
def SAVE_ALL_STUDENT_NOTIFICATION(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        student_members = Student.objects.all()
        for student_member in student_members:
            notification = Student_Notification(
                student_id = student_member,
                message=message,
            )
            notification.save()
        messages.success(request, 'Notification sent to all Students Successfully.')
        return redirect('send_student_notification')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('send_student_notification')

# Added Student Feedback Reply Here
@login_required(login_url='/')
def STUDENT_FEEDBACK_REPLY(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]   # It is to get latest feedback first..

    context = {
        'feedback' : feedback,
        'feedback_history' : feedback_history,
    }
    return render(request, 'Hod/student_feedback.html',context)

# Added Student Feedback Reply Save Here
@login_required(login_url='/')
def STUDENT_FEEDBACK_REPLY_SAVE(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Student_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
    return redirect('student_feedback_reply')

# Added Student Leave View Here
@login_required(login_url='/')
def STUDENT_LEAVE_VIEW(request):
    student_leave = Student_Leave.objects.all()
    context = {
        'student_leave' : student_leave,
    }
    return render(request, 'Hod/student_leave.html',context)

# Added Student Approve Leave Here
@login_required(login_url='/')
def STUDENT_APPROVE_LEAVE(request,id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')

# Added Student Disapprove Leave Here
@login_required(login_url='/')
def STUDENT_DISAPPROVE_LEAVE(request,id):
    leave = Student_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')

# Added Hod View Attendance Here
@login_required(login_url='/')
def HOD_VIEW_ATTENDANCE(request):
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)

        for i in attendance:
            attendance_id = i.id
            attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }
    return render(request, 'Hod/view_attendance.html',context)

# Added HOD Book Auditorium Here
@login_required(login_url='/')
def HOD_BOOK_AUDITORIUM(request):
    auditorium_booking = Auditorium_Booking.objects.all()
    context = {
        'auditorium_booking' : auditorium_booking,
    }
    return render(request, 'Hod/book_auditorium.html',context)

# Added HOF Book Auditorium Approve Here
@login_required(login_url='/')
def HOD_BOOK_AUDITORIUM_APPROVE(request,id):
    booking = Auditorium_Booking.objects.get(id = id)
    booking.status = 1
    booking.save()
    return redirect('hod_book_auditorium')

# Added HOD Book Auditorium Disapprove Here
@login_required(login_url='/')
def HOD_BOOK_AUDITORIUM_DISAPPROVE(request,id):
    booking = Auditorium_Booking.objects.get(id = id)
    booking.status = 2
    booking.save()
    return redirect('hod_book_auditorium')

# Added HOD View Timetable View
@login_required(login_url='/')
def HOD_VIEW_TIMETABLE(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_course = None
    get_session_year = None
    timetable = None

    if action is not None:
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')

        get_course = Course.objects.get(id=course_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        timetable = Timetable.objects.filter(course=get_course, session_year=get_session_year)

        # attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)

        # for i in attendance:
        #     attendance_id = i.id
        #     attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)

    context = {
        'course' : course,
        'session_year': session_year,
        'action': action,
        'get_course': get_course,
        'get_session_year': get_session_year,
        'timetable': timetable,
    }
    return render(request, 'Hod/view_timetable.html',context)

# Added HOD Edit Timetable Here
@login_required(login_url='/')
def HOD_EDIT_TIMETABLE(request,id):
    timetable = Timetable.objects.get(id=id)

    context = {
        'timetable': timetable,
    }
    return render(request, 'Hod/edit_timetable.html', context)

# Added Updated Timetable Here
@login_required(login_url='/')
def UPDATE_TIMETABLE(request):
    if request.method == 'POST':
        tt_id = request.POST.get('tt_id')
        course_name = request.POST.get('course_name')
        session_year1 = request.POST.get('session_year1')
        lecture_number1 = request.POST.get('lecture_number1')
        time_slot1 = request.POST.get('time_slot1')
        monday1 = request.POST.get('monday1')
        tuesday1 = request.POST.get('tuesday1')
        wednesday1 = request.POST.get('wednesday1')
        thursday1 = request.POST.get('thursday1')
        friday1 = request.POST.get('friday1')
        saturday1 = request.POST.get('saturday1')

        course1 = Course.objects.get(name=course_name)
        session_year2 = Session_Year.objects.get(session_start=session_year1[:10])

        timetable = Timetable(
            id = tt_id,
            course = course1,
            session_year = session_year2,
            lecture_number = lecture_number1,
            time_slot = time_slot1,
            monday = monday1,
            tuesday = tuesday1,
            wednesday = wednesday1,
            thursday = thursday1,
            friday = friday1,
            saturday = saturday1,
        )
        timetable.save()
        messages.success(request, 'Timetable Is Successfully Updated..!')
    return redirect('hod_view_timetable')

# Added Timetable Here
@login_required(login_url='/')
def ADD_TIMETABLE(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    lec_no = [1, 2, 3, 4, 5]
    time_slots = ["12:00pm- 1:00om", "1:00pm - 2:00pm", "2:00pm - 3:00pm", "3:00pm - 4:00pm"]

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        lecture_number = request.POST.get('lecture_number')
        time_slot1 = request.POST.get('time_slot1')
        monday1 = request.POST.get('monday1')
        tuesday1 = request.POST.get('tuesday1')
        wednesday1 = request.POST.get('wednesday1')
        thursday1 = request.POST.get('thursday1')
        friday1 = request.POST.get('friday1')
        saturday1 = request.POST.get('saturday1')


        course = Course.objects.get(id=course_id)
        session_year = Session_Year.objects.get(id=session_year_id)

        # Check if the Timetable Fields are Available..
        if Timetable.objects.filter(course=course, session_year=session_year, lecture_number=lecture_number).exists():
            messages.warning(request, 'The selected Course and Lecture are already Added. Please choose different Lecture.')
        else:
            timetable = Timetable(
                course=course,
                session_year=session_year,
                lecture_number=lecture_number,
                time_slot=time_slot1,
                monday=monday1,
                tuesday=tuesday1,
                wednesday=wednesday1,
                thursday=thursday1,
                friday=friday1,
                saturday=saturday1,
            )
            timetable.save()
            messages.success(request, 'Timetable Is Successfully Added..!')
        return redirect('add_timetable')

    context = {
        'course': course,
        'session_year': session_year,
        'lec_no': lec_no,
        'time_slots': time_slots,
    }
    return render(request, 'Hod/add_timetable.html', context)