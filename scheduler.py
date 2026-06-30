"""
Morning digest scheduler — v1.5 (not yet implemented).

Planned behavior:
  - Run daily at 08:00 via cron / launchd
  - Read last 3 daily notes from vault
  - Call Claude API to summarize
  - Print or send digest to stdout / notification

To implement: add `schedule` to requirements.txt, wire up run_digest().
"""

# TODO v1.5: implement morning digest


def run_digest() -> None:
    raise NotImplementedError("Morning digest not yet implemented (v1.5)")


if __name__ == "__main__":
    run_digest()
