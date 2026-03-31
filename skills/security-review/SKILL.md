---
name: security-review
description: Use when performing a security-focused review of code, diffs, or specs, especially for auth, authorization, input validation, secrets, injection, data exposure, and Spring Security configurations.
---

# Security Review

## Overview
Run a security-focused review that favors exploitable, evidence-backed findings over generic advice. Use manual reasoning to trace trust boundaries, attack paths, and security regressions that scanners often miss.

## When to Use
- Reviewing diffs, files, features, or specs for security risk
- Changes touching auth, session handling, secrets, uploads, external calls, persistence, or AI/LLM features
- Auditing Spring or Spring Security configuration and request flows
- Performing quick triage on fast-moving or AI-generated codebases where convenience may have beaten security

Do not use this skill for formal pentest reports, exploit development, or deep cryptographic design review.

## Inputs
- `content` — Review target: diff, file, function, feature, config, or spec
- `also_consider` (optional) — Threat model, asset sensitivity, framework context, deployment assumptions, or specific risk areas

## Core Principle
Review like an attacker, report like an engineer: find the simplest realistic path to compromise, privilege escalation, sensitive data exposure, or unsafe code execution, then give concrete evidence and remediation.

## Execution

### Step 1: Establish Scope
1. Load only the provided review target.
2. Determine whether the scope is:
   - diff-based review
   - full-file/function review
   - spec/design review
3. Identify trust boundaries and security-sensitive surfaces inside scope:
   - request entry points
   - authentication/session boundaries
   - authorization checks
   - data access paths
   - file or object handling
   - external network calls
   - logging/error handling
   - secrets/config loading
   - code execution or LLM/tool invocation paths
4. If content is empty or unreadable, halt and report that no security analysis was possible.

### Step 2: Trace Security-Critical Flows
Walk the content in this order:

1. **Inputs to sinks**
   - trace user-controlled input to database queries, HTML output, file paths, shell/system calls, templates, deserializers, and external requests
2. **Identity to authorization**
   - trace how user identity is established
   - verify privileged actions derive identity and role from trusted server-side state, not client input
3. **Data access to ownership**
   - trace object/record lookup paths
   - verify ownership, tenant isolation, and post-auth authorization
4. **Configuration to exposure**
   - trace secrets, flags, credentials, and environment-specific behavior
5. **State transitions**
   - trace login, reset, admin, payment, upload, and multi-step operations for bypasses, race conditions, or partial-failure gaps

### Step 3: Apply Security Checklist

#### 1. Secrets and Configuration
- Hardcoded API keys, tokens, passwords, signing secrets, database URLs
- Secrets in frontend bundles, client config, logs, comments, fixtures, or properties
- Unsafe defaults such as debug enabled, permissive dev fallbacks, test bypasses
- Missing environment separation or production-safe defaults

#### 2. Authentication and Session Security
- Missing authentication on privileged routes
- Trust in client-provided identity, role, or account identifiers
- JWT/session validation gaps, missing expiry, weak invalidation, insecure cookie flags
- Weak password reset, magic link, MFA, or re-auth flows
- Missing brute-force or abuse controls on auth endpoints

#### 3. Authorization and Data Exposure
- IDOR / BOLA / broken object-level authorization
- Missing ownership or tenant checks on reads, writes, and searches
- Client-side-only authorization
- Function-level access control gaps on admin or support operations
- Sensitive data returned too broadly or logged unnecessarily

#### 4. Validation and Injection
- Missing server-side validation
- SQL/NoSQL/LDAP/command/template injection
- XSS via unsafe rendering or untrusted rich content
- SSRF, path traversal, open redirect, XXE, unsafe deserialization
- Mass assignment / over-posting on ORM or DTO binding

#### 5. Code Execution and AI/LLM Risk
- `eval`, `exec`, shell invocation, dynamic template compilation, unsafe plugin execution
- LLM output used in code, SQL, shell, or privilege-bearing operations without validation
- User input mixed into system prompts or tool instructions without boundary separation
- Tool/function calling without argument validation or allowlists

#### 6. File and Object Handling
- Uploads without type, size, content, or storage controls
- Use of original filenames or executable/public storage paths
- Archive extraction, image/document parsing, or conversion of untrusted files without safeguards

#### 7. Error Handling, Logging, and Monitoring
- Sensitive data in logs, traces, metrics, or error responses
- Stack traces or debug detail exposed to users
- Missing security event logging for auth failure, privilege changes, or sensitive actions

#### 8. Dependency and Platform Hygiene
- Known-vulnerable or abandoned dependencies in critical paths
- Unsafe framework defaults left unreviewed
- Missing HTTPS, security headers, rate limits, or request size/resource limits where relevant

### Step 4: Spring and Spring Security Checks
When the code uses Spring, Spring Boot, or Spring Security, explicitly verify:

- deny-by-default authorization posture
- server-side method or request authorization on privileged operations
- DTO / bean validation on external request boundaries
- parameterized SQL/JPQL/native queries and safe repository usage
- CSRF posture matches endpoint type:
  - enabled by default for session/cookie-backed unsafe methods
  - any disablement is justified and narrow
  - SPA integrations handle token repository and header flow correctly
- CORS is origin-specific and not wildcard-plus-credentials
- cookies/session settings are secure
- no secrets in `application*.properties`, YAML, logs, or fixtures

### Step 5: Filter for Signal
Report only findings that are:
- directly supported by the provided content
- plausibly exploitable or materially weakening security
- specific enough to fix

Do not report:
- vague hypotheses without evidence
- style-only observations
- generic “consider adding security” advice
- dependency CVEs without plausible relevance to this usage

### Step 6: Present Findings
Return concise Markdown with:
1. short summary of security posture in scope
2. prioritized findings
3. concrete remediation guidance
4. uncovered areas or assumptions, if they materially limit confidence

## Output Format

```markdown
## Security Review Summary

**Assessment**: CLEAN | NEEDS ATTENTION | HIGH RISK

## Findings
### [high] Broken object ownership check
- **Location**: `src/orders/OrderController.java:84`
- **Issue**: Order lookup uses request `orderId` without verifying current user ownership.
- **Impact**: Authenticated users can access other users' orders.
- **Evidence**: Repository query filters by `id` only; no tenant/user constraint appears in scope.
- **Fix**: Add server-side ownership/tenant predicate and return not found on mismatch.

## Uncovered Areas
- Session validation implementation not provided; cookie flags could not be confirmed.
```

## Review Rules
- Prefer attack paths over checklists.
- Open surrounding context before finalizing a finding when the provided content allows it.
- Call out assumptions explicitly when certainty depends on unseen code.
- Favor practical remediation, not generic policy language.
- Default to review-only; do not implement fixes unless the user asks.

## Halt Conditions
- HALT if content is empty, unreadable, or missing.
- HALT if the requested conclusion would require speculation beyond provided evidence.
