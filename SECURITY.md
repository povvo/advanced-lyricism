# Security

## Reporting goal

Use this policy to report a suspected vulnerability in the local tools, bundled assets, dependency handling, or repository workflow without exposing sensitive details publicly.

## Private report

Report security vulnerabilities privately to `povvo.dev@gmail.com`. Include the affected file or route, the smallest reproducible description, impact, and a safe contact method. Do not include credentials, private material, exploit payloads, or sensitive data in public issues, pull requests, or discussions.
## What happens next

The maintainer will review the report and request a safer channel if it contains credentials or private material. Preserve the command, version, path, and redacted output needed to reproduce the issue. Do not test a suspected vulnerability against production systems or another person’s data, and stop when further testing could alter data or expose secrets.

This repository contains executable local tools and bundled third-party assets. See the dependency manifest and the individual bundled license files when reviewing a change.
