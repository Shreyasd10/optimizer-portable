---
name: create-pr
description: Generate pull request descriptions and creation commands from branch diff context. Use when the user asks to create a PR or needs a structured PR summary.
---

# Create Pr

## Goal
Generate pull request descriptions and creation commands from branch diff context. Use when the user asks to create a PR or needs a structured PR summary.

## Your Role
You are the `create-pr` specialist. Be skeptical of weak assumptions, precise in recommendations, and explicit about missing information.

## Inputs
- `content` — The target material to process (code, diff, spec, logs, task request, or workflow context).
- `also_consider` optional — Additional constraints, priorities, or risks to account for.

## Execution
### Step 1: Receive Scope
1. Load the provided content and identify artifact type and boundaries.
2. If scope is unclear, request clarification before proceeding.

### Step 2: Apply Skill-Specific Guidance
1. Execute the guidance below with strict adherence to sequence and constraints.
2. Highlight assumptions and unresolved dependencies explicitly.

#### Skill-specific guidance
Generate a PR description summarizing code changes using a predefined template.

## Interactive Mode Flags

This skill supports the following optional flags to customize behavior:

| Flag | Description |
|------|-------------|
| `--auto` | Skip all confirmations and use detected defaults |
| `--verbose` | Show detailed analysis output during each step |
| `--dry-run` | Preview the PR description without creating or saving |
| `--draft` | Create PR as draft (when using gh CLI) |

**Usage examples:**
- `create-pr --auto` - Generate and create PR with all defaults
- `create-pr --verbose --dry-run` - Show detailed analysis without saving
- `create-pr --draft` - Create a draft PR for early review

## Steps

### Step 1. Identify Source Branch
Use the current working branch as the source branch.

**Error Handling:**
- If in detached HEAD state, warn the user and ask them to checkout a branch first
- If there are uncommitted changes, warn the user and ask if they want to proceed or commit first
- Run: `git status --porcelain` to detect uncommitted changes
- Run: `git symbolic-ref --short HEAD 2>/dev/null || echo "DETACHED"` to check branch state

### Step 2. Detect Target Branch
Detect the target branch automatically:
- Check if the current repo has a `main` branch; use it as default
- If `main` doesn't exist, check for `develop`, then `master`
- If none exist, ask the user to specify the target branch
- Display the detected target branch and ask for confirmation (allow override)

**Error Handling:**
- If no target branch can be detected and user doesn't specify one, abort with clear message
- Run: `git branch -r | grep -E 'origin/(main|develop|master)$'` to check remote branches
- Fallback: `git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's|origin/||'` for default branch

### Step 3. Validate Branch State
Before proceeding with diff analysis, validate the branch state:

**Branch Naming Convention Check:**
- Detect if branch follows common naming patterns: `feature/`, `bugfix/`, `hotfix/`, `release/`, `chore/`, `docs/`
- If branch doesn't follow conventions, warn but allow proceeding
- Extract ticket/issue ID from branch name if present (e.g., `feature/JIRA-123-description`)

**Upstream Tracking Verification:**
- Run: `git rev-parse --abbrev-ref @{upstream} 2>/dev/null` to check tracking branch
- If no upstream, warn user that branch may not be pushed yet

**Merge Conflict Detection:**
- Run: `git merge-tree $(git merge-base HEAD <target-branch>) HEAD <target-branch>` to preview merge
- If conflicts detected, list conflicting files and warn user before proceeding
- Allow user to abort or continue with PR creation

### Step 4. Verify Branch Divergence
Verify the branches diverge by running git diff:
- Run: `git diff <target-branch>...HEAD --name-only` to list changed files
- Run: `git log <target-branch>..HEAD --oneline` to extract commit messages
- If no differences exist, stop and inform the user
- Handle special cases: skip merge commits (`--no-merges` flag), handle file renames and deletions gracefully
- If differences exist, proceed to Step 5

