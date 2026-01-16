"""
PydanticAI tools for conference agent.

This module defines the tools available to the agent for interacting
with conference data and email functionality.
"""
from datetime import datetime
from typing import Any

import openpyxl
from pydantic_ai import RunContext

from src.conference_agent.agent.dependencies import AgentDependencies
from src.conference_agent.logging import logger


def list_conference_files(ctx: RunContext[AgentDependencies]) -> dict[str, Any]:
    """
    List all available files in the conference data directory.

    Returns:
        Dict with success status, list of files, and count
    """
    files = []
    if ctx.deps.data_dir.exists():
        for file_path in ctx.deps.data_dir.iterdir():
            if file_path.is_file():
                files.append(file_path.name)

    logger.info(f"TOOL: Listed {len(files)} conference files")
    return {
        "success": True,
        "files": sorted(files),
        "count": len(files),
    }


def read_conference_file(ctx: RunContext[AgentDependencies], filename: str) -> dict[str, Any]:
    """
    Read the content of a specific conference file.

    INTENTIONAL VULNERABILITY: No path traversal protection (for workshop).

    Args:
        filename: Name of the file to read (horaires.txt, programme.txt, participants.xlsx)

    Returns:
        Dict with file content or error
    """
    file_path = ctx.deps.data_dir / filename

    if not file_path.exists():
        available = sorted([f.name for f in ctx.deps.data_dir.iterdir() if f.is_file()])
        return {
            "success": False,
            "error": f"File not found: {filename}",
            "available_files": available,
        }

    try:
        if filename.endswith(('.xlsx', '.xls')):
            # Handle Excel files
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            headers = [cell.value for cell in sheet[1]]
            participants = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                participant = {}
                for header, value in zip(headers, row):
                    if header:
                        participant[header] = value
                participants.append(participant)

            logger.info(f"TOOL: Read Excel file: {filename} ({len(participants)} rows)")
            return {
                "success": True,
                "filename": filename,
                "type": "excel",
                "data": participants,
                "count": len(participants),
            }
        else:
            # Handle text files
            content = file_path.read_text(encoding="utf-8")
            logger.info(f"TOOL: Read text file: {filename} ({len(content)} chars)")
            return {
                "success": True,
                "filename": filename,
                "type": "text",
                "content": content,
            }
    except Exception as e:
        logger.error(f"Error reading file {filename}: {e}")
        return {
            "success": False,
            "error": f"Error reading file: {str(e)}",
        }


def list_emails(ctx: RunContext[AgentDependencies], max_results: int = 10) -> dict[str, Any]:
    """
    List recent emails from the inbox.

    Args:
        max_results: Maximum number of emails to return (default: 10)

    Returns:
        Dict with list of emails
    """
    emails = ctx.deps.mock_inbox[:max_results]
    logger.info(f"TOOL: Listed {len(emails)} emails")

    return {
        "success": True,
        "emails": emails,
        "count": len(emails),
    }


def send_email(
    ctx: RunContext[AgentDependencies],
    to: list[str],
    subject: str,
    body: str,
) -> dict[str, Any]:
    """
    Send an email to one or more recipients.

    INTENTIONAL VULNERABILITY: No recipient authorization check (for workshop).

    Args:
        to: List of recipient email addresses
        subject: Email subject
        body: Email body content

    Returns:
        Dict with send confirmation
    """
    # Validate inputs
    if not to:
        return {"success": False, "error": "No recipients specified"}
    if not subject:
        return {"success": False, "error": "No subject specified"}

    # Mock sending email
    email_record = {
        "id": f"sent_{len(ctx.deps.sent_emails) + 1}",
        "to": to,
        "subject": subject,
        "body": body,
        "sent_at": datetime.now().isoformat(),
    }

    ctx.deps.sent_emails.append(email_record)
    logger.info(f"TOOL: Email sent to {len(to)} recipient(s): {subject}")

    return {
        "success": True,
        "message": f"Email sent to {len(to)} recipient(s)",
        "recipients": to,
        "subject": subject,
        "email_id": email_record["id"],
    }


def read_email(ctx: RunContext[AgentDependencies], email_id: str) -> dict[str, Any]:
    """
    Read the full content of a specific email by ID.

    Args:
        email_id: ID of the email to read

    Returns:
        Dict with full email content
    """
    # Search in mock inbox
    for email in ctx.deps.mock_inbox:
        if email["id"] == email_id:
            logger.info(f"TOOL: Read email: {email_id}")
            return {
                "success": True,
                "email": email,
            }

    # Email not found
    available_ids = [email["id"] for email in ctx.deps.mock_inbox]
    return {
        "success": False,
        "error": f"Email not found: {email_id}",
        "available_ids": available_ids,
    }
