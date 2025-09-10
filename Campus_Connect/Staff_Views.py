from django.shortcuts import render, redirect
from app.models import Staff, Staff_Notification, Staff_Leave, Staff_Feedback, Subject, Session_Year, Student, Attendance, Attendance_Report, Student_Result, Auditorium_Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Login Home Url
@login_required(login_url='/')
def HOME(request):
    return render(request,'Staff/home.html')

# Staff Notification url
@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        notification = Staff_Notification.objects.filter(staff_id=staff_id)

        context = {
            'notification' : notification,
        }
        return render(request,'Staff/notifications.html',context)

# Staff Notification Mark Done
@login_required(login_url='/')
def STAFF_NOTIFICATIONS_MARK_AS_DONE(request,status):
    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications')

# Staff Apply Leave url
@login_required(login_url='/')
def STAFF_APPLY_LEAVE(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        staff_leave_history = Staff_Leave.objects.filter(staff_id = staff_id)

        context = {
            'staff_leave_history' : staff_leave_history,
        }
        return render(request,'Staff/apply_leave.html',context)

# Staff Apply Leave Save Url
@login_required(login_url='/')
def STAFF_APPLY_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff = Staff.objects.get(admin = request.user.id)


        leave = Staff_Leave(
            staff_id = staff,
            date = leave_date,
            message = leave_message,
        )
        leave.save()
        messages.success(request, 'Staff Leave Successfully Sent')
    return redirect('staff_apply_leave')

# Staff Feedback Url
@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)
    context = {
        'feedback_history' : feedback_history
    }
    return render(request,'Staff/feedback.html',context)

# Staff Feedback Url
@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin = request.user.id)
        feedback_staff = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = '',
        )
        feedback_staff.save()
        return redirect('staff_feedback')

# Staff Take Attendance Url
@login_required(login_url='/')
def TAKE_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff = staff_id)
    session_year = Session_Year.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id = subject_id)
            get_session_year = Session_Year.objects.get(id = session_year_id)

            subject = Subject.objects.filter(id = subject_id)
            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id = student_id)

    context = {
        'subject' : subject,
        'session_year' : session_year,
        'get_subject' : get_subject,
        'get_session_year' : get_session_year,
        'action' : action,
        'students' : students,
    }
    return render(request,'Staff/take_attendance.html',context)

# Save Attendance Url
@login_required(login_url='/')
def SAVE_ATTENDANCE(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student_id')

        get_subject = Subject.objects.get(id=subject_id)
        get_session_year = Session_Year.objects.get(id=session_year_id)

        attendance = Attendance(
            subject_id = get_subject,
            attendance_date = attendance_date,
            session_year_id = get_session_year,
        )
        attendance.save()

        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)

            present_students = Student.objects.get(id = int_stud)
            attendance_report = Attendance_Report(
                student_id = present_students,
                attendance_id = attendance,
            )
            attendance_report.save()
    return redirect('staff_take_attendance')

# View Attendance Url
@login_required(login_url='/')
def VIEW_ATTENDANCE(request):
    staff_id = Staff.objects.get(admin = request.user.id)
    subject = Subject.objects.filter(staff_id = staff_id)
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

        get_subject = Subject.objects.get(id = subject_id)
        get_session_year = Session_Year.objects.get(id = session_year_id)

        attendance = Attendance.objects.filter(subject_id = get_subject, attendance_date = attendance_date)

        for i in attendance:
            attendance_id = i.id
            attendance_report = Attendance_Report.objects.filter(attendance_id = attendance_id)

    context = {
        'subject' : subject,
        'session_year' : session_year,
        'action' : action,
        'get_subject' : get_subject,
        'get_session_year' : get_session_year,
        'attendance_date' : attendance_date,
        'attendance_report' : attendance_report,
    }
    return render(request,'Staff/view_attendance.html',context)

# Staff Add Result Url
@login_required(login_url='/')
def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(staff_id = staff)
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id = subject_id)
            get_session_year = Session_Year.objects.get(id = session_year_id)

            subjects = Subject.objects.filter(id = subject_id)
            for i in subjects:
                student_id = i.course.id
                students = Student.objects.filter(course_id = student_id)


    context = {
        'subjects' : subjects,
        'session_year' : session_year,
        'action' : action,
        'get_subject' : get_subject,
        'get_session_year' : get_session_year,
        'students' : students,
    }
    return render(request,'Staff/add_result.html',context)

# Staff Save Result Url
@login_required(login_url='/')
def STAFF_SAVE_RESULT(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        exam_mark = request.POST.get('exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id = subject_id)

        check_exist = Student_Result.objects.filter(subject_id = get_subject, student_id = get_student).exists()
        if check_exist:
            result = Student_Result.objects.get(subject_id = get_subject, student_id = get_student)
            result.assignment_mark = assignment_mark
            result.exam_mark = exam_mark
            result.save()
            messages.success(request, 'Result is Successfully Updated..!')
            return redirect('staff_add_result')
        else:
            result = Student_Result(
                student_id = get_student,
                subject_id = get_subject,
                assignment_mark = assignment_mark,
                exam_mark = exam_mark,
            )
            result.save()
            messages.success(request, 'Result is Successfully Added..!')
            return redirect('staff_add_result')

# Staff Book Auditorium Url
@login_required(login_url='/')
def STAFF_BOOK_AUDITORIUM(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id

        auditorium_booking_history = Auditorium_Booking.objects.filter(staff_id=staff_id)

        context = {
            'auditorium_booking_history': auditorium_booking_history,
        }
        return render(request, 'Staff/book_auditorium.html', context)

# Staff Book Auditorium Save Url
@login_required(login_url='/')
def STAFF_BOOK_AUDITORIUM_SAVE(request):
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        purpose = request.POST.get('purpose')

        staff = Staff.objects.get(admin=request.user.id)

        # Check if it is the requested dates are available ...
        if Auditorium_Booking.objects.filter(start_date__lte=end_date, end_date__gte=start_date).exists():
            messages.warning(request, 'The selected dates are already booked. Please choose different dates.')
        else:
            booking = Auditorium_Booking(
                staff_id = staff,
                start_date = start_date,
                end_date = end_date,
                purpose = purpose,
            )
            booking.save()
            messages.success(request, 'Auditorium booking request Successfully Sent..!')
        return redirect('staff_book_auditorium')
