# Teacher Management System - Admin Feature

## Overview
This feature allows administrators to create teacher accounts with auto-generated credentials that are sent via email.

## Features
- ✅ Admin-only access to create teachers
- ✅ Auto-generated unique teacher IDs (TCH001, TCH002, etc.)
- ✅ Secure random password generation
- ✅ Email notification with login credentials
- ✅ Professional HTML email template
- ✅ Complete CRUD operations for teachers

## Setup Instructions

### 1. Email Configuration

Create a `.env` file in the `Backend` directory with the following variables:

```env
# SMTP Configuration for Gmail (or your email provider)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
FROM_EMAIL=noreply@eventsync.com
```

#### For Gmail:
1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated 16-character password
   - Use this as `SMTP_PASSWORD`

#### For Other Providers:
Update `SMTP_HOST` and `SMTP_PORT` accordingly:
- **Outlook/Hotmail**: `smtp.office365.com`, port `587`
- **Yahoo**: `smtp.mail.yahoo.com`, port `587`
- **Custom SMTP**: Use your provider's settings

### 2. Install Dependencies

The email feature uses Python's built-in `smtplib`, so no additional packages are needed.

### 3. Create an Admin User

First, you need an admin user. You can create one manually in MongoDB:

```javascript
// In MongoDB shell or Compass
use eventsync_db

db.users.insertOne({
  name: "Admin User",
  email: "admin@eventsync.com",
  password: "$2b$12$..." , // Use bcrypt to hash "adminpassword" or any password
  role: "admin",
  is_active: true,
  created_at: new Date()
})
```

Or register via API and manually update the role to "admin":

```bash
# Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@eventsync.com",
    "password": "adminpassword"
  }'

# Then update role in MongoDB
db.users.updateOne(
  {email: "admin@eventsync.com"},
  {$set: {role: "admin"}}
)
```

## API Endpoints

### 1. Admin Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "admin@eventsync.com",
  "password": "adminpassword"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### 2. Create Teacher (Admin Only)
```bash
POST /admin/teachers/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Dr. John Smith",
  "email": "john.smith@university.edu",
  "department": "Computer Science",
  "subject": "Data Structures",
  "phone": "+1234567890"
}

Response:
{
  "id": "674a2c8f9e7b3d2a1c4e5f6a",
  "teacher_id": "TCH001",
  "name": "Dr. John Smith",
  "email": "john.smith@university.edu",
  "department": "Computer Science",
  "subject": "Data Structures",
  "phone": "+1234567890",
  "role": "teacher",
  "is_active": true,
  "created_at": "2025-11-30T10:30:00",
  "created_by": "674a2c8f9e7b3d2a1c4e5f6b"
}
```

### 3. Get All Teachers (Admin Only)
```bash
GET /admin/teachers/
Authorization: Bearer <admin_token>

Response:
[
  {
    "id": "...",
    "teacher_id": "TCH001",
    "name": "Dr. John Smith",
    ...
  }
]
```

### 4. Get Teacher by ID (Admin Only)
```bash
GET /admin/teachers/{teacher_id}
Authorization: Bearer <admin_token>
```

### 5. Delete Teacher (Admin Only)
```bash
DELETE /admin/teachers/{teacher_id}
Authorization: Bearer <admin_token>
```

## Email Template

Teachers will receive a professional HTML email with:
- Welcome message
- Teacher ID and password clearly displayed
- Login URL link
- Security warning to change password
- Professional styling

### Sample Email Content:
```
Subject: Welcome to EventSync - Your Login Credentials

Hello Dr. John Smith,

Your teacher account has been successfully created.

Login Credentials:
Teacher ID: TCH001
Password: Xy9#mK2$pL5q

⚠️ Please change your password after your first login.

[Login Now Button]
```

## Teacher Login

After receiving credentials, teachers can login using:

```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john.smith@university.edu",
  "password": "Xy9#mK2$pL5q"
}
```

## Security Features

1. **Password Generation**: 12-character passwords with:
   - Uppercase letters
   - Lowercase letters
   - Numbers
   - Special characters (!@#$%^&*)

2. **Password Hashing**: All passwords are hashed using bcrypt before storage

3. **Admin Authorization**: Only users with role="admin" can create teachers

4. **Unique Teacher IDs**: Sequential IDs (TCH001, TCH002...) to prevent duplicates

5. **Email Verification**: Checks for existing emails before creation

## Testing

### Test Email Configuration
You can test your email setup by modifying `utils/email_util.py` and running:

```python
from utils.email_util import send_test_email

# Test email
send_test_email("your-test-email@example.com")
```

### Complete Flow Test

1. Start the server:
```bash
cd Backend
uvicorn main:app --reload
```

2. Login as admin and get token

3. Create a teacher:
```bash
curl -X POST http://localhost:8000/admin/teachers/ \
  -H "Authorization: Bearer <your-admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Teacher",
    "email": "test@example.com",
    "department": "Mathematics"
  }'
```

4. Check your email inbox for credentials

5. Login as the teacher using received credentials

## Troubleshooting

### Email Not Sending

1. **Check SMTP credentials**: Verify `.env` file settings
2. **Gmail App Password**: Make sure you're using an App Password, not your regular password
3. **Firewall**: Ensure port 587 is not blocked
4. **Check logs**: Look for error messages in console output

### "Access forbidden" Error
- Make sure your user has `role: "admin"` in the database
- Verify your JWT token is valid and not expired

### "Email already exists" Error
- Check both `users` and `teachers` collections in MongoDB
- The email must be unique across both collections

## Database Collections

### teachers Collection Structure
```javascript
{
  _id: ObjectId("..."),
  name: "Dr. John Smith",
  email: "john.smith@university.edu",
  department: "Computer Science",
  subject: "Data Structures",
  phone: "+1234567890",
  teacher_id: "TCH001",
  password: "$2b$12$...",  // bcrypt hashed
  role: "teacher",
  is_active: true,
  created_at: ISODate("..."),
  created_by: "674a..."  // Admin's user ID
}
```

## Future Enhancements

- [ ] Password reset functionality
- [ ] Email templates for password reset
- [ ] Teacher profile update endpoint
- [ ] Bulk teacher import from CSV
- [ ] Email delivery status tracking
- [ ] Teacher activity logs
- [ ] Account deactivation (instead of deletion)
- [ ] Teacher dashboard statistics

## Support

For issues or questions, please contact the development team or check the logs for detailed error messages.
