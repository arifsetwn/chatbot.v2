"""
Analytics tracking for chatbot usage
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading


class Analytics:
    """Track and analyze chatbot usage metrics"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.analytics_file = self.log_dir / "analytics.json"
        self.lock = threading.Lock()
        self._ensure_analytics_file()
    
    def _ensure_analytics_file(self):
        """Ensure analytics file exists with default structure"""
        if not self.analytics_file.exists():
            default_data = {
                "total_chats": 0,
                "total_users": 0,
                "chats_history": [],
                "response_times": [],
                "daily_stats": {},
                "start_time": datetime.now().isoformat()
            }
            with open(self.analytics_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def log_chat(self, user_id: str, response_time: float, success: bool = True):
        """
        Log a chat interaction
        
        Args:
            user_id: Identifier for the user (can be session_id or username)
            response_time: Response time in seconds
            success: Whether the response was successful
        """
        with self.lock:
            try:
                # Read current data
                with open(self.analytics_file, 'r') as f:
                    data = json.load(f)
                
                # Get today's date
                today = datetime.now().strftime("%Y-%m-%d")
                
                # Update total chats
                data["total_chats"] += 1
                
                # Track unique users
                if user_id not in data.get("users_seen", []):
                    if "users_seen" not in data:
                        data["users_seen"] = []
                    data["users_seen"].append(user_id)
                    data["total_users"] = len(data["users_seen"])
                
                # Log chat history
                data["chats_history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "user_id": user_id,
                    "response_time": response_time,
                    "success": success
                })
                
                # Keep only last 1000 chats in history
                if len(data["chats_history"]) > 1000:
                    data["chats_history"] = data["chats_history"][-1000:]
                
                # Track response times (keep last 100)
                data["response_times"].append(response_time)
                if len(data["response_times"]) > 100:
                    data["response_times"] = data["response_times"][-100:]
                
                # Update daily stats
                if "daily_stats" not in data:
                    data["daily_stats"] = {}
                
                if today not in data["daily_stats"]:
                    data["daily_stats"][today] = {
                        "chats": 0,
                        "users": [],
                        "avg_response_time": 0,
                        "total_response_time": 0
                    }
                
                daily = data["daily_stats"][today]
                daily["chats"] += 1
                daily["total_response_time"] += response_time
                daily["avg_response_time"] = daily["total_response_time"] / daily["chats"]
                
                if user_id not in daily["users"]:
                    daily["users"].append(user_id)
                
                # Save updated data
                with open(self.analytics_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
            except Exception as e:
                print(f"Error logging analytics: {e}")
    
    def get_stats(self) -> Dict:
        """Get current analytics stats"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Get today's stats
            today_stats = data.get("daily_stats", {}).get(today, {
                "chats": 0,
                "users": [],
                "avg_response_time": 0
            })
            
            # Calculate average response time
            response_times = data.get("response_times", [])
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Calculate uptime
            start_time = datetime.fromisoformat(data.get("start_time", datetime.now().isoformat()))
            uptime_hours = (datetime.now() - start_time).total_seconds() / 3600
            
            return {
                "total_chats": data.get("total_chats", 0),
                "total_users": data.get("total_users", 0),
                "chats_today": today_stats.get("chats", 0),
                "active_users_today": len(today_stats.get("users", [])),
                "avg_response_time": avg_response_time,
                "uptime_hours": uptime_hours,
                "recent_chats": data.get("chats_history", [])[-10:],
                "daily_stats": data.get("daily_stats", {})
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                "total_chats": 0,
                "total_users": 0,
                "chats_today": 0,
                "active_users_today": 0,
                "avg_response_time": 0,
                "uptime_hours": 0,
                "recent_chats": [],
                "daily_stats": {}
            }
    
    def get_daily_stats(self, days: int = 7) -> Dict[str, Dict]:
        """Get daily stats for the last N days"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
            
            daily_stats = data.get("daily_stats", {})
            
            # Get last N days
            result = {}
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                if date in daily_stats:
                    result[date] = daily_stats[date]
                else:
                    result[date] = {
                        "chats": 0,
                        "users": [],
                        "avg_response_time": 0
                    }
            
            return result
        except Exception as e:
            print(f"Error getting daily stats: {e}")
            return {}
    
    def reset_stats(self):
        """Reset all analytics data"""
        with self.lock:
            default_data = {
                "total_chats": 0,
                "total_users": 0,
                "users_seen": [],
                "chats_history": [],
                "response_times": [],
                "daily_stats": {},
                "start_time": datetime.now().isoformat()
            }
            with open(self.analytics_file, 'w') as f:
                json.dump(default_data, f, indent=2)


# Global analytics instance
_analytics_instance = None

def get_analytics() -> Analytics:
    """Get or create global analytics instance"""
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = Analytics()
    return _analytics_instance
