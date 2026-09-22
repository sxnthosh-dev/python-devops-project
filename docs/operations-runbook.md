# Operations Runbook

## Start the stack

    docker compose up -d

## Stop the stack without deleting data

    docker compose stop

## Start stopped services

    docker compose start

## Check container status

    docker compose ps

## Check Kimai

    curl -I http://127.0.0.1
    curl -I http://127.0.0.1:8000

## Check Prometheus

    curl http://127.0.0.1:9090/-/healthy

## Grafana

http://127.0.0.1:3000

## Logs

    docker compose logs --tail=100 kimai
    docker compose logs --tail=100 kimai2
    docker compose logs --tail=100 nginx
    docker compose logs --tail=100 db

## Health checks

    docker inspect kimai_app --format="Kimai1={{.State.Health.Status}}"
    docker inspect kimai_app_2 --format="Kimai2={{.State.Health.Status}}"
    docker inspect devops-mariadb --format="MariaDB={{.State.Health.Status}}"

## Terraform safety

Run terraform plan before making infrastructure changes. Do not run terraform apply if it proposes replacing the working MariaDB or Kimai containers.

## Data safety

Do not use docker compose down -v because persistent volumes may be deleted.

## Backup

    mkdir -p backups
    ls -lh backups/

## Rollback

Change the Kimai image tag in docker-compose.yml and recreate the Kimai service:

    docker compose up -d --force-recreate kimai

## Git documentation workflow

    git status --short
    git diff --check
    git add docs/
    git commit -m "Complete project documentation and final audit"
    git push origin main
