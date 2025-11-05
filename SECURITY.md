# Security Policy

## Supported Versions

This project requires Django 4.2.26 or later to protect against known security vulnerabilities.

| Django Version | Supported          |
| -------------- | ------------------ |
| 5.2.8+         | :white_check_mark: |
| 5.1.14+        | :white_check_mark: |
| 4.2.26+        | :white_check_mark: |
| < 4.2.26       | :x:                |

## Security Vulnerabilities

### CVE-2024-XXXXX: SQL Injection via _connector argument

**Description:** Django versions before 5.1.14, 4.2.26, and 5.2.8 are vulnerable to SQL injection when using QuerySet methods (`filter()`, `exclude()`, `get()`) or the `Q()` class with a suitably crafted dictionary using dictionary expansion as the `_connector` argument.

**Impact:** This vulnerability could allow attackers to execute arbitrary SQL queries if user-controlled dictionaries are unpacked into QuerySet methods.

**Mitigation:** 
- Update Django to version 4.2.26 or later (LTS), 5.1.14+ or 5.2.8+
- Never unpack user-controlled dictionaries directly into QuerySet methods
- Always validate and sanitize filter parameters before use
- Avoid patterns like: `Model.objects.filter(**user_input)`

**Example of vulnerable code:**
```python
# VULNERABLE - Do not do this!
def get_items(request):
    filters = request.POST.get('filters')  # User-controlled input
    filters_dict = json.loads(filters)
    items = Item.objects.filter(**filters_dict)  # SQL injection risk
    return items
```

**Example of safe code:**
```python
# SAFE - Validate and whitelist parameters
def get_items(request):
    allowed_filters = {}
    if request.POST.get('name'):
        allowed_filters['name'] = request.POST.get('name')
    if request.POST.get('value'):
        allowed_filters['value'] = request.POST.get('value')
    items = Item.objects.filter(**allowed_filters)
    return items
```

**Credits:** Django would like to thank cyberstan for reporting this issue.

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by emailing the maintainers directly rather than opening a public issue. Please include:

1. A description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

We will respond to security reports within 48 hours and work to release a fix as quickly as possible.
