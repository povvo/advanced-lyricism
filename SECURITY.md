# Security

## Reporting goal

Use this policy to report a suspected vulnerability in the local tools, bundled assets, dependency handling, or repository workflow without exposing sensitive details publicly.

## Private report

Report security vulnerabilities privately to `povvo.dev@gmail.com`. Include the affected file or route, the smallest reproducible description, impact, and a safe contact method. Do not include credentials, private material, exploit payloads, or sensitive data in public issues, pull requests, or discussions.


## Validation basis

Source inspection was performed against the repository security contact, dependency manifest, bundled asset license paths, and contributor escalation route. No user-edit, developmental test, penetration test, vulnerability scan, or SME confirmation was performed; this policy makes no claim that those activities occurred.

## What happens next

Expect an initial response within 72 hours; the maintainer will request a safer channel if the report contains credentials or private material. The report is considered received when the maintainer acknowledges it by private reply. If no acknowledgement arrives within 72 hours, resend the message with the original timestamp and subject, then use the repository owner’s private GitHub contact path if available.

Do not test a suspected vulnerability against production systems or another person’s data. Preserve the command, version, path, and redacted output needed to reproduce the issue, and stop when further testing could alter data or expose secrets.

This repository contains executable local tools and bundled third-party assets. See the dependency manifest and the individual bundled license files when reviewing a change.
