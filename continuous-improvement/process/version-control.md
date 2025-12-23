# Version Control and Fork Management

## Overview
Guidelines for version control, branching, and fork management to support continuous improvement and experimentation.

## Branching Strategy

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Requires review and passing tests
- **Merges From**: `develop`, hotfix branches
- **Stability**: Always stable and deployable

#### `develop`
- **Purpose**: Integration branch for next release
- **Protection**: Requires review
- **Merges From**: Feature, improvement, bugfix branches
- **Stability**: Mostly stable, may have minor issues

### Supporting Branches

#### Feature Branches
- **Naming**: `feature/[feature-name]`
- **Purpose**: New features or capabilities
- **Lifetime**: Created from develop, merged back to develop
- **Example**: `feature/ml-decision-support`

#### Improvement Branches
- **Naming**: `improvement/[improvement-name]`
- **Purpose**: Enhancements to existing features
- **Lifetime**: Created from develop, merged back to develop
- **Example**: `improvement/protocol-performance`

#### Bugfix Branches
- **Naming**: `bugfix/[bug-id]-[short-description]`
- **Purpose**: Non-critical bug fixes
- **Lifetime**: Created from develop, merged back to develop
- **Example**: `bugfix/AUTO-2025-042-validation-error`

#### Hotfix Branches
- **Naming**: `hotfix/[version]-[issue]`
- **Purpose**: Critical production bug fixes
- **Lifetime**: Created from main, merged to both main and develop
- **Example**: `hotfix/1.2.1-critical-security-fix`

#### Experimental Branches
- **Naming**: `experimental/[experiment-name]`
- **Purpose**: Proof of concepts, risky innovations
- **Lifetime**: Created from develop, may or may not be merged
- **Example**: `experimental/quantum-consensus`

#### Research Branches
- **Naming**: `research/[research-topic]`
- **Purpose**: Research and exploration work
- **Lifetime**: Created from develop, results documented, may be merged
- **Example**: `research/new-protocol-design`

## Fork Management

### When to Create a Fork

#### Repository Fork
- Experimenting with major architecture changes
- External contribution workflow
- Creating derivative work
- Long-term experimentation

#### Branch Fork (Preferred for Internal Work)
- Protocol revisions
- Feature development
- Bug fixes
- Improvements

### Fork Naming Conventions

For external repository forks:
- `[username]/iNFINITE-Ai-2025-Council-Simulator`
- Keep upstream as remote: `upstream`

For internal branches (preferred):
- Follow branching strategy naming

### Fork Lifecycle

#### 1. Creation
```bash
# Create branch fork
git checkout develop
git pull origin develop
git checkout -b improvement/protocol-v2

# Or create repository fork (external contributors)
# Fork via GitHub UI, then clone
```

#### 2. Development
```bash
# Make regular commits
git add .
git commit -m "Clear commit message"
git push origin improvement/protocol-v2

# Keep updated with develop
git fetch origin
git merge origin/develop
# Or rebase if history is clean
git rebase origin/develop
```

#### 3. Testing and Validation
```bash
# Run all tests
npm test  # or appropriate test command

# Run linters
npm run lint

# Validate documentation
# Check that all tests pass
```

#### 4. Review and Merge
```bash
# Create pull request via GitHub
# Address review feedback
# Ensure CI passes
# Merge when approved
```

#### 5. Cleanup
```bash
# After merge, delete branch
git checkout develop
git pull origin develop
git branch -d improvement/protocol-v2
git push origin --delete improvement/protocol-v2
```

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Maintenance tasks

### Examples
```
feat(protocol): Add weighted voting consensus

Implements weighted voting mechanism where council members
have different vote weights based on expertise and history.

Closes #123
```

```
fix(validation): Prevent null pointer in data validator

Added null check before accessing validation rules.
Includes test case for null input scenario.

Fixes #456
```

### Best Practices
- Keep commits atomic (one logical change)
- Write clear, descriptive messages
- Reference issue numbers
- Use present tense
- Keep subject line under 50 characters
- Wrap body at 72 characters

## Pull Request Process

### Creating a Pull Request

1. **Prepare**
   - Ensure all tests pass
   - Update documentation
   - Rebase on target branch if needed
   - Self-review changes

