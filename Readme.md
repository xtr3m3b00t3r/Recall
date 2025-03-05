# Recall v25.03

A simple, future-proof system for tracking your daily work activities and compiling weekly summaries.

## About Recall

Recall helps you document your daily accomplishments and automatically compile them into weekly "release notes." This approach gives you:

- A structured way to track what you've accomplished each day
- Easy weekly summaries that highlight your achievements
- A searchable, future-proof archive of your professional activities
- Valuable material for performance reviews, resumes, and reflection

## Features

- Markdown-based note-taking system
- Hierarchical folder organization (Year/Quarter/Week/Day)
- Automated setup of daily notes with consistent templates
- Weekly summary generation from your daily entries
- Plain text storage format for maximum future compatibility
- No external dependencies - built with Python standard library

## Installation

1. Clone this repository or download the files
2. Ensure you have Python 3.6+ installed
3. No third-party packages required!

## Usage

### Initial Setup

```bash
python recall_setup.py
```

This creates the initial folder structure and templates.

### Weekly Workflow

**Monday morning**: 
```bash
python recall_setup.py
```
This automatically creates daily notes for the current week.

**Throughout the week**:
- Fill in your daily note for each day (located in `Recall/YEAR/QUARTER/WEEKXX/daily/`)
- Focus on capturing accomplishments, decisions, and learnings

**Friday afternoon**:
```bash
python recall_compile.py
```
This collects your daily notes and generates a draft weekly summary for you to review and finalize.

## Customization

You can easily customize the templates in the `Recall/Templates/` directory:
- `daily-template.md` - Template for daily notes
- `weekly-template.md` - Template for weekly summaries

## Directory Structure

```
Recall/
├── 2025/
│   ├── Q1/
│   │   ├── Week10-Mar03-Mar09/
│   │   │   ├── daily/
│   │   │   │   ├── 2025-03-03.md
│   │   │   │   ├── 2025-03-04.md
│   │   │   │   ├── ...
│   │   │   ├── week10-summary.md
│   ├── Templates/
│   │   ├── daily-template.md
│   │   ├── weekly-template.md
```

## License

MIT License - See LICENSE file for details.

## Author

Created by Benjamin D.W Truman (2025)