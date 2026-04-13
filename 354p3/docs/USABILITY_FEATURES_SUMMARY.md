# Usability Features Summary

This add-on package completes the **Usability Features** section of the CMPT 354 project without changing the team's existing core files.

## 1) Responsive Web Design
A lightweight Flask preview app is included in `usability_web/`.

It demonstrates:
- responsive layout for desktop, tablet, and mobile
- card-based robot overview
- robot detail pages
- touch-friendly buttons and clean spacing
- a dedicated section explaining trigger usage in the project

## 2) SQL Triggers / Integrity Functionality
A separate SQL script is included in:

`SQL Dump/SQLQuery1_complete_with_usability.sql`

This script preserves the project domain and adds integrity-oriented database logic:
- CHECK constraints for positive measurements and versions
- trigger to reject future progress updates
- trigger to automatically increment sub-assembly version after part changes
- trigger to prevent duplicate robot names on insert
- audit table + trigger to log robot deletions before cascade removes dependent rows

## Why this is safe for the team repo
- Existing team files are left unchanged
- Team-added `f6-10/` files remain untouched
- The usability work is added as clearly separated supporting files

## Demo suggestion
For the presentation, you can show:
1. the responsive preview site (`usability_web/app.py`)
2. the trigger section on the homepage
3. the SQL file with the trigger definitions
4. an example delete cascade / audit explanation using `RobotDeleteAudit`
