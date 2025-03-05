import os
import re
from datetime import datetime, timedelta
import glob
import argparse

# Base directory for all release notes
BASE_DIR = "Work-Release-Notes"

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

def find_week_directory(target_date=None):
    """Find the directory for the specified week"""
    if target_date is None:
        target_date = datetime.now()
    
    start_date, _ = get_week_dates(target_date)
    
    year_dir = os.path.join(BASE_DIR, str(start_date.year))
    quarter_dir = os.path.join(year_dir, get_quarter(start_date))
    
    # Get week number
    week_num = start_date.isocalendar()[1]  # ISO week number
    
    # Look for week directory
    week_pattern = f"Week{week_num:02d}-*"
    matching_dirs = glob.glob(os.path.join(quarter_dir, week_pattern))
    
    if matching_dirs:
        return matching_dirs[0]
    else:
        raise FileNotFoundError(f"Could not find directory for week {week_num} of {start_date.year}")

def extract_section_content(content, section_name):
    """Extract content from a specific markdown section"""
    pattern = rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |$)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def compile_weekly_summary(week_dir):
    """Compile daily notes into weekly summary"""
    # Find daily notes directory
    daily_dir = os.path.join(week_dir, "daily")
    if not os.path.exists(daily_dir):
        raise FileNotFoundError(f"Daily notes directory not found: {daily_dir}")
    
    # Find all daily notes from the week, sorted by date
    daily_files = sorted(glob.glob(os.path.join(daily_dir, "*.md")))
    
    if not daily_files:
        print("No daily notes found for this week.")
        return
    
    # Find weekly summary file
    weekly_files = glob.glob(os.path.join(week_dir, "week*-summary.md"))
    if not weekly_files:
        raise FileNotFoundError(f"Weekly summary template not found in {week_dir}")
    
    weekly_summary_path = weekly_files[0]
    
    # Read current weekly summary
    with open(weekly_summary_path, "r") as f:
        weekly_content = f.read()
    
    # Collect daily note sections
    all_accomplishments = []
    all_projects = set()
    all_learnings = []
    all_challenges = []
    all_follow_ups = []
    all_decisions = []
    all_collaborations = []
    
    for daily_file in daily_files:
        with open(daily_file, "r") as f:
            daily_content = f.read()
        
        # Extract date from filename
        day_date = os.path.basename(daily_file).replace(".md", "")
        
        # Extract relevant sections
        tasks = extract_section_content(daily_content, "🛠️ Tasks Completed")
        if tasks:
            all_accomplishments.extend([f"- {line.strip()}" for line in tasks.split("\n") if line.strip()])
        
        projects = extract_section_content(daily_content, "🏗️ Projects Worked On")
        if projects:
            all_projects.update([line.strip()[2:] for line in projects.split("\n") if line.strip()])
        
        learnings = extract_section_content(daily_content, "🧠 Learnings")
        if learnings:
            all_learnings.extend([f"- {line.strip()}" for line in learnings.split("\n") if line.strip()])
        
        challenges = extract_section_content(daily_content, "🚧 Blockers & Challenges")
        if challenges:
            all_challenges.extend([f"- {line.strip()}" for line in challenges.split("\n") if line.strip()])
        
        follow_ups = extract_section_content(daily_content, "📌 Follow-ups Needed")
        if follow_ups:
            all_follow_ups.extend([f"- {line.strip()}" for line in follow_ups.split("\n") if line.strip()])
        
        decisions = extract_section_content(daily_content, "🤔 Decisions Made")
        if decisions:
            all_decisions.extend([f"- {line.strip()}" for line in decisions.split("\n") if line.strip()])
        
        notes = extract_section_content(daily_content, "📝 Notes for Weekly Summary")
        if notes:
            all_accomplishments.extend([f"- {line.strip()}" for line in notes.split("\n") if line.strip()])
    
    # Project progress section
    project_sections = []
    for project in all_projects:
        project_sections.append(f"""### {project}
- Status: [On Track/At Risk/Blocked]
- Progress:
  - 
- Next Steps:
  - 
""")
    
    # Update weekly summary sections
    weekly_content = re.sub(
        r"## 🌟 Key Accomplishments\s*\n(.*?)(?=\n## )",
        f"## 🌟 Key Accomplishments\n\n{chr(10).join(all_accomplishments)}\n\n",
        weekly_content,
        flags=re.DOTALL
    )
    
    # Update project progress section with discovered projects
    if project_sections:
        project_section = "## 📊 Project Progress\n\n" + "\n".join(project_sections)
        weekly_content = re.sub(
            r"## 📊 Project Progress\s*\n(.*?)(?=\n## )",
            f"{project_section}\n\n",
            weekly_content,
            flags=re.DOTALL
        )
    
    # Update learnings section
    if all_learnings:
        weekly_content = re.sub(
            r"## 💎 Key Learnings & Insights\s*\n(.*?)(?=\n## )",
            f"## 💎 Key Learnings & Insights\n\n{chr(10).join(all_learnings)}\n\n",
            weekly_content,
            flags=re.DOTALL
        )
    
    # Update challenges section
    if all_challenges:
        weekly_content = re.sub(
            r"## 🚧 Challenges & Blockers\s*\n(.*?)(?=\n## )",
            f"## 🚧 Challenges & Blockers\n\n{chr(10).join(all_challenges)}\n\n",
            weekly_content,
            flags=re.DOTALL
        )
    
    # Save compiled summary with _draft suffix
    draft_path = weekly_summary_path.replace(".md", "_draft.md")
    with open(draft_path, "w") as f:
        f.write(weekly_content)
    
    print(f"Draft weekly summary compiled to: {draft_path}")
    print("\nNote: This is a draft. Please review and edit before finalizing.")
    print("To finalize, rename the file by removing '_draft' from the filename.")

def main():
    parser = argparse.ArgumentParser(description="Compile weekly release notes from daily notes")
    parser.add_argument("--date", help="Target date in YYYY-MM-DD format (defaults to today)")
    
    args = parser.parse_args()
    
    if args.date:
        target_date = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        target_date = datetime.now()
    
    try:
        week_dir = find_week_directory(target_date)
        compile_weekly_summary(week_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()