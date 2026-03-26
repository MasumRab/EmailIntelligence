# Sentinel Security Improvements

## Overly Permissive CORS
Discovered that `src/main.py` defaulted to `allow_origins=["*"]`. Fixed by making it fall back to an empty list `[]` and pulling allowed origins from the `ALLOWED_ORIGINS` environment variable.

## Setup Script Path Vulnerability
Discovered a hardcoded developer path in `src/core/commands/setup_command.py` (`/home/masum/github/EmailIntelligenceGem/`). Replaced with `str(ROOT_DIR)` to make the script secure and portable across environments.

## Unbounded Memory Growth in Rate Limiter
Discovered that `src/utils/rate_limit.py` used a `defaultdict(list)` for request tracking, allowing memory exhaustion from large numbers of unique spoofed IPs. Fixed by implementing an `OrderedDict` with LRU eviction and a `max_clients` cap of 10,000.
