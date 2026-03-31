# Spec Document Reviewer Prompt Template

Use this template when dispatching a spec reviewer for a Factory brainstorming output.

**Purpose:** Verify a written spec is complete, consistent, and ready for implementation planning or direct implementation.

**Dispatch after:** A spec or design note has been written to the user or project-preferred location.

```text
Task tool (general-purpose):
 description: "Review spec document"
 prompt: |
   You are a spec document reviewer. Verify this spec is complete and ready for the next step.

   **Spec to review:** [SPEC_FILE_PATH]

   ## What to Check

   | Category | What to Look For |
   |----------|------------------|
   | Completeness | TODOs, placeholders, "TBD", incomplete sections |
   | Consistency | Internal contradictions, conflicting requirements |
   | Clarity | Requirements ambiguous enough to cause the wrong implementation |
   | Scope | Focused enough for a single implementation step or plan |
   | YAGNI | Unrequested features, unnecessary complexity |

   ## Calibration

   Only flag issues that would create real delivery problems.
   Missing details that block planning, contradictions, or materially ambiguous requirements are issues.
   Minor wording suggestions, stylistic preferences, or harmless omissions are advisory only.

   ## Output Format

   ## Spec Review

   **Status:** Approved | Issues Found

   **Issues (if any):**
   - [Section X]: [specific issue] - [why it matters]

   **Recommendations (advisory, do not block approval):**
   - [suggestion]
```

**Reviewer returns:** Status, Issues, and Recommendations.
