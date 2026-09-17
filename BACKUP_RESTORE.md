# Database Backup & Restore

## Overview

This document describes the backup and restore procedure for the MariaDB database used by the Python DevOps project.

The database name is:

`devops_db`

The application database user is:

`devuser`

---

## 1. Create a Database Backup

Make sure the project is running:

```bash
docker compose up -d
