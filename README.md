## Rollback

Docker images are tagged with both `latest` and the Git commit SHA.

To roll back to a previous version:

```bash
export IMAGE_TAG=<previous_commit_sha>
docker compose pull web
docker compose up -d web
