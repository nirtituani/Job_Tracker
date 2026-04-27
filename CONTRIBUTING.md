# Contributing to Job Application Tracker

Thank you for your interest in contributing to the Job Application Tracker! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs. actual behavior
- Your operating system and Python version
- Any error messages or screenshots

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- How you envision it working
- Any examples from other apps (if applicable)

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Test thoroughly on your platform
5. Commit with clear messages (`git commit -m 'Add: Description of feature'`)
6. Push to your branch (`git push origin feature/YourFeature`)
7. Open a Pull Request

## 📝 Coding Guidelines

### Python Style
- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

### Database Changes
- Always include migration logic for existing databases
- Use `ALTER TABLE` for adding new columns
- Test with existing database files
- Document schema changes in comments

### UI Changes
- Maintain consistent spacing and layout
- Test on multiple screen sizes
- Ensure accessibility (keyboard navigation, etc.)
- Keep the interface clean and intuitive

### Testing
Before submitting:
- Test all CRUD operations (Create, Read, Update, Delete)
- Test with empty database
- Test with populated database
- Test edge cases (long text, special characters, etc.)
- Test on your target platform (Windows/macOS/Linux)

## 🔄 Development Workflow

1. **Set up your environment**
   ```bash
   git clone https://github.com/nirtituani/Job_Tracker.git
   cd Job_Tracker
   python3 job_tracker.py  # Test that it works
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Edit the code
   - Test thoroughly
   - Update documentation if needed

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub

## 🎯 Areas for Contribution

### High Priority
- Cross-platform testing and bug fixes
- Performance optimizations
- Accessibility improvements
- Documentation improvements

### Nice to Have
- Additional export formats (PDF, JSON)
- Data visualization (charts, graphs)
- Email integration for automated follow-ups
- Calendar integration for interview reminders
- Dark mode theme
- Custom themes/color schemes

### Future Ideas
- Cloud sync option (optional)
- Mobile companion app
- Browser extension for one-click application saving
- AI-powered resume suggestions

## 📋 Code Review Process

All contributions go through code review:
1. Automated checks (if any are set up)
2. Manual review by project maintainer
3. Testing on different platforms
4. Feedback and requested changes
5. Approval and merge

## 🐛 Bug Triage

Bugs are labeled by priority:
- **Critical**: App crashes, data loss
- **High**: Major features broken
- **Medium**: Minor features broken, workaround exists
- **Low**: Cosmetic issues, minor inconveniences

## 💬 Communication

- Use GitHub Issues for bug reports and feature requests
- Be respectful and constructive
- Provide context and details
- Follow up on your issues/PRs

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md (Contributors section)
- Release notes for significant contributions
- Git history (your commits stay attributed to you)

---

Thank you for helping make Job Application Tracker better! 🚀
