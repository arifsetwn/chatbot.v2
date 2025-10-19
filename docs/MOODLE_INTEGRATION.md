# Moodle LMS Integration Guide

## 📋 Overview

Integrasi chatbot dengan Moodle LMS memungkinkan:
- **Single Sign-On (SSO)**: Autentikasi mahasiswa via Moodle
- **Course Access**: Akses informasi course dan materi
- **Assignment Management**: Lihat dan submit tugas
- **Grade Tracking**: Monitor nilai dan progress
- **Dashboard**: Dashboard personalized untuk setiap mahasiswa

---

## 🚀 Quick Start

### 1. Setup Moodle Web Services

#### A. Enable Web Services (Moodle Admin)

```
Site Administration > Advanced Features
✅ Enable web services
```

#### B. Enable REST Protocol

```
Site Administration > Plugins > Web Services > Manage Protocols
✅ Enable: REST protocol
```

#### C. Create External Service

```
Site Administration > Plugins > Web Services > External Services
Click: "Add"

Service name: Chatbot Service
Short name: chatbot_service
Enabled: ✅

Add Functions:
- core_webservice_get_site_info
- core_user_get_users
- core_user_get_users_by_field
- core_enrol_get_users_courses
- core_course_get_courses
- core_course_get_contents
- mod_assign_get_assignments
- mod_assign_get_submissions
- mod_assign_save_submission
- gradereport_user_get_grade_items
- core_completion_get_course_completion_status
- mod_forum_get_forum_discussions (optional)
- mod_forum_add_discussion (optional)
```

#### D. Create Web Service Token

```
Site Administration > Plugins > Web Services > Manage Tokens
Click: "Add"

User: Select your admin/service user
Service: Chatbot Service
IP Restriction: (optional, set to your server IP)

Copy the generated token
```

### 2. Configure Chatbot

#### A. Add to .env file

```bash
# Moodle LMS Integration
MOODLE_URL=https://moodle.ums.ac.id
MOODLE_TOKEN=your_token_here
```

#### B. Install Dependencies

```bash
pip install requests>=2.31.0
```

#### C. Test Connection

```bash
python -c "from utils.moodle_client import MoodleClient; client = MoodleClient(); print('✅ Connected' if client.validate_connection() else '❌ Failed')"
```

---

## 💻 Usage Examples

### Example 1: Get User Information

```python
from utils.moodle_client import MoodleClient

client = MoodleClient()

# Get user by username
user = client.get_user_by_username("arif.setiawan")
print(f"User: {user['fullname']}")
print(f"Email: {user['email']}")
```

### Example 2: Get Student's Courses

```python
# Get enrolled courses
courses = client.get_enrolled_courses(user['id'])

for course in courses:
    print(f"- {course['fullname']}")
    print(f"  Progress: {course.get('progress', 0)}%")
```

### Example 3: Get Assignments

```python
# Get assignments for specific courses
course_ids = [1, 2, 3]
assignments = client.get_assignments(course_ids)

for course in assignments['courses']:
    print(f"\nCourse: {course['id']}")
    for assign in course['assignments']:
        print(f"  - {assign['name']}")
        print(f"    Due: {datetime.fromtimestamp(assign['duedate'])}")
```

### Example 4: Get Student Dashboard

```python
# Get comprehensive dashboard
dashboard = client.get_student_dashboard("arif.setiawan")

print(f"Student: {dashboard['user']['fullname']}")
print(f"Courses: {len(dashboard['courses'])}")
print(f"Upcoming Assignments: {len(dashboard['upcoming_assignments'])}")

# Show upcoming assignments
for assignment in dashboard['upcoming_assignments'][:5]:
    print(f"- {assignment['name']}")
    print(f"  Due: {assignment['duedate']}")
```

### Example 5: Get Grades

```python
# Get grades for a course
user_id = 123
course_id = 456

grades = client.get_user_grades(course_id, user_id)

for grade_info in grades.get('usergrades', []):
    for item in grade_info.get('gradeitems', []):
        print(f"{item['itemname']}: {item['gradeformatted']}")
```

---

## 🤖 Chatbot Integration Scenarios

### Scenario 1: Check Upcoming Assignments

**User:** "Apa tugas saya yang belum dikerjakan?"

