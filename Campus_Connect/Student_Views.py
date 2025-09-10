from django.shortcuts import render, redirect
from app.models import Student_Notification, Student, Student_Feedback, Student_Leave, Subject, Attendance, Attendance_Report, Student_Result, Timetable
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home Url
@login_required(login_url='/')
def HOME(request):
    return render(request,'Student/home.html')

# Student Notification Url
@login_required(login_url='/')
def STUDENT_NOTIFICATIONS(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id

        notification = Student_Notification.objects.filter(student_id = student_id)
        context = {
            'notification' : notification,
        }
        return render(request,'Student/notifications.html',context)

# Student Notification Mark Done Url
@login_required(login_url='/')
def STUDENT_NOTIFICATIONS_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notifications')

# Student Feedback Url
@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        'feedback_history' : feedback_history,
    }
    return render(request,'Student/feedback.html',context)

# Student Feedback Save Url
@login_required(login_url='/')
def STUDENT_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        student_id = Student.objects.get(admin = request.user.id)
        feedback_student = Student_Feedback(
            student_id = student_id,
            feedback = feedback,
            feedback_reply = '',
        )
        feedback_student.save()
        return redirect('student_feedback')

# Student Apply Leave Url
@login_required(login_url='/')
def STUDENT_APPLY_LEAVE(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id

        student_leave_history = Student_Leave.objects.filter(student_id = student_id)

        context = {
            'student_leave_history' : student_leave_history,
        }
        return render(request,'Student/apply_leave.html',context)

# Student Apply Leave Save Url
@login_required(login_url='/')
def STUDENT_APPLY_LEAVE_SAVE(request):
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_id = Student.objects.get(admin = request.user.id)

        student_leave = Student_Leave(
            student_id = student_id,
            date = leave_date,
            message = leave_message,
        )
        student_leave.save()
        messages.success(request, 'Student Leave Successfully Sent')
        return redirect('student_apply_leave')

# Student View Attendance Url
@login_required(login_url='/')
def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(course = student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report =None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id = subject_id)

            # attendance = Attendance.objects.get(subject_id = get_subject)
            attendance_report = Attendance_Report.objects.filter(student_id = student, attendance_id__subject_id = subject_id)


    context = {
        'subjects' : subjects,
        'action' : action,
        'get_subject' : get_subject,
        'attendance_report' : attendance_report,
    }
    return render(request,'Student/view_attendance.html',context)

# Student View Result Url
@login_required(login_url='/')
def STUDENT_VIEW_RESULT(request):
    student = Student.objects.get(admin = request.user.id)
    result = Student_Result.objects.filter(student_id = student)
    mark = None

    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark

        mark = assignment_mark + exam_mark

    context = {
        'result' : result,
        'mark' : mark,
    }
    return render(request,'Student/view_result.html',context)


# Student View Timetable Url
def STUDENT_VIEW_TIMETABLE(request):
    student = Student.objects.get(admin = request.user.id)
    course = student.course_id
    session_year = student.session_year_id

    timetable_items = Timetable.objects.filter(course=course, session_year=session_year)

    context = {
        'timetable': timetable_items,
    }
    return render(request,'Student/view_timetable.html',context)