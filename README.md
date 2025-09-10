# CampusConnect-SMS

CampusConnect-SMS is a comprehensive School Management System built with Django. It provides modules for user authentication, student and staff management, attendance tracking, notifications, feedback, leave management, timetable scheduling, and auditorium booking.

## Features

- **Custom User Model**: Supports HOD, Staff, and Student roles.
- **Authentication**: Email-based login via a custom backend ([app/EmailBackEnd.py](app/EmailBackEnd.py)).
- **Student & Staff Management**: CRUD operations for students, staff, courses, and sessions ([app/models.py](app/models.py)).
- **Attendance & Reports**: Track attendance and generate reports.
- **Notifications**: Send notifications to staff and students.
- **Feedback & Leave**: Manage feedback and leave requests for both staff and students.
- **Timetable**: Schedule and manage lectures ([app/models.py](app/models.py)).
- **Auditorium Booking**: Book and manage auditorium slots.
- **Admin Panel**: Django admin for superuser management.
- **Responsive UI**: Templates for login, dashboard, and profile ([templates/](templates/)).

## Project Structure

```
Campus_Connect/
    app/
        models.py
        views.py
        EmailBackEnd.py
        ...
    Campus_Connect/
        settings.py
        urls.py
        ...
    templates/
        base.html
        login.html
        profile.html
        ...
    static/
        assets/
    media/
        profile_pic/
    manage.py
    db.sqlite3
```

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd CampusConnect-SMS--main/Campus_Connect
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   # If requirements.txt is missing, install manually:
   pip install django django-active-link
   ```

3. **Apply migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**
   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```sh
   python manage.py runserver
   ```

6. **Access the app**
   - Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Configuration

- **Custom User Model**: Set in [`Campus_Connect/settings.py`](Campus_Connect/Campus_Connect/settings.py) as `AUTH_USER_MODEL = 'app.CustomUser'`.
- **Static & Media Files**: Configured for profile pictures and assets.
- **Authentication Backend**: Uses [`app/EmailBackEnd.py`](app/EmailBackEnd.py) for email login.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

---

**Pro Tip:** For production, set `DEBUG = False` and configure allowed hosts and secret keys securely.
