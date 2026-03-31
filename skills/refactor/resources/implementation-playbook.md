# Refactor Implementation Playbook

This file provides the detailed decision rules and examples behind the `refactor` skill.

## Core Principle

Refactor for the current codebase, not for an imagined ideal architecture. Prefer the smallest behavior-preserving change that makes the next change safer.

## External Reference

- [Refactoring.Guru: Refactoring](https://refactoring.guru/refactoring) for a broad catalog of code smells, refactoring techniques, and the step-by-step refactoring mindset. For medium- and high-complexity refactors, review this reference as part of planning. Use it to strengthen refactoring choices, not to override repository-specific conventions.

## 1. Start with Codebase Adaptation

Before proposing changes:

1. Identify the active language and framework.
2. Identify module structure and ownership boundaries.
3. Identify existing testing and validation commands.
4. Identify already-used patterns for dependency injection, validation, mapping, error handling, logging, and transactions.
5. Prefer matching those patterns over introducing new ones.

Questions to answer first:

- Is this a layered service, feature-based package layout, or mixed legacy structure?
- Where does this repo currently place business logic?
- Are DTOs, entities, mappers, and repositories separated already?
- Which tests exist around the area being changed?
- Which lint, format, and build checks are actually used here?

## 2. Refactoring Priorities

Prioritize in this order:

### High value, low-risk

- Remove dead code
- Rename unclear symbols
- Extract magic numbers or duplicated literals
- Flatten trivial conditionals
- Extract obviously duplicated private logic

### Medium risk, high value

- Break large methods into cohesive private methods
- Extract helper classes or collaborators
- Split mixed orchestration and business rules
- Untangle mapping and validation duplication

### Higher risk

- Moving responsibilities across layers
- Changing transaction boundaries
- Replacing shared abstractions
- Reorganizing public package structure

Do higher-risk refactors only when the codebase already points that way or the user asks for it.

## 3. Java and Spring Boot Refactoring Heuristics

When working in Java or Spring Boot, inspect for these first:

### Controllers

Good signals:

- Thin request handling
- Validation delegated through existing patterns
- Service orchestration only
- DTO-focused web layer

Refactor targets:

- Business logic inside controllers
- Repository calls directly from controllers
- Manual response construction duplicated across endpoints
- Repeated exception translation logic that should follow existing advice/handler patterns

### Services

Good signals:

- Clear orchestration or business-rule ownership
- Focused transaction boundaries
- Dependencies injected through constructors

Refactor targets:

- God services with unrelated responsibilities
- Large methods mixing validation, mapping, persistence, and side effects
- Duplicated branching across service methods
- Hidden side effects or implicit workflow ordering

### Repositories and Persistence

Good signals:

- Persistence-focused methods
- Query logic isolated to repository or persistence adapter layers already used by the repo

Refactor targets:

- Business logic in repositories
- Duplicated query fragments
- Overly broad repository interfaces
- Leaky persistence concerns scattered into services

### DTOs, Entities, and Mapping

Good signals:

- Stable boundary between API payloads and persistence/domain models
- Existing mapper pattern used consistently

Refactor targets:

- Entity exposure through controllers where the repo already uses DTOs
- Repeated manual mapping blocks
- Validation annotations placed inconsistently with repo patterns

### Dependency Injection

Prefer:

- Constructor injection
- Final dependencies where consistent with the repo

Avoid:

- Introducing field injection into constructor-injected codebases
- Adding service locators or static access patterns unless legacy code forces it

### Transactions

Preserve:

- Existing `@Transactional` semantics
- Read-only transaction intent
- Existing retry or locking behavior

Be careful with:

- Moving writes outside transaction scope
- Expanding transaction boundaries around remote calls
- Refactors that change lazy-loading behavior

## 4. Spring Test Strategy During Refactoring

Use the narrowest test layer that proves behavior:

- Pure business logic: JUnit + Mockito
- MVC/API behavior: `@WebMvcTest` or existing controller test style
- JPA/query behavior: `@DataJpaTest`
- Full wiring only when needed: existing `@SpringBootTest` patterns

During refactoring:

1. Preserve existing tests where possible.
2. Add focused tests around risky seams before larger extractions.
3. Avoid replacing narrow tests with heavier tests unless necessary.

## 5. Behavior-Preserving Refactor Patterns

### Extract orchestration from a large service method

```java
public OrderResult placeOrder(CreateOrderRequest request) {
    validateRequest(request);
    Customer customer = customerRepository.findById(request.customerId())
        .orElseThrow(() -> new NotFoundException("Customer not found"));

    Order order = orderMapper.toEntity(request, customer);
    applyPricing(order);
    persistOrder(order);
    publishOrderCreated(order);
    return orderMapper.toResult(order);
}
```

After:

```java
public OrderResult placeOrder(CreateOrderRequest request) {
    validateRequest(request);
    Customer customer = loadCustomer(request.customerId());
    Order order = createOrder(request, customer);
    finalizeOrder(order);
    return orderMapper.toResult(order);
}

private Customer loadCustomer(UUID customerId) {
    return customerRepository.findById(customerId)
        .orElseThrow(() -> new NotFoundException("Customer not found"));
}

private Order createOrder(CreateOrderRequest request, Customer customer) {
    return orderMapper.toEntity(request, customer);
}

private void finalizeOrder(Order order) {
    applyPricing(order);
    persistOrder(order);
    publishOrderCreated(order);
}
```

### Extract duplicated mapping

Before:

```java
UserSummaryDto dto = new UserSummaryDto();
dto.setId(user.getId());
dto.setName(user.getName());
dto.setEmail(user.getEmail());
```

After:

```java
private UserSummaryDto toSummary(User user) {
    UserSummaryDto dto = new UserSummaryDto();
    dto.setId(user.getId());
    dto.setName(user.getName());
    dto.setEmail(user.getEmail());
    return dto;
}
```

Only extract to a dedicated mapper if the repo already uses mappers or the duplication is repeated enough to justify it.

### Replace field injection with constructor injection

Before:

```java
@Service
public class BillingService {

    @Autowired
    private InvoiceRepository invoiceRepository;
}
```

After:

```java
@Service
public class BillingService {

    private final InvoiceRepository invoiceRepository;

    public BillingService(InvoiceRepository invoiceRepository) {
        this.invoiceRepository = invoiceRepository;
    }
}
```

## 6. Smells to Watch For

### Generic

- Methods too large to name clearly
- Classes with multiple unrelated reasons to change
- Repeated conditional branches across files
- Helper classes that became dumping grounds
- Public APIs leaking internal implementation details

### Java/Spring Boot specific

- Controller doing validation, mapping, persistence, and business decisions
- Service returning web-specific response objects in a layered codebase
- Repository methods with business policy branching
- Broad `catch (Exception)` blocks
- Transactional annotations applied inconsistently
- Excessive static utility use in otherwise injected code
- Test classes that verify too much through full app context when a slice test exists

## 7. Safety Rules

- Preserve API contracts unless explicitly told otherwise.
- Preserve serialized field names and response shapes.
- Preserve database write semantics and transaction boundaries.
- Preserve security and authorization checks.
- Avoid package moves that create unnecessary churn unless the refactor requires them.
- Prefer staged refactors over big-bang rewrites.

## 8. Verification

Before declaring success:

1. Run the repo-native tests for the changed area first.
2. Run the repo-native validation commands for formatting, linting, and type/build checks if they exist.
3. Re-check that no unintended contract or schema changes were introduced.

Typical Java/Spring Boot examples:

- `./mvnw test`
- `./mvnw -pl <module> test`
- `./gradlew test`
- `./mvnw verify` or `./gradlew check` when that is the repo's normal gate

## 9. Escalation Conditions

Stop and call out risk when the refactor affects:

- Auth or permission enforcement
- Billing or financial calculations
- Shared API contracts
- Persistence schemas or migrations
- Cross-service event payloads
- Compliance-sensitive data handling
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    address: Address;
}