**Error Handling:**
- If `git diff` fails, check if target branch exists locally: `git branch --list <target-branch>`
- If target branch doesn't exist locally, try fetching: `git fetch origin <target-branch>`
- If still failing, provide clear error message with suggested fixes

### Step 5. Collect Semantic Information
Extract commit messages between source and target branches using: `git log <target-branch>..HEAD --format="%s%n%b"`

**Conventional Commit Parsing:**
Parse commits for conventional commit prefixes and auto-categorize:

| Prefix | Category | Type of Change |
|--------|----------|----------------|
| `feat:` | New feature | ✨ New feature |
| `fix:` | Bug fix | 🐛 Bug fix |
| `docs:` | Documentation | 📚 Documentation update |
| `chore:` | Maintenance | 📦 Chore |
| `refactor:` | Refactoring | ♻️ Refactor |
| `test:` | Testing | ✅ Tests added |
| `style:` | Formatting | 🎨 Style change |
| `perf:` | Performance | ⚡ Performance improvement |
| `ci:` | CI/CD | 🏗️ Build/CI related changes |
| `build:` | Build system | 🏗️ Build/CI related changes |

**Breaking Change Detection:**
- Search commit bodies for `BREAKING CHANGE:` or `BREAKING-CHANGE:` markers
- Search for commits with `!` suffix (e.g., `feat!:`, `fix!:`)
- If found, automatically check the "💥 Breaking change" box in Type of Change

**File Categorization:**
If commit messages are poor quality (generic like "fix bug", "update", "changes"), extract meaningful context from the git diff instead.

Parse the git diff to identify files changed by type. Use project-specific patterns based on detected project type:

**Auto-detect project type from:**
- `pom.xml` → Java/Maven project
- `build.gradle` → Java/Gradle project
- `package.json` → JavaScript/TypeScript project
- `go.mod` → Go project
- `pyproject.toml`, `setup.py`, `requirements.txt` → Python project
- `Cargo.toml` → Rust project
- `*.csproj`, `*.sln` → .NET project

**File categorization patterns by project type:**

| Project Type | Source Code | Tests | Configuration |
|--------------|-------------|-------|---------------|
| Java (Maven) | `src/main/java/**`, `src/main/resources/**` | `src/test/**` | `pom.xml`, `application.properties`, `application.yml` |
| Java (Gradle) | `src/main/java/**`, `src/main/resources/**` | `src/test/**` | `build.gradle`, `application.properties`, `application.yml` |
| JavaScript/TS | `src/**`, `lib/**` | `test/**`, `__tests__/**`, `*.test.js`, `*.spec.ts` | `package.json`, `tsconfig.json`, `*.config.js` |
| Python | `src/**`, `<package_name>/**` | `tests/**`, `test_*.py`, `*_test.py` | `pyproject.toml`, `setup.py`, `setup.cfg` |
| Go | `**/*.go` (excluding `*_test.go`) | `**/*_test.go` | `go.mod`, `go.sum` |
| Rust | `src/**/*.rs` | `tests/**`, `**/tests.rs` | `Cargo.toml` |
| Generic | `src/**`, `lib/**` | `test/**`, `tests/**`, `spec/**` | `*.json`, `*.yml`, `*.yaml`, `*.toml` |

**Common patterns (all projects):**
- Documentation: `*.md`, `docs/**`, `*.rst`, `*.txt`
- CI/CD: `.github/**`, `.gitlab-ci.yml`, `azure-pipelines.yaml`, `Jenkinsfile`
- Docker: `Dockerfile`, `docker-compose.yml`, `.dockerignore`

Categorize changes: new features, bug fixes, refactoring, configuration, tests, documentation, dependencies, or migrations.

### Step 6. Detect Breaking Changes
Search for breaking indicators:
- Removed or renamed public methods/endpoints
- Changed method signatures or endpoint paths
- Database schema changes (ALTER TABLE, DROP)
- Configuration property removals or renamed keys
- Changed enums or constants that are externally referenced
- Commits marked with `BREAKING CHANGE:` or `!` suffix

