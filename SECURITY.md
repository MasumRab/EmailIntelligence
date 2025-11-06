# Security Policy

## Supported Versions

We actively support and patch security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| scientific | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in EmailIntelligence, please help us by reporting it responsibly.

### How to Report

1. **Do not** create public GitHub issues for security vulnerabilities
2. Email security concerns to: [security@masumrab.com](mailto:security@masumrab.com)
3. Include detailed information about:
   - The vulnerability
   - Steps to reproduce
   - Potential impact
   - Your contact information for follow-up

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Investigation**: We'll investigate and validate the report
- **Updates**: We'll provide regular updates on our progress
- **Resolution**: We'll work to resolve valid vulnerabilities quickly
- **Disclosure**: We'll coordinate disclosure timing with you

## Security Best Practices

### For Users
- Always use environment variables for sensitive configuration
- Regularly update dependencies
- Use strong, unique passwords
- Enable MFA when available
- Keep backups of important data

### For Contributors
- Run security scans before committing
- Never commit secrets or sensitive data
- Use secure coding practices
- Review dependency licenses
- Follow the principle of least privilege

## Known Security Features

- Argon2 password hashing (not SHA256)
- Environment-based secret management
- Input validation and sanitization
- Secure subprocess execution
- JWT token authentication
- CORS protection
- Security headers middleware

## Security Updates

Security updates will be released as soon as possible after verification. Critical security fixes may result in immediate patch releases.

## Contact

For security-related questions or concerns:
- Email: [security@masumrab.com](mailto:security@masumrab.com)
- Project Issues: [GitHub Issues](https://github.com/MasumRab/EmailIntelligence/issues)

Thank you for helping keep EmailIntelligence secure! 🔒