2. **Create PR**
   - Use descriptive title
   - Fill out PR template
   - Link related issues
   - Add appropriate labels
   - Request reviewers

3. **PR Description Template**
```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Improvement
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance testing (if applicable)

## Checklist
- [ ] Code follows project standards
- [ ] Documentation updated
- [ ] All tests passing
- [ ] No regressions introduced
- [ ] Reviewers assigned

## Related Issues
Fixes #[issue number]
Relates to #[issue number]

## Screenshots (if applicable)
[Add screenshots]
```

### Reviewing a Pull Request

1. **Initial Check**
   - Verify CI passes
   - Check PR description
   - Understand the change

2. **Code Review**
   - Review code quality
   - Check for issues
   - Verify tests
   - Validate documentation

3. **Testing**
   - Checkout branch locally
   - Run tests
   - Manual testing if needed
   - Performance validation

4. **Feedback**
   - Provide constructive comments
   - Suggest improvements
   - Approve or request changes
   - Be respectful and helpful

### Merging Strategy

#### Squash and Merge (Preferred for Features)
- Combines all commits into one
- Clean main branch history
- Use for feature branches

#### Merge Commit (For Long-lived Branches)
- Preserves all commits
- Clear merge history
- Use for develop → main

#### Rebase and Merge (For Clean History)
- Linear history
- Individual commits preserved
- Use for small, clean changes

## Version Tagging

### Semantic Versioning
Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Tagging Process
```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release version 1.2.0"

# Push tag
git push origin v1.2.0

# List tags
git tag -l
```

### Release Notes
For each version, document:
- New features
- Improvements
- Bug fixes
- Breaking changes
- Migration guide (if needed)

## Conflict Resolution

### Preventing Conflicts
- Pull frequently from main/develop
- Communicate with team
- Keep branches short-lived
- Make focused changes

### Resolving Conflicts
```bash
# Update local branch
git fetch origin
git merge origin/develop

# Resolve conflicts in editor
# Test after resolution
git add .
git commit -m "Resolve merge conflicts"
git push
```

### Escalation
If conflicts are complex:
1. Discuss with team
2. Pair on resolution
3. Get help from original authors
4. Document resolution approach

## Repository Maintenance

### Regular Tasks

#### Daily
- Review open PRs
- Address urgent issues
- Monitor CI/CD

#### Weekly
- Clean up merged branches
- Review open issues
- Update documentation

#### Monthly
- Archive old branches
- Review repository health
- Update dependencies
- Assess repository metrics

### Repository Health Metrics
- Open PR age
- CI success rate
- Code review velocity
- Branch count
- Issue resolution time

## Best Practices

### Do's
- ✓ Keep branches up to date
- ✓ Write clear commit messages
- ✓ Create focused PRs
- ✓ Review code thoroughly
- ✓ Test before merging
- ✓ Document changes
- ✓ Communicate with team

### Don'ts
- ✗ Commit secrets or credentials
- ✗ Push directly to main
- ✗ Create huge PRs
- ✗ Ignore CI failures
- ✗ Skip code review
- ✗ Leave branches stale
- ✗ Force push to shared branches

## Tools and Automation

### Git Hooks
- Pre-commit: Lint and format
- Pre-push: Run tests
- Commit-msg: Validate format

### CI/CD Integration
- Automated testing
- Code quality checks
- Security scanning
- Deployment automation

### GitHub Features
- Protected branches
- Required reviews
- Status checks
- Auto-merge
- Branch protection rules

## Training and Support

### Resources
- Git documentation
- Team wiki
- Training sessions
- Pair programming
- Code review guidelines

### Getting Help
- Ask team members
- Review documentation
- Search similar issues
- Escalate if needed

## Continuous Improvement

### Process Reviews
- Quarterly workflow assessment
- Team feedback collection
- Metrics analysis
- Process refinement

### Adaptations
- Update guidelines as needed
- Adopt better practices
- Improve automation
- Enhance documentation

## Conclusion
Effective version control and fork management enable safe experimentation, collaborative development, and continuous improvement. By following these guidelines, we maintain code quality while moving quickly.
