# 🎓 Moodle Integration - Quick Reference

## ✅ What's Implemented

Integrasi chatbot dengan Moodle LMS untuk:
- ✅ **Authentication**: User lookup dan validation
- ✅ **Courses**: Daftar course yang diambil mahasiswa
- ✅ **Assignments**: List dan detail tugas
- ✅ **Grades**: Tracking nilai dan progress
- ✅ **Dashboard**: View dashboard mahasiswa lengkap
- ✅ **Admin Panel**: UI untuk konfigurasi dan testing

## 🚀 Quick Setup

### 1. Enable Moodle Web Services

```
Moodle Admin > Site Administration > Advanced Features
✅ Enable web services

Moodle Admin > Plugins > Web Services > Manage Protocols
✅ Enable REST protocol
```

### 2. Create Service & Token

```
Create External Service: "Chatbot Service"
Add required functions (see MOODLE_INTEGRATION.md)
Generate token
```

### 3. Configure Chatbot

Edit `.env`:
```bash
MOODLE_URL=https://moodle.ums.ac.id
MOODLE_TOKEN=your_token_here
```

### 4. Test Connection

```bash
# Via Admin Panel
Go to: Admin > Moodle Integration > Test Connection

# Via CLI
python -c "from utils.moodle_client import MoodleClient; c = MoodleClient(); print('✅' if c.validate_connection() else '❌')"
```

## 📁 Files Created

| File | Purpose |
|------|---------|
| `utils/moodle_client.py` | Moodle API client library |
| `MOODLE_INTEGRATION.md` | Complete integration guide |
| `pages/2_Admin.py` | Added "Moodle Integration" menu |

## 💡 Usage in Chatbot

### Example: Get Student Assignments

```python
from utils.moodle_client import get_moodle_client

# In chatbot logic
client = get_moodle_client()
dashboard = client.get_student_dashboard(username)

# Show upcoming assignments
for assign in dashboard['upcoming_assignments']:
    print(f"- {assign['name']} (Due: {assign['duedate']})")
```

### Example: Check Grades

```python
user = client.get_user_by_username("arif.setiawan")
courses = client.get_enrolled_courses(user['id'])

for course in courses:
    grades = client.get_user_grades(course['id'], user['id'])
    # Display grades
```

## 🔐 Security Notes

- ✅ Token stored in `.env` (not in code)
- ✅ HTTPS recommended for production
- ✅ IP restriction in Moodle token config
- ✅ Minimum permissions principle

## 📚 Full Documentation

See **[MOODLE_INTEGRATION.md](./MOODLE_INTEGRATION.md)** for:
- Complete setup instructions
- API reference
- Code examples
- Troubleshooting guide
- Security best practices

## 🧪 Testing Checklist

- [ ] Test connection from Admin panel
- [ ] Search user by username
- [ ] Load courses list
- [ ] Get assignments for a course
- [ ] View student dashboard
- [ ] Check error handling

## 🚧 Future Enhancements

- [ ] Quiz integration
- [ ] Assignment submission from chatbot
- [ ] Forum posting
- [ ] Calendar sync
- [ ] File upload
- [ ] Messaging

---

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** October 19, 2025
