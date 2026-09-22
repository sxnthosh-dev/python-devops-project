FROM kimai/kimai2:stable

EXPOSE 8001

ENTRYPOINT ["docker-php-entrypoint"]

CMD ["/entrypoint.sh"]

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=30s \
    CMD curl -f http://127.0.0.1:8001 || exit 1