If breaking changes detected, escalate to "Type of Change" section and flag for review. Document what breaks and migration path if available.

### Step 7. Analyze Cross-Service Impacts
Analyze impacts on related services and systems. This section is configurable based on your project:

**Auto-detection:**
- Scan for service client files (e.g., `*Client.java`, `*Service.java`, `*Api.ts`)
- Look for HTTP client configurations, Feign clients, RestTemplate usage
- Check for message queue producers/consumers (Kafka, RabbitMQ, SQS)

**For projects with explicit service dependencies:**
- Check project configuration for defined service dependencies:
  - Look for `services.yml`, `dependencies.yml`, or similar config files
  - Parse environment variables referencing external service URLs
  - Scan for OpenAPI/Swagger client generated code directories

**If project-specific services are defined (via config or user input):**
- Note which services are impacted by the changes
- Document API contract changes that affect downstream services
- Flag changes that require coordinated deployments

**Product/Entity Hierarchy (if applicable):**
- If the project uses a configurable entity hierarchy model (e.g., `productGroup → product → subProduct → transactionType`), flag changes as high-impact
- Check project documentation or configuration for hierarchy definitions
- Ask user to confirm hierarchy structure on first run if not auto-detected

**Bulk Processing/Workflows (if applicable):**
- If changes touch file processing, ETL, or workflow systems, note affected pipelines
- Document impact on batch jobs or scheduled tasks

### Step 8. Generate the PR Description
Follow the exact structure and headings of the template below:
- Use commit messages and file categories to populate sections
- Auto-populate "Type of Change" checkboxes based on conventional commit prefixes detected in Step 5
- If a section is not applicable, omit it entirely (do not write "N/A")
- Prioritize important changes; if there are more than 15 file changes, summarize by category rather than listing each file
- For each major section, include examples or specific file names where relevant

**Check for existing PR template:**
- Look for `.github/PULL_REQUEST_TEMPLATE.md` or `.github/pull_request_template.md`
- If found, merge required sections from existing template with generated content
- Preserve any custom sections defined in the project template
- Warn user if project template has required fields not automatically populated

### Step 9. Validate and Enforce Constraints
Count characters (excluding markdown formatting). If the description exceeds 4000 characters, prioritize sections in this order:
1. Title and Description
2. Pull Request Summary, Type of Change, and Breaking Changes
3. Core Implementation (keep only key components)
4. API and Specification Changes
5. Cross-Service Impacts
6. Testing
7. Configuration
8. Related Issues

Trim the least critical sections until under 4000 characters.

### Step 10. Output and Actions
Display the full PR description in the terminal and save it to `.pr-description.md` by default.

**Output Options:**
- Copy the description to clipboard
- Save the description to `.pr-description.md` (required default)
- Display character count and section summary

**Auto-labeling Suggestions:**
Based on file changes, suggest labels for the PR:
| File Pattern | Suggested Label |
|--------------|-----------------|
| `*.md`, `docs/**` | `documentation` |
| `*test*`, `*spec*` | `tests` |
| `*.yml`, `*.yaml`, `*.json` (config) | `configuration` |
| `.github/**`, `Jenkinsfile`, `azure-pipelines.*` | `ci/cd` |
| `Dockerfile`, `docker-compose.*` | `docker` |
| `pom.xml`, `package.json`, `go.mod` | `dependencies` |
| Breaking change detected | `breaking-change` |
| Security-related files | `security` |

**Optional PR Creation Commands (only if user explicitly asks):**
- **Standard PR**: `gh pr create --title "<title>" --body-file .pr-description.md`
- **Draft PR**: `gh pr create --draft --title "<title>" --body-file .pr-description.md`
- **PR with labels**: `gh pr create --label "<label1>,<label2>" --title "<title>" --body-file .pr-description.md`
- **PR with reviewers**: `gh pr create --reviewer "<user1>,<user2>" --title "<title>" --body-file .pr-description.md`

