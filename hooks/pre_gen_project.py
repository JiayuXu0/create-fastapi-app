#!/usr/bin/env python3
"""
Pre-generation hook for FastAPI Template Cookiecutter.
Validates user input and ensures project configuration is valid.
"""

import re
import sys

# Get variables from cookiecutter context
project_name = "{{ cookiecutter.project_name }}"
project_slug = "{{ cookiecutter.project_slug }}"
author_email = "{{ cookiecutter.author_email }}"
github_username = "{{ cookiecutter.github_username }}"

def validate_project_name():
    """Validate project name."""
    if not project_name or len(project_name.strip()) < 3:
        print("ERROR: Project name must be at least 3 characters long!")
        sys.exit(1)

def validate_project_slug():
    """Validate project slug (must be valid Python package name)."""
    if not re.match(r'^[a-z][a-z0-9\-]*[a-z0-9]$', project_slug):
        print("ERROR: Project slug must be a valid package name (lowercase, hyphens allowed)")
        print(f"Current slug: {project_slug}")
        sys.exit(1)

def validate_email():
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, author_email):
        print("ERROR: Please provide a valid email address!")
        sys.exit(1)

def validate_github_username():
    """Validate GitHub username."""
    if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-])*[a-zA-Z0-9]$', github_username):
        print("ERROR: Please provide a valid GitHub username!")
        sys.exit(1)

if __name__ == "__main__":
    print("🔍 Validating project configuration...")
    
    validate_project_name()
    validate_project_slug()
    validate_email()
    validate_github_username()
    
    print("✅ Project configuration validated successfully!")
    print(f"📦 Creating project: {project_name}")
    print(f"📁 Project slug: {project_slug}")