**Chatbot:**
```python
# In chatbot logic
username = get_current_user()  # From session
dashboard = moodle_client.get_student_dashboard(username)

response = "📝 Tugas yang akan datang:\n\n"
for i, assign in enumerate(dashboard['upcoming_assignments'][:5], 1):
    response += f"{i}. **{assign['name']}**\n"
    response += f"   Deadline: {assign['duedate']}\n"
    response += f"   Course: {assign['course']}\n\n"
```

### Scenario 2: Check Grades

**User:** "Berapa nilai saya di mata kuliah Algoritma?"

**Chatbot:**
```python
# Find course by name
courses = moodle_client.get_enrolled_courses(user_id)
algo_course = next((c for c in courses if 'algoritma' in c['fullname'].lower()), None)

if algo_course:
    grades = moodle_client.get_user_grades(algo_course['id'], user_id)
    # Format and show grades
```

### Scenario 3: Course Progress

**User:** "Bagaimana progress belajar saya?"

**Chatbot:**
```python
dashboard = moodle_client.get_student_dashboard(username)

response = "📊 Progress Belajar:\n\n"
for course in dashboard['courses']:
    progress = course.get('progress', 0)
    response += f"• {course['fullname']}: {progress}%\n"
```

---

## 🔐 Security Best Practices

### 1. Token Management

```python
# ❌ DON'T: Hardcode tokens
client = MoodleClient("https://moodle.ums.ac.id", "abc123token")

# ✅ DO: Use environment variables
client = MoodleClient()  # Reads from .env
```

### 2. IP Restriction

In Moodle token configuration:
- Set IP restriction to your server's IP
- Use HTTPS only
- Rotate tokens periodically

### 3. User Permissions

- Create dedicated service user in Moodle
- Grant minimum required permissions
- Don't use admin account for web services

### 4. Error Handling

```python
try:
    user = client.get_user_by_username(username)
except Exception as e:
    logger.error(f"Moodle API error: {e}")
    # Show user-friendly error message
```

---

## 🧪 Testing

### Test Connection

```bash
# Via Admin Panel
Admin > Moodle Integration > Test Connection

# Via CLI
python utils/moodle_client.py
```

### Test API Functions

```python
from utils.moodle_client import MoodleClient

client = MoodleClient()

# Test 1: Site info
info = client.get_site_info()
assert 'sitename' in info

# Test 2: User lookup
user = client.get_user_by_username("test_user")
assert user is not None

# Test 3: Courses
courses = client.get_enrolled_courses(user['id'])
assert isinstance(courses, list)
```

---

## 📊 API Functions Reference

| Function | Description | Parameters |
|----------|-------------|------------|
| `get_site_info()` | Get site information | None |
| `get_user_by_username(username)` | Find user by username | username: str |
| `get_enrolled_courses(user_id)` | Get user's courses | user_id: int |
| `get_course_contents(course_id)` | Get course materials | course_id: int |
| `get_assignments(course_ids)` | Get assignments | course_ids: List[int] |
| `get_user_grades(course_id, user_id)` | Get grades | course_id: int, user_id: int |
| `get_student_dashboard(username)` | Get full dashboard | username: str |

---

## 🚧 Troubleshooting

### Error: "Invalid token"

**Solution:**
- Check token in .env matches Moodle
- Verify token is not expired
- Check service is enabled

### Error: "Function not available"

**Solution:**
- Add function to External Service in Moodle
- Check user has permission for the function

### Error: "Connection timeout"

**Solution:**
- Check Moodle URL is correct
- Verify network connectivity
- Check firewall settings

### Error: "User not found"

**Solution:**
- Verify username spelling
- Check user exists in Moodle
- Try searching by email or ID instead

---

## 🔄 Future Enhancements

- [ ] Quiz integration (attempt quizzes)
- [ ] Forum integration (post questions)
- [ ] Calendar integration (show events)
- [ ] File upload (submit assignments)
- [ ] Messaging (send messages to instructors)
- [ ] Badge system (show achievements)
- [ ] Certificate generation

---

## 📚 Resources

- [Moodle Web Services Documentation](https://docs.moodle.org/dev/Web_services)
- [Moodle Web Service API Functions](https://docs.moodle.org/dev/Web_service_API_functions)
- [REST Protocol Guide](https://docs.moodle.org/dev/Creating_a_web_service_client#REST)

---

## 📝 Notes

- Requires Moodle 3.9+ for best compatibility
- Some functions require admin privileges
- API responses cached for performance
- Rate limiting recommended for production

---

**Created:** October 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅
