import os
import sys
from datetime import datetime, timedelta
import shutil

# Base directory for all release notes
BASE_DIR = "Recall"
TEMPLATES_DIR = os.path.join(BASE_DIR, "Templates")

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def get_week_dates(target_date=None):
    """Get the start and end dates for the week containing the target date"""
    if target_date is None:
        target_date = datetime.now()
    
    # Find Monday of the current week
    start_of_week = target_date - timedelta(days=target_date.weekday())
    # Find Sunday of the current week
    end_of_week = start_of_week + timedelta(days=6)
    
    return start_of_week, end_of_week

def get_quarter(date):
    """Get the quarter (Q1-Q4) for a given date"""
    return f"Q{(date.month - 1) // 3 + 1}"

def setup_templates():
    """Create template files if they don't exist"""
    ensure_directory_exists(TEMPLATES_DIR)
    
    daily_template_path = os.path.join(TEMPLATES_DIR, "daily-template.md")
    weekly_template_path = os.path.join(TEMPLATES_DIR, "weekly-template.md")
    
    # Only create templates if they don't exist
    if not os.path.exists(daily_template_path):
        with open(daily_template_path, "w", encoding="utf-8") as f:
            f.write("""# Daily Notes: [DATE]

## 🏗️ Projects Worked On

- 

## 🛠️ Tasks Completed

- 

## 🤔 Decisions Made

- 

## 💡 Ideas & Insights

- 

## 🧠 Learnings

- 

## 🚧 Blockers & Challenges

- 

## 📌 Follow-ups Needed

- 

## 📝 Notes for Weekly Summary

- 
""")
        print(f"Created daily template: {daily_template_path}")
    
    if not os.path.exists(weekly_template_path):
        with open(weekly_template_path, "w", encoding="utf-8") as f:
            f.write("""# Weekly Release Notes: Week of [START_DATE] to [END_DATE]

## 🌟 Key Accomplishments

- 

## 📊 Project Progress

### [Project Name]
- Status: [On Track/At Risk/Blocked]
- Progress:
  - 
- Next Steps:
  - 

### [Project Name]
- Status:
- Progress:
- Next Steps:

## 💎 Key Learnings & Insights

- 

## 🔄 Process Improvements

- 

## 🚧 Challenges & Blockers

- 

## 👥 Collaborations & Meetings

- 

## 📅 Looking Ahead to Next Week

- 

## 🌱 Personal Growth & Development

- 
""")
        print(f"Created weekly template: {weekly_template_path}")

def setup_week(target_date=None):
    """Set up folder structure and files for a specific week"""
    if target_date is None:
        target_date = datetime.now()
    
    start_date, end_date = get_week_dates(target_date)
    
    # Create directory structure
    year_dir = os.path.join(BASE_DIR, str(start_date.year))
    quarter_dir = os.path.join(year_dir, get_quarter(start_date))
    
    # Create week directory with format Week##-MonDD-MonDD
    week_num = start_date.isocalendar()[1]  # ISO week number
    week_dir_name = f"Week{week_num:02d}-{start_date.strftime('%b%d')}-{end_date.strftime('%b%d')}"
    week_dir = os.path.join(quarter_dir, week_dir_name)
    daily_dir = os.path.join(week_dir, "daily")
    
    ensure_directory_exists(year_dir)
    ensure_directory_exists(quarter_dir)
    ensure_directory_exists(week_dir)
    ensure_directory_exists(daily_dir)
    
    # Create daily note files for each day of the week
    try:
        with open(os.path.join(TEMPLATES_DIR, "daily-template.md"), "r", encoding="utf-8") as template_file:
            daily_template = template_file.read()
        
        # Create weekly summary template
        with open(os.path.join(TEMPLATES_DIR, "weekly-template.md"), "r", encoding="utf-8") as template_file:
            weekly_template = template_file.read()
        
        # Replace placeholders in weekly template
        weekly_template = weekly_template.replace(
            "[START_DATE]", start_date.strftime("%B %d, %Y")
        ).replace(
            "[END_DATE]", end_date.strftime("%B %d, %Y")
        )
        
        # Write weekly summary template
        weekly_summary_path = os.path.join(week_dir, f"week{week_num:02d}-summary.md")
        if not os.path.exists(weekly_summary_path):
            with open(weekly_summary_path, "w", encoding="utf-8") as f:
                f.write(weekly_template)
            print(f"Created weekly summary template: {weekly_summary_path}")
        
        # Create daily notes for each workday (Monday to Friday)
        for i in range(5):  # 0=Monday, 4=Friday
            day_date = start_date + timedelta(days=i)
            day_file = os.path.join(daily_dir, f"{day_date.strftime('%Y-%m-%d')}.md")
            
            # Only create if it doesn't exist
            if not os.path.exists(day_file):
                day_content = daily_template.replace("[DATE]", day_date.strftime("%Y-%m-%d"))
                with open(day_file, "w", encoding="utf-8") as f:
                    f.write(day_content)
                print(f"Created daily note: {day_file}")
    except Exception as e:
        print(f"Error setting up week: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    # Ensure base directory exists
    ensure_directory_exists(BASE_DIR)
    
    # Set up templates
    setup_templates()
    
    # Set up current week
    setup_week()
    
    print("Weekly setup complete!")

if __name__ == "__main__":
    main()