Check if `gh` CLI is available only when user asks to create PR directly: `which gh && gh auth status`

**Error Handling:**
- If `gh` CLI is not installed, provide installation instructions
- If `gh` is not authenticated, prompt: `gh auth login`
- If PR creation fails, show error and allow retry with different options

### Step 11. Prompt User for Next Action
Default action: return the generated markdown content and confirm `.pr-description.md` path.

Ask user preference:
- Use the markdown file as-is
- Regenerate with different options
- Create PR using gh CLI commands (only on explicit request)

## Template

### 📝 Title
[Keep under 70 characters. Extract from the most common theme in commit messages or primary file changes. Be specific about what changed.]

**Format:** `<type>: <description>` (following conventional commits if detected)

**Examples:**
- ❌ "Update code"
- ❌ "Fix bug"
- ✅ "feat: Add user management endpoints for post-approval workflow"
- ✅ "fix: Resolve duplicate product hierarchy sync in bulk upload"
- ✅ "refactor: Optimize authorization caching logic"

### 📄 Description
[One sentence summarizing the change. Extract from commit messages if available. State the business value or problem solved.]

**Example:** "Adds new user management endpoints to support the post-approval workflow for corporate product assignments."

### 📌 Pull Request Summary
[2-3 sentences providing context. Include what was changed and why. Reference any additions to OpenAPI specifications or other contracts. Use commit history to inform this section. For service orchestration changes, explain the interaction pattern with dependent services.]

**Example:** "This PR introduces new endpoints for managing users after approval in the UPS (User Platform Service) integration. The changes support the post-approval workflow where corporates can assign additional products to existing users. OpenAPI specs have been updated to reflect the new `/users/{userId}/products` endpoints."

### 💥 Breaking Changes
[Include only if applicable. Document what breaks, the impact, and migration path.

**Criteria for breaking changes:**
- Removed or renamed public API endpoints
- Changed request/response schema for existing endpoints
- Removed configuration properties
- Changed method signatures in public interfaces
- Database schema changes requiring migrations
- Changes to entity hierarchy structure or validation rules
- Commits containing `BREAKING CHANGE:` or using `!` suffix

**Format:**
- What breaks: [specific endpoint, property, or interface]
- Impact: [which services/clients are affected]
- Migration path: [how to upgrade, deprecation timeline, or workarounds]]

### ⚙️ API and Specification Changes
[Include only if applicable. Detail new endpoints, schema components, or contract modifications. Specify HTTP methods, paths, request/response fields.

**Format:**
- New endpoints: POST /users/{userId}/products, GET /users/{userId}/products
- Modified endpoints: PUT /corporates/{corporateId}/hierarchy (added hierarchyVersion field)
- New schemas: UserProductAssignment, ProductHierarchyNode
- Removed endpoints: [if any]
- OpenAPI spec updates: [file paths and summary]

If no API changes, omit this section.]

### 🛠️ Core Implementation
[Include only if applicable. List the primary components affected by this change. Focus on significant implementation details, not trivial refactoring. Group changes by component type and note files impacted:]

- **Controller**: [endpoints modified or created; file paths]
- **Service Layer**: [business logic changes; file paths]
- **HTTP Client**: [external API calls or integration changes; file paths]
- **Mapper**: [data transformation changes; file paths]
- **Repository**: [database query changes; file paths]
- **Utilities**: [helper functions or common code; file paths]
- **Models**: [domain model changes or new entities; file paths]

**Example:**
- **Controller**: UserProductController.java - added POST /users/{userId}/products endpoint
- **Service Layer**: UserProductService.java - orchestrates service calls
- **HTTP Client**: UpsClient.java - new method assignProductsToUser()
- **Mapper**: UserProductMapper.java - converts DTO to domain model

### ✅ Testing
[Include only if applicable. Summarize new tests, updated test cases, or coverage improvements. Mention test types: unit, integration, E2E. Reference test file paths.]