interface Address {
    street: string;
    city: string;
    state: string;
    zipCode: string;
}

function createUser(userData: UserData) {}

// SMELL: Feature Envy (method uses another class's data more than its own)
// BEFORE
class Order {
    calculateShipping(customer: Customer): number {
        if (customer.isPremium) {
            return customer.address.isInternational ? 0 : 5;
        }
        return customer.address.isInternational ? 20 : 10;
    }
}

// AFTER: Move method to the class it envies
class Customer {
    calculateShippingCost(): number {
        if (this.isPremium) {
            return this.address.isInternational ? 0 : 5;
        }
        return this.address.isInternational ? 20 : 10;
    }
}

class Order {
    calculateShipping(customer: Customer): number {
        return customer.calculateShippingCost();
    }
}

// SMELL: Primitive Obsession
// BEFORE
function validateEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

let userEmail: string = "test@example.com";

// AFTER: Value Object
class Email {
    private readonly value: string;

    constructor(email: string) {
        if (!this.isValid(email)) {
            throw new Error("Invalid email format");
        }
        this.value = email;
    }

    private isValid(email: string): boolean {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    toString(): string {
        return this.value;
    }
}

let userEmail = new Email("test@example.com"); // Validation automatic
```

### 5. Decision Frameworks

**Code Quality Metrics Interpretation Matrix**

| Metric | Good | Warning | Critical | Action |
|--------|------|---------|----------|--------|
| Cyclomatic Complexity | <10 | 10-15 | >15 | Split into smaller methods |
| Method Lines | <20 | 20-50 | >50 | Extract methods, apply SRP |
| Class Lines | <200 | 200-500 | >500 | Decompose into multiple classes |
| Test Coverage | >80% | 60-80% | <60% | Add unit tests immediately |
| Code Duplication | <3% | 3-5% | >5% | Extract common code |
| Comment Ratio | 10-30% | <10% or >50% | N/A | Improve naming or reduce noise |
| Dependency Count | <5 | 5-10 | >10 | Apply DIP, use facades |

**Refactoring ROI Analysis**

```
Priority = (Business Value × Technical Debt) / (Effort × Risk)

Business Value (1-10):
- Critical path code: 10
- Frequently changed: 8
- User-facing features: 7
- Internal tools: 5
- Legacy unused: 2

Technical Debt (1-10):
- Causes production bugs: 10
- Blocks new features: 8
- Hard to test: 6
- Style issues only: 2

Effort (hours):
- Rename variables: 1-2
- Extract methods: 2-4
- Refactor class: 4-8
- Architecture change: 40+

Risk (1-10):
- No tests, high coupling: 10
- Some tests, medium coupling: 5
- Full tests, loose coupling: 2
```

**Technical Debt Prioritization Decision Tree**

```
Is it causing production bugs?
├─ YES → Priority: CRITICAL (Fix immediately)
└─ NO → Is it blocking new features?
    ├─ YES → Priority: HIGH (Schedule this sprint)
    └─ NO → Is it frequently modified?
        ├─ YES → Priority: MEDIUM (Next quarter)
        └─ NO → Is code coverage < 60%?
            ├─ YES → Priority: MEDIUM (Add tests)
            └─ NO → Priority: LOW (Backlog)
```

### 6. Modern Code Quality Practices (2024-2025)

**AI-Assisted Code Review Integration**

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # GitHub Copilot Autofix
      - uses: github/copilot-autofix@v1
        with:
          languages: 'python,typescript,go'

      # CodeRabbit AI Review
      - uses: coderabbitai/action@v1
        with:
          review_type: 'comprehensive'
          focus: 'security,performance,maintainability'

      # Codium AI PR-Agent
      - uses: codiumai/pr-agent@v1
        with:
          commands: '/review --pr_reviewer.num_code_suggestions=5'
```

**Static Analysis Toolchain**

```python
# pyproject.toml
[tool.ruff]
line-length = 100
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C90", # mccabe complexity
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "A",   # flake8-builtins
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "RET", # flake8-return
]

[tool.mypy]
strict = true
warn_unreachable = true
warn_unused_ignores = true

[tool.coverage]
fail_under = 80
```

```javascript
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended-type-checked",
    "plugin:sonarjs/recommended",
    "plugin:security/recommended"
  ],
  "plugins": ["sonarjs", "security", "no-loops"],
  "rules": {
    "complexity": ["error", 10],
    "max-lines-per-function": ["error", 20],
    "max-params": ["error", 3],
    "no-loops/no-loops": "warn",
    "sonarjs/cognitive-complexity": ["error", 15]
  }
}
```

**Automated Refactoring Suggestions**

```python
# Use Sourcery for automatic refactoring suggestions
# sourcery.yaml
rules:
  - id: convert-to-list-comprehension
  - id: merge-duplicate-blocks
  - id: use-named-expression
  - id: inline-immediately-returned-variable

# Example: Sourcery will suggest
# BEFORE
result = []
for item in items:
    if item.is_active:
        result.append(item.name)

# AFTER (auto-suggested)
result = [item.name for item in items if item.is_active]
```

**Code Quality Dashboard Configuration**

```yaml
# sonar-project.properties
sonar.projectKey=my-project
sonar.sources=src
sonar.tests=tests
sonar.coverage.exclusions=**/*_test.py,**/test_*.py
sonar.python.coverage.reportPaths=coverage.xml

# Quality Gates
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300

# Thresholds
sonar.coverage.threshold=80
sonar.duplications.threshold=3
sonar.maintainability.rating=A
sonar.reliability.rating=A
sonar.security.rating=A
```

**Security-Focused Refactoring**

```python
# Use Semgrep for security-aware refactoring
# .semgrep.yml
rules:
  - id: sql-injection-risk
    pattern: execute($QUERY)
    message: Potential SQL injection
    severity: ERROR
    fix: Use parameterized queries

  - id: hardcoded-secrets
    pattern: password = "..."
    message: Hardcoded password detected
    severity: ERROR
    fix: Use environment variables or secret manager

# CodeQL security analysis
# .github/workflows/codeql.yml
- uses: github/codeql-action/analyze@v3
  with:
    category: "/language:python"
    queries: security-extended,security-and-quality
```

### 7. Refactored Implementation

Provide the complete refactored code with:

**Clean Code Principles**
- Meaningful names (searchable, pronounceable, no abbreviations)
- Functions do one thing well
- No side effects
- Consistent abstraction levels
- DRY (Don't Repeat Yourself)
- YAGNI (You Aren't Gonna Need It)

**Error Handling**
```python
# Use specific exceptions
class OrderValidationError(Exception):
    pass

class InsufficientInventoryError(Exception):
    pass

# Fail fast with clear messages
def validate_order(order):
    if not order.items:
        raise OrderValidationError("Order must contain at least one item")

    for item in order.items:
        if item.quantity <= 0:
            raise OrderValidationError(f"Invalid quantity for {item.name}")
```

**Documentation**
```python
def calculate_discount(order: Order, customer: Customer) -> Decimal:
    """
    Calculate the total discount for an order based on customer tier and order value.

    Args:
        order: The order to calculate discount for
        customer: The customer making the order

    Returns:
        The discount amount as a Decimal

    Raises:
        ValueError: If order total is negative
    """
```

### 8. Testing Strategy

Generate comprehensive tests for the refactored code:

**Unit Tests**
```python
class TestOrderProcessor:
    def test_validate_order_empty_items(self):
        order = Order(items=[])
        with pytest.raises(OrderValidationError):
            validate_order(order)

    def test_calculate_discount_vip_customer(self):
        order = create_test_order(total=1000)
        customer = Customer(tier="VIP")
        discount = calculate_discount(order, customer)
        assert discount == Decimal("100.00")  # 10% VIP discount
```

**Test Coverage**
- All public methods tested
- Edge cases covered
- Error conditions verified
- Performance benchmarks included

### 9. Before/After Comparison

Provide clear comparisons showing improvements:

**Metrics**
- Cyclomatic complexity reduction
- Lines of code per method
- Test coverage increase
- Performance improvements

**Example**
```
Before:
- processData(): 150 lines, complexity: 25
- 0% test coverage
- 3 responsibilities mixed

After:
- validateInput(): 20 lines, complexity: 4
- transformData(): 25 lines, complexity: 5
- saveResults(): 15 lines, complexity: 3
- 95% test coverage
- Clear separation of concerns
```

### 10. Migration Guide

If breaking changes are introduced:

**Step-by-Step Migration**
1. Install new dependencies
2. Update import statements
3. Replace deprecated methods
4. Run migration scripts
5. Execute test suite

**Backward Compatibility**
```python
# Temporary adapter for smooth migration
class LegacyOrderProcessor:
    def __init__(self):
        self.processor = OrderProcessor()

    def process(self, order_data):
        # Convert legacy format
        order = Order.from_legacy(order_data)
        return self.processor.process(order)
```

### 11. Performance Optimizations

Include specific optimizations:

**Algorithm Improvements**
```python
# Before: O(n²)
for item in items:
    for other in items:
        if item.id == other.id:
            # process

# After: O(n)
item_map = {item.id: item for item in items}
for item_id, item in item_map.items():
    # process
```

**Caching Strategy**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_expensive_metric(data_id: str) -> float:
    # Expensive calculation cached
    return result
```

### 12. Code Quality Checklist

Ensure the refactored code meets these criteria:

- [ ] All methods < 20 lines
- [ ] All classes < 200 lines
- [ ] No method has > 3 parameters
- [ ] Cyclomatic complexity < 10
- [ ] No nested loops > 2 levels
- [ ] All names are descriptive
- [ ] No commented-out code
- [ ] Consistent formatting
- [ ] Type hints added (Python/TypeScript)
- [ ] Error handling comprehensive
- [ ] Logging added for debugging
- [ ] Performance metrics included
- [ ] Documentation complete
- [ ] Tests achieve > 80% coverage
- [ ] No security vulnerabilities
- [ ] AI code review passed
- [ ] Static analysis clean (SonarQube/CodeQL)
- [ ] No hardcoded secrets

## Severity Levels

Rate issues found and improvements made:

**Critical**: Security vulnerabilities, data corruption risks, memory leaks
**High**: Performance bottlenecks, maintainability blockers, missing tests
**Medium**: Code smells, minor performance issues, incomplete documentation
**Low**: Style inconsistencies, minor naming issues, nice-to-have features

## Output Format

1. **Analysis Summary**: Key issues found and their impact
2. **Refactoring Plan**: Prioritized list of changes with effort estimates
3. **Refactored Code**: Complete implementation with inline comments explaining changes
4. **Test Suite**: Comprehensive tests for all refactored components
5. **Migration Guide**: Step-by-step instructions for adopting changes
6. **Metrics Report**: Before/after comparison of code quality metrics
7. **AI Review Results**: Summary of automated code review findings
8. **Quality Dashboard**: Link to SonarQube/CodeQL results

Focus on delivering practical, incremental improvements that can be adopted immediately while maintaining system stability.
