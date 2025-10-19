"""
Moodle Web Services API Client
Handles integration with Moodle LMS for:
- User authentication
- Course management
- Assignment submission
- Grade tracking
"""

import os
import requests
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from datetime import datetime


class MoodleClient:
    """
    Client for interacting with Moodle Web Services API.
    
    Prerequisites:
    - Moodle Web Services must be enabled
    - REST protocol must be enabled
    - External service with required functions must be created
    - API token must be generated
    """
    
    def __init__(self, moodle_url: str = None, token: str = None):
        """
        Initialize Moodle client.
        
        Args:
            moodle_url: Base URL of Moodle instance (e.g., https://moodle.ums.ac.id)
            token: Web service token from Moodle
        """
        self.moodle_url = moodle_url or os.getenv("MOODLE_URL", "")
        self.token = token or os.getenv("MOODLE_TOKEN", "")
        self.rest_endpoint = f"{self.moodle_url}/webservice/rest/server.php"
        
        if not self.moodle_url or not self.token:
            raise ValueError("Moodle URL and token must be provided")
    
    def _call_api(self, function: str, params: Dict[str, Any] = None) -> Dict:
        """
        Make a REST API call to Moodle.
        
        Args:
            function: Moodle web service function name
            params: Parameters for the function
            
        Returns:
            API response as dictionary
        """
        if params is None:
            params = {}
        
        data = {
            'wstoken': self.token,
            'wsfunction': function,
            'moodlewsrestformat': 'json',
            **params
        }
        
        try:
            response = requests.post(self.rest_endpoint, data=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            # Check for Moodle errors
            if isinstance(result, dict) and 'exception' in result:
                raise Exception(f"Moodle API Error: {result.get('message', 'Unknown error')}")
            
            return result
        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    # ============================================
    # SITE & USER INFORMATION
    # ============================================
    
    def get_site_info(self) -> Dict:
        """
        Get basic site information and validate token.
        
        Returns:
            Dict with site name, version, user info, etc.
        """
        return self._call_api('core_webservice_get_site_info')
    
    def get_user_by_field(self, field: str, values: List[str]) -> List[Dict]:
        """
        Get users by field (username, email, id, etc.).
        
        Args:
            field: Field to search ('username', 'email', 'id', 'idnumber')
            values: List of values to search for
            
        Returns:
            List of user dictionaries
        """
        params = {
            'field': field,
        }
        
        # Add multiple values
        for i, value in enumerate(values):
            params[f'values[{i}]'] = value
        
        return self._call_api('core_user_get_users', params)
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Get user information by username.
        
        Args:
            username: Moodle username
            
        Returns:
            User dictionary or None if not found
        """
        users = self.get_user_by_field('username', [username])
        return users[0] if users else None
    
    # ============================================
    # COURSE MANAGEMENT
    # ============================================
    
    def get_enrolled_courses(self, user_id: int) -> List[Dict]:
        """
        Get list of courses a user is enrolled in.
        
        Args:
            user_id: Moodle user ID
            
        Returns:
            List of course dictionaries
        """
        params = {'userid': user_id}
        return self._call_api('core_enrol_get_users_courses', params)
    
    def get_course_contents(self, course_id: int) -> List[Dict]:
        """
        Get contents of a course (sections, modules, resources).
        
        Args:
            course_id: Moodle course ID
            
        Returns:
            List of section dictionaries with modules
        """
        params = {'courseid': course_id}
        return self._call_api('core_course_get_contents', params)
    
    def get_all_courses(self) -> List[Dict]:
        """
        Get all courses in the Moodle instance.
        (Requires admin privileges)
        
        Returns:
            List of all courses
        """
        return self._call_api('core_course_get_courses')
    
    # ============================================
    # ASSIGNMENT MANAGEMENT
    # ============================================
    
    def get_assignments(self, course_ids: List[int] = None) -> Dict:
        """
        Get assignments for given courses.
        
        Args:
            course_ids: List of course IDs (if None, get all)
            
        Returns:
            Dict with 'courses' containing assignments
        """
        params = {}
        
        if course_ids:
            for i, course_id in enumerate(course_ids):
                params[f'courseids[{i}]'] = course_id
        
        return self._call_api('mod_assign_get_assignments', params)
    
    def get_assignment_submissions(self, assign_id: int) -> List[Dict]:
        """
        Get submissions for an assignment.
        
        Args:
            assign_id: Assignment ID
            
        Returns:
            List of submission dictionaries
        """
        params = {'assignmentids[0]': assign_id}
        result = self._call_api('mod_assign_get_submissions', params)
        return result.get('assignments', [{}])[0].get('submissions', [])
    
    def submit_assignment(self, assign_id: int, plugin_data: Dict) -> Dict:
        """
        Submit an assignment.
        
        Args:
            assign_id: Assignment ID
            plugin_data: Submission data (text, files, etc.)
            
        Returns:
            Submission result
        """
        params = {
            'assignmentid': assign_id,
        }
        
        # Add plugin data
        for i, (key, value) in enumerate(plugin_data.items()):
            params[f'plugindata[{i}][name]'] = key
            params[f'plugindata[{i}][value]'] = value
        
        return self._call_api('mod_assign_save_submission', params)
    
    # ============================================
    # GRADE & PROGRESS TRACKING
    # ============================================
    
    def get_user_grades(self, course_id: int, user_id: int) -> List[Dict]:
        """
        Get grades for a user in a course.
        
        Args:
            course_id: Course ID
            user_id: User ID
            
        Returns:
            List of grade items
        """
        params = {
            'courseid': course_id,
            'userid': user_id
        }
        return self._call_api('gradereport_user_get_grade_items', params)
    
    def get_course_completion(self, course_id: int, user_id: int) -> Dict:
        """
        Get course completion status for a user.
        
        Args:
            course_id: Course ID
            user_id: User ID
            
        Returns:
            Completion status dictionary
        """
        params = {
            'courseid': course_id,
            'userid': user_id
        }
        return self._call_api('core_completion_get_course_completion_status', params)
    
    # ============================================
    # FORUM & MESSAGING
    # ============================================
    
    def get_forum_discussions(self, forum_id: int) -> List[Dict]:
        """
        Get discussions from a forum.
        
        Args:
            forum_id: Forum ID
            
        Returns:
            List of discussion dictionaries
        """
        params = {'forumid': forum_id}
        return self._call_api('mod_forum_get_forum_discussions', params)
    
    def post_forum_discussion(self, forum_id: int, subject: str, message: str) -> Dict:
        """
        Post a new discussion to a forum.
        
        Args:
            forum_id: Forum ID
            subject: Discussion subject
            message: Discussion message
            
        Returns:
            Discussion creation result
        """
        params = {
            'forumid': forum_id,
            'subject': subject,
            'message': message,
        }
        return self._call_api('mod_forum_add_discussion', params)
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    
    def validate_connection(self) -> bool:
        """
        Test if Moodle connection is valid.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            info = self.get_site_info()
            return 'sitename' in info
        except Exception:
            return False
    
    def get_student_dashboard(self, username: str) -> Dict:
        """
        Get comprehensive dashboard data for a student.
        
        Args:
            username: Student's Moodle username
            
        Returns:
            Dict with courses, assignments, grades, etc.
        """
        # Get user
        user = self.get_user_by_username(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        user_id = user['id']
        
        # Get enrolled courses
        courses = self.get_enrolled_courses(user_id)
        
        # Get assignments
        course_ids = [c['id'] for c in courses]
        assignments_data = self.get_assignments(course_ids) if course_ids else {'courses': []}
        
        # Organize data
        dashboard = {
            'user': {
                'id': user_id,
                'username': user['username'],
                'fullname': user['fullname'],
                'email': user['email']
            },
            'courses': [],
            'upcoming_assignments': [],
            'recent_grades': []
        }
        
        # Process courses
        for course in courses:
            course_info = {
                'id': course['id'],
                'fullname': course['fullname'],
                'shortname': course['shortname'],
                'progress': course.get('progress', 0),
            }
            
            # Get grades for this course
            try:
                grades = self.get_user_grades(course['id'], user_id)
                course_info['grades'] = grades.get('usergrades', [])
            except Exception:
                course_info['grades'] = []
            
            dashboard['courses'].append(course_info)
        
        # Process assignments
        for course_data in assignments_data.get('courses', []):
            for assignment in course_data.get('assignments', []):
                # Check if assignment is due soon
                due_date = assignment.get('duedate', 0)
                if due_date > datetime.now().timestamp():
                    dashboard['upcoming_assignments'].append({
                        'id': assignment['id'],
                        'name': assignment['name'],
                        'course': assignment.get('courseid'),
                        'duedate': datetime.fromtimestamp(due_date).isoformat(),
                        'intro': assignment.get('intro', '')[:200]
                    })
        
        # Sort assignments by due date
        dashboard['upcoming_assignments'].sort(key=lambda x: x['duedate'])
        
        return dashboard


def get_moodle_client() -> MoodleClient:
    """
    Get a singleton Moodle client instance.
    
    Returns:
        MoodleClient instance
    """
    return MoodleClient()


# ============================================
# USAGE EXAMPLE
# ============================================

if __name__ == "__main__":
    """
    Example usage of Moodle client.
    
    Setup .env with:
    MOODLE_URL=https://moodle.ums.ac.id
    MOODLE_TOKEN=your_token_here
    """
    
    try:
        client = MoodleClient()
        
        # Test connection
        if client.validate_connection():
            print("✅ Connected to Moodle successfully!")
            
            # Get site info
            info = client.get_site_info()
            print(f"Site: {info['sitename']}")
            print(f"Version: {info['version']}")
            print(f"User: {info['fullname']}")
            
        else:
            print("❌ Failed to connect to Moodle")
            
    except Exception as e:
        print(f"Error: {e}")
