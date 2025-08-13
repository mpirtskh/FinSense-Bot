from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

class UsageTracker:
    """Simple usage tracker for OpenAI API calls."""
    
    def __init__(self, log_file: str = "usage_log.json"):
        self.log_file = Path(log_file)
        self.usage_data = self._load_usage()
    
    def _load_usage(self) -> Dict:
        """Load existing usage data from file."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {
            "total_calls": 0,
            "total_tokens": 0,
            "daily_usage": {},
            "model_usage": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def _save_usage(self):
        """Save usage data to file."""
        self.usage_data["last_updated"] = datetime.now().isoformat()
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.usage_data, f, indent=2, ensure_ascii=False)
    
    def log_call(self, model: str, input_tokens: int, output_tokens: int, cost: Optional[float] = None):
        """Log an API call with token usage."""
        today = datetime.now().strftime("%Y-%m-%d")
        total_tokens = input_tokens + output_tokens
        
        # Update total counts
        self.usage_data["total_calls"] += 1
        self.usage_data["total_tokens"] += total_tokens
        
        # Update daily usage
        if today not in self.usage_data["daily_usage"]:
            self.usage_data["daily_usage"][today] = {
                "calls": 0,
                "tokens": 0,
                "cost": 0.0
            }
        
        self.usage_data["daily_usage"][today]["calls"] += 1
        self.usage_data["daily_usage"][today]["tokens"] += total_tokens
        if cost:
            self.usage_data["daily_usage"][today]["cost"] += cost
        
        # Update model usage
        if model not in self.usage_data["model_usage"]:
            self.usage_data["model_usage"][model] = {
                "calls": 0,
                "tokens": 0
            }
        
        self.usage_data["model_usage"][model]["calls"] += 1
        self.usage_data["model_usage"][model]["tokens"] += total_tokens
        
        self._save_usage()
    
    def get_summary(self) -> str:
        """Get a formatted usage summary."""
        summary = f"""
📊 **Usage Summary**
==================
Total API Calls: {self.usage_data['total_calls']:,}
Total Tokens: {self.usage_data['total_tokens']:,}

📅 **Today's Usage** ({datetime.now().strftime('%Y-%m-%d')})
"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        if today in self.usage_data["daily_usage"]:
            today_data = self.usage_data["daily_usage"][today]
            summary += f"Calls: {today_data['calls']}\n"
            summary += f"Tokens: {today_data['tokens']:,}\n"
            if today_data['cost'] > 0:
                summary += f"Cost: ${today_data['cost']:.4f}\n"
        else:
            summary += "No usage today\n"
        
        summary += "\n🤖 **Model Usage**\n"
        for model, data in self.usage_data["model_usage"].items():
            summary += f"{model}: {data['calls']} calls, {data['tokens']:,} tokens\n"
        
        return summary
    
    def get_daily_stats(self, days: int = 7) -> str:
        """Get usage stats for the last N days."""
        dates = sorted(self.usage_data["daily_usage"].keys(), reverse=True)[:days]
        
        stats = f"📈 **Last {days} Days Usage**\n"
        stats += "=" * 30 + "\n"
        
        for date in dates:
            data = self.usage_data["daily_usage"][date]
            stats += f"{date}: {data['calls']} calls, {data['tokens']:,} tokens"
            if data['cost'] > 0:
                stats += f", ${data['cost']:.4f}"
            stats += "\n"
        
        return stats

# Global usage tracker instance
usage_tracker = UsageTracker() 