**Format:**
- Unit tests added: [test class names and what they validate]
- Integration tests added: [test scenarios with mocked services]
- E2E tests added: [full workflow tests if applicable]
- Coverage: [if coverage increased, specify percentage or components]

**Example:** "Added UserProductControllerTest with 8 unit tests for endpoint validation. Added UserProductServiceIntegrationTest with mocked service responses."

### 🔧 Configuration
[Include only if applicable. List changes to configuration files. Exclude environment-specific configs (local, dev, prod) that are not committed. Note: Do NOT include credentials, secrets, or local-only configurations.

**Format:**
- application.properties: [property name changes, additions, removals with descriptions]
- application.yml: [YAML structure changes]
- pom.xml / package.json / go.mod: [dependency additions, version updates]
- Deployment configs: [any changes to container/orchestration configs]

**Example:** "Added api.ups.product-assignment-endpoint property to configure the UPS endpoint URL. Updated api.ups.timeout from 5000ms to 8000ms."]

### 🔀 Cross-Service Impacts
[Include only if applicable. Document interactions with dependent services and system-wide impacts.

**Format (customize based on your project's services):**
- **Service A**: [what APIs are called, data exchanged, impact]
- **Service B**: [what APIs are called, data exchanged, impact]
- **Entity/Product Hierarchy**: [if changes affect multi-level hierarchies, explain impact]
- **Batch Processing**: [if changes affect file processing or workflows, note affected pipelines]

**Example:** "Changes introduce new API calls to User Service during the post-approval workflow. Authorization service must be updated to reflect new assignments. Entity hierarchy validation logic enhanced."]

### 🔍 Related Issues
[Include only if applicable. Link to related issues, tasks, or user stories.

**Format:**
- Addresses #[issue_number] - [brief description]
- Relates to #[issue_number] - [brief description]
- Closes #[issue_number] - [brief description]

**Auto-detection:** Extract issue numbers from branch name (e.g., `feature/JIRA-123-description`) or commit messages.

**Example:**
- Addresses #12345 (User Management Post-Approval Feature)
- Relates to #12340 (Bulk Upload Enhancements)]

### 👥 Recommended Reviewers
[Suggest who should review based on change type:
- **API/Contract changes**: API/Platform team
- **Config changes**: DevOps/Infrastructure team
- **Database/Migration**: Database/DBA team
- **Batch processing changes**: Data/ETL team
- **Authorization changes**: Security team
- **Documentation changes**: Technical writing team]

### 🚀 Deployment & Rollback Considerations
[Include only if applicable. Note any special deployment steps, feature flags, or rollback procedures.

**Format:**
- Feature flags: [if feature is behind a flag, specify flag name and default state]
- Migrations: [database migrations, data transformations needed]
- Rollback plan: [steps to safely rollback if issues occur]
- Deployment order: [if this PR depends on other PRs or services being deployed first]
- Environment requirements: [any new environment variables or infrastructure needed]

**Example:** "Feature is behind feature-flag: post-approval-user-mgmt. Requires database migration script migration-20250323-001.sql. Rollback: disable feature flag and revert API calls to legacy endpoint."]

### 🧾 Type of Change
[Check only the applicable boxes. Auto-populated based on conventional commit prefixes when detected. Select at least one.]
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] ✅ Tests added
- [ ] 🎨 Style change (formatting, renaming)
- [ ] ♻️ Refactor (no functional changes, no api changes)
- [ ] ⚡ Performance improvement
- [ ] 🏗️ Build/CI related changes
- [ ] 📦 Chore (release related changes)
- [ ] 🗄️ Database migration
- [ ] 🔐 Security enhancement
- [ ] 🔄 Dependency update

## Notes

- **Conventional commits**: If commits follow conventional commit format, the skill will auto-populate Type of Change checkboxes and include the type prefix in the PR title.
- **Commit message usage**: Extract semantic meaning from commit messages (between source and target branches) to populate the PR description. This provides context about intent and rationale. If messages are poor quality, rely on code diff analysis and domain knowledge.
- **File categorization**: Group files by project type patterns. The skill auto-detects project type from manifest files (pom.xml, package.json, go.mod, etc.).
- **When to omit sections**: If a PR only touches tests, omit "Core Implementation". If no config changes, omit "Configuration". A leaner PR description is often clearer than a padded one.
- **Handling large changesets**: For PRs with many files, focus on the "why" and high-level impact rather than line-by-line details.
- **Cross-service impacts**: If your project has defined service dependencies (via configuration or documentation), the skill will automatically check for impacts. Otherwise, you'll be prompted to specify relevant services.
- **Entity hierarchy changes**: If your project uses a multi-level entity hierarchy, flag these changes as high-impact, as they affect all downstream workflows.
- **Breaking change communication**: Be explicit about breaking changes. Poor communication here can cause production incidents. Always include migration path and deprecation timeline.
- **Project template merging**: If your repository has `.github/PULL_REQUEST_TEMPLATE.md`, the generated content will be merged with your project's required sections.
- **Draft PRs**: Use `--draft` flag or select draft option for work-in-progress that needs early review.
- **Next steps**: After generating the PR description, save and return `.pr-description.md` by default. Only provide/execute gh-based PR creation when explicitly requested.

## Error Handling Reference

| Error | Cause | Resolution |
|-------|-------|------------|
| "Detached HEAD state" | Not on a branch | Run `git checkout <branch-name>` |
| "Uncommitted changes" | Working tree is dirty | Commit or stash changes first |
| "No target branch found" | main/develop/master don't exist | Specify target branch manually |
| "Git diff failed" | Target branch not found | Fetch remote: `git fetch origin <branch>` |
| "Merge conflicts detected" | Source and target have conflicts | Resolve conflicts or note in PR |
| "gh CLI not found" | GitHub CLI not installed | Install from https://cli.github.com |
| "gh not authenticated" | Not logged into GitHub | Run `gh auth login` |
| "PR creation failed" | Various (permissions, network) | Check error message, retry |

## Example Workflow

**Scenario:** Feature branch `feature/JIRA-123-post-approval-user-mgmt` with changes to user management APIs.

**Step 1-3 Output:**
```
Source branch: feature/JIRA-123-post-approval-user-mgmt
Branch naming: ✓ Follows convention (feature/)
Ticket detected: JIRA-123
Upstream: ✓ Tracking origin/feature/JIRA-123-post-approval-user-mgmt
Target branch: main (detected, confirmed)
Merge conflicts: None detected
Uncommitted changes: None
```

**Step 4-5 Output:**
```
Files changed: 12 (8 source, 2 test, 1 config, 1 doc)
Commits: 3
  - feat: Add user product assignment endpoint
  - test: Add unit tests for UserProductService
  - docs: Update API documentation
Conventional commits: ✓ Detected (feat, test, docs)
Auto-populated types: ✨ New feature, ✅ Tests added, 📚 Documentation update
```

**Step 6-7 Output:**
```
Breaking changes: None detected
Cross-service impact: User Service (new endpoints), Auth Service (matrix update)
Suggested labels: enhancement, tests, documentation
```

**Step 10-11 Output:**
```
PR Description generated (2,847 characters)
Suggested labels: enhancement, tests, documentation
Recommended reviewers: @api-team, @security-team

Options:
1. Create PR now (gh pr create)
2. Create Draft PR (gh pr create --draft)
3. Create PR with labels and reviewers
4. Review locally first
5. Save to .pr-description.md
```

### Step 3: Present Output
1. Return actionable Markdown output aligned to this skill objective.
2. Include clear next actions and any required user decisions.

## Halt Conditions
- HALT if content is empty, unreadable, or missing required context.
- HALT if required evidence cannot be obtained from provided material.
- HALT if output would be speculative without explicit assumptions.
