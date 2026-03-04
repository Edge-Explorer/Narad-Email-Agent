import os
import sys
from fastmcp import FastMCP
from dotenv import load_dotenv

# Ensure we can import from our internal directories and find local files (.env, .db).
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)
os.chdir(base_path)

from agents.email_agent import EmailAgent
from core.composer import EmailComposer
from core.summarizer import EmailSummarizer
from core.database import NaradDatabase

# Initialize MCP Server
mcp = FastMCP("Narad Email Agent")

# Initialize Narad Components
load_dotenv()
agent = EmailAgent()
summarizer = EmailSummarizer()
db = NaradDatabase()

@mcp.tool()
def apply_for_job(
    goal: str,
    recipient_email: str,
    recipient_name: str = "",
    job_title: str = "Job Applicant",
    job_description: str = "",
    cv_profile: str = None
) -> str:
    """
    Drafts and sends a personalized job application email.
    
    Args:
        goal: The natural language goal (e.g. 'Apply for AI role').
        recipient_email: The email address to send to.
        recipient_name: The name of the recipient or company.
        job_title: The title of the job you're applying for.
        job_description: The full text of the job description.
        cv_profile: Optional filename of the CV to use from the 'resumes/' folder.
    """
    try:
        composer = EmailComposer(cv_filename=cv_profile)
        draft = composer.draft_email(goal, tone="formal", job_description=job_description, recipient_info=recipient_name)
        
        resume_path = os.path.join("resumes", composer.current_cv)
        result = agent.send_email(recipient_email, draft['subject'], draft['body'], attachment_path=resume_path)
        
        # Log to CRM
        db.log_application(recipient_email, recipient_name, recipient_name, job_title, job_description)
        
        return f"Status: {result}\nCRM: Application logged for {recipient_name}."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def check_inbox(count: int = 5) -> str:
    """
    Fetches the latest emails from your inbox.
    """
    try:
        emails = agent.fetch_latest_emails(count=count)
        if not emails:
            return "Inbox is empty."
        
        output = "Latest Emails:\n"
        for idx, e in enumerate(emails, 1):
            output += f"[{idx}] From: {e['from']} | Subject: {e['subject']} | Date: {e['date']}\n"
        return output
    except Exception as e:
        return f"Error Check Inbox: {e}"

@mcp.tool()
def summarize_inbox() -> str:
    """
    Uses AI to generate a concise summary of your recent emails.
    """
    try:
        emails = agent.fetch_latest_emails(count=5)
        if not emails:
            return "No emails to summarize."
        return summarizer.summarize_emails(emails)
    except Exception as e:
        return f"Error Summarizing: {e}"

@mcp.tool()
def get_job_stats() -> str:
    """
    Returns a summary of your job applications from the local CRM.
    """
    try:
        apps = db.get_pending_followups()
        if not apps:
            return "No applications logged in CRM yet."
        
        output = f"Total Applications: {len(apps)}\n"
        output += "-" * 30 + "\n"
        for a in apps[:10]:
            output += f"ID: {a[0]} | Company: {a[3]} | Status: {a[5]} | Date: {a[6][:10]}\n"
        return output
    except Exception as e:
        return f"Error CRM stats: {e}"

@mcp.tool()
def prepare_for_interview(app_id: int = None) -> str:
    """
    Generates a personalized interview prep guide for a specific application.
    If no ID is provided, it uses the most recent application.
    """
    try:
        apps = db.get_pending_followups()
        if not apps:
            return "No applications found to prepare for."
        
        # Find specific app or use last
        selected_app = None
        if app_id:
            for a in apps:
                if a[0] == app_id:
                    selected_app = a
                    break
        else:
            selected_app = apps[0]
            
        if not selected_app:
            return f"Application ID {app_id} not found."
        
        company = selected_app[3]
        jd = selected_app[8]
        composer = EmailComposer() # Uses default CV
        
        prompt = f"""
        I have an interview at {company}. 
        Here is the Job Description: {jd}
        Here is my CV context: {composer.cv_content[:2000]}
        
        Provide:
        1. Top 5 technical questions they might ask me.
        2. Top 3 behavioral questions.
        3. A "Perfect Pitch" for how I should introduce myself for this specific role.
        """
        return composer.gemini.generate_content(prompt)
    except Exception as e:
        return f"Error Prep Interview: {e}"

@mcp.resource("narad://resumes")
def list_cv_profiles() -> str:
    """Lists all available resume files in the resumes folder."""
    try:
        composer = EmailComposer()
        profiles = composer.list_profiles()
        return "\n".join(profiles) if profiles else "No resumes found in 'resumes/' folder."
    except Exception as e:
        return f"Error list profiles: {e}"

if __name__ == "__main__":
    mcp.run()
