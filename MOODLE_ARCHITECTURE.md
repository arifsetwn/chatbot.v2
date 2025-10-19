# 🎓 Moodle Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CHATBOT SYSTEM                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │   Chat Page      │         │   Admin Panel    │            │
│  │  (1_Chat.py)     │         │  (2_Admin.py)    │            │
│  │                  │         │                  │            │
│  │  - User Chat     │         │  - Moodle Config │            │
│  │  - Get Assignments│        │  - Test Connection│           │
│  │  - Check Grades  │         │  - User Lookup   │            │
│  │  - View Progress │         │  - Course Browser│            │
│  └────────┬─────────┘         └────────┬─────────┘            │
│           │                            │                       │
│           └────────────┬───────────────┘                       │
│                        │                                       │
│              ┌─────────▼──────────┐                           │
│              │  Moodle Client     │                           │
│              │ (moodle_client.py) │                           │
│              │                    │                           │
│              │ - get_site_info()  │                           │
│              │ - get_user_by_*()  │                           │
│              │ - get_courses()    │                           │
│              │ - get_assignments()│                           │
│              │ - get_grades()     │                           │
│              │ - get_dashboard()  │                           │
│              └─────────┬──────────┘                           │
│                        │                                       │
└────────────────────────┼───────────────────────────────────────┘
                         │
                         │ REST API
                         │ (HTTPS)
                         ▼
         ┌───────────────────────────────┐
         │      MOODLE LMS              │
         │  (moodle.ums.ac.id)          │
         ├───────────────────────────────┤
         │                               │
         │  📚 Courses                   │
         │  📝 Assignments               │
         │  📊 Grades                    │
         │  👤 Users                     │
         │  📈 Progress Tracking         │
         │  💬 Forums (optional)         │
         │                               │
         └───────────────────────────────┘
```

## 🔄 Data Flow

### Flow 1: Check Assignments
```
User → Chat → "Apa tugas saya?"
  ↓
Chatbot Logic
  ↓
moodle_client.get_student_dashboard(username)
  ↓
Moodle API → GET /webservice/rest/server.php
  ↓
Return: {courses, assignments, grades}
  ↓
Format Response
  ↓
Display to User: "📝 Tugas yang akan datang: ..."
```

### Flow 2: Check Grades
```
User → Chat → "Berapa nilai saya di Algoritma?"
  ↓
Chatbot Logic
  ↓
1. moodle_client.get_enrolled_courses(user_id)
2. Find course matching "Algoritma"
3. moodle_client.get_user_grades(course_id, user_id)
  ↓
Moodle API → Multiple REST calls
  ↓
Return: Grade data
  ↓
Format Response
  ↓
Display to User: "📊 Nilai Anda: A- (85/100)"
```

### Flow 3: Admin Configuration
```
Admin → Admin Panel → Moodle Integration
  ↓
Enter: MOODLE_URL + MOODLE_TOKEN
  ↓
Click: "Test Connection"
  ↓
moodle_client.validate_connection()
  ↓
Moodle API → core_webservice_get_site_info
  ↓
Return: Site info or error
  ↓
Display: "✅ Connected" or "❌ Failed"
  ↓
Click: "Save Configuration"
  ↓
Write to .env file
```

## 📊 Feature Matrix

| Feature | Status | Complexity | Priority |
|---------|--------|------------|----------|
| User Authentication | ✅ Done | Low | High |
| Course List | ✅ Done | Low | High |
| Assignments | ✅ Done | Medium | High |
| Grades Tracking | ✅ Done | Medium | High |
| Student Dashboard | ✅ Done | High | High |
| Assignment Submission | 🔄 Pending | High | Medium |
| Quiz Integration | 🔄 Pending | High | Medium |
| Forum Integration | 🔄 Pending | Medium | Low |
| Calendar Sync | 🔄 Pending | Medium | Low |
| File Upload | 🔄 Pending | High | Low |

## 🔐 Security Layers

```
Layer 1: HTTPS Transport
   ↓
Layer 2: Token Authentication (MOODLE_TOKEN)
   ↓
Layer 3: IP Restriction (Moodle config)
   ↓
Layer 4: Function Permissions (External Service)
   ↓
Layer 5: User Context (per-user data access)
```

## 📈 Performance Considerations

### Caching Strategy
```python
# Cache user data for 5 minutes
@st.cache_data(ttl=300)
def get_cached_user(username):
    return moodle_client.get_user_by_username(username)

# Cache courses for 1 hour
@st.cache_data(ttl=3600)
def get_cached_courses(user_id):
    return moodle_client.get_enrolled_courses(user_id)
```

### Rate Limiting
- Max 60 requests/minute per user
- Batch requests when possible
- Use webhooks for real-time updates (future)

## 🧪 Testing Strategy

### Unit Tests
```python
def test_moodle_connection():
    client = MoodleClient()
    assert client.validate_connection() == True

def test_get_user():
    client = MoodleClient()
    user = client.get_user_by_username("test_user")
    assert user is not None
    assert 'id' in user
```

### Integration Tests
```python
def test_full_dashboard_flow():
    client = MoodleClient()
    dashboard = client.get_student_dashboard("test_user")
    assert 'user' in dashboard
    assert 'courses' in dashboard
    assert 'upcoming_assignments' in dashboard
```

## 🚀 Deployment Checklist

- [ ] Moodle Web Services enabled
- [ ] REST protocol enabled
- [ ] External Service created with functions
- [ ] Token generated and saved to .env
- [ ] Connection tested from Admin panel
- [ ] IP restriction configured (production)
- [ ] HTTPS enforced
- [ ] Error logging enabled
- [ ] Rate limiting configured
- [ ] Caching strategy implemented

## 📚 API Endpoints Used

| Moodle Function | Purpose | Required |
|----------------|---------|----------|
| `core_webservice_get_site_info` | Validate connection | ✅ Yes |
| `core_user_get_users` | Find users | ✅ Yes |
| `core_enrol_get_users_courses` | Get enrolled courses | ✅ Yes |
| `core_course_get_contents` | Course materials | ✅ Yes |
| `mod_assign_get_assignments` | List assignments | ✅ Yes |
| `gradereport_user_get_grade_items` | Get grades | ✅ Yes |
| `core_completion_get_course_completion_status` | Progress tracking | ⚪ Optional |
| `mod_forum_get_forum_discussions` | Forum access | ⚪ Optional |

---

**Architecture Version:** 1.0  
**Last Updated:** October 19, 2025  
**Status:** Production Ready ✅
