# Secure Coding

**Write code that doesn't make the OWASP Top 10 list.**

Security vulnerabilities in LLM-generated code are a real and growing problem. This skill trains reviewers and coders to catch the most common issues before they ship: SQL injection, secrets in code, missing auth checks, unsafe deserialization, and more.

---

## The OWASP Top 10 (Local AI Focus)

The OWASP Top 10 is the industry-standard list of the most critical web application security risks. Every developer should be able to recognize and fix each category.

### A01 — Broken Access Control
**What it is:** Users can access resources or perform actions they shouldn't.

```python
# VULNERABLE: Any user can delete any post
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, user_id: int):
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))

# SECURE: Verify ownership before deleting
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(get_current_user)):
    post = db.get_post(post_id)
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete_post(post_id)
```

**Checklist:**
- [ ] Verify ownership on every write operation
- [ ] Check permissions on every read of sensitive data
- [ ] Never trust user-supplied IDs without ownership verification

---

### A02 — Cryptographic Failures
**What it is:** Weak or missing encryption of sensitive data.

```python
# VULNERABLE: Storing plaintext passwords
user.password = password

# VULNERABLE: Using MD5 or SHA1 for passwords
import hashlib
user.password = hashlib.md5(password.encode()).hexdigest()

# SECURE: Use bcrypt or argon2
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user.password_hash = pwd_context.hash(password)

# Verify
pwd_context.verify(plain_password, stored_hash)
```

**Checklist:**
- [ ] Never store plaintext passwords
- [ ] Use bcrypt, argon2, or scrypt for password hashing
- [ ] Use HTTPS for all data in transit
- [ ] Don't use MD5 or SHA1 for security-sensitive hashing

---

### A03 — Injection (SQL, Command, LDAP)
**What it is:** Attacker-controlled input is interpreted as code/commands.

```python
# VULNERABLE: String formatting in SQL
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# SECURE: Parameterized queries
def get_user(username: str):
    return db.execute("SELECT * FROM users WHERE username = ?", (username,))

# VULNERABLE: Shell injection
import subprocess
def run_tool(filename):
    subprocess.run(f"process {filename}", shell=True)

# SECURE: No shell, explicit arg list
def run_tool(filename: str):
    subprocess.run(["process", filename], shell=False)
```

**Checklist:**
- [ ] Never concatenate user input into SQL queries
- [ ] Use parameterized queries or ORM
- [ ] Never use `shell=True` with user-controlled input
- [ ] Validate and sanitize all input at system boundaries

---

### A04 — Insecure Design
**What it is:** Missing security controls in the architecture itself.

```python
# VULNERABLE: Rate limiting not implemented
@app.post("/login")
def login(username: str, password: str):
    user = authenticate(username, password)
    return {"token": create_token(user)}

# SECURE: Rate limit login attempts
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
def login(request: Request, username: str, password: str):
    user = authenticate(username, password)
    return {"token": create_token(user)}
```

**Checklist:**
- [ ] Rate limit authentication endpoints
- [ ] Limit failed login attempts (lockout or delay)
- [ ] Don't expose stack traces to end users
- [ ] Log security-relevant events (failed logins, access denied)

---

### A05 — Security Misconfiguration
**What it is:** Default settings, exposed admin interfaces, overly permissive CORS.

```python
# VULNERABLE: Allow all origins (CORS wildcard)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# SECURE: Explicit allowlist
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Checklist:**
- [ ] No default credentials in production
- [ ] No `DEBUG=True` in production
- [ ] No wildcard CORS unless genuinely needed
- [ ] No exposed admin endpoints without auth
- [ ] Environment variables, not hardcoded secrets

---

### A06 — Vulnerable Components
**What it is:** Using outdated libraries with known CVEs.

```bash
# Check for known vulnerabilities in Python dependencies
pip install pip-audit
pip-audit

# Or with safety
pip install safety
safety check
```

**Checklist:**
- [ ] Regularly run `pip-audit` or `safety check`
- [ ] Pin dependency versions in production
- [ ] Review changelogs when upgrading
- [ ] Remove unused dependencies

---

### A07 — Authentication Failures
**What it is:** Weak session management, no token expiry, predictable tokens.

```python
# VULNERABLE: Long-lived or never-expiring JWT
token = jwt.encode({"user_id": 1}, SECRET, algorithm="HS256")

# SECURE: Short expiry + refresh token pattern
from datetime import datetime, timedelta, timezone
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Checklist:**
- [ ] JWT access tokens expire in 15–60 minutes
- [ ] Use refresh tokens for long sessions
- [ ] Validate `exp`, `iat`, and `iss` claims on every request
- [ ] Use a strong, randomly generated `SECRET_KEY`
- [ ] Never put `SECRET_KEY` in source code

---

### A08 — Secrets in Code
**What it is:** API keys, passwords, and tokens committed to version control.

```python
# VULNERABLE: Hardcoded secret
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "hunter2"

# SECURE: Load from environment
import os
API_KEY = os.environ["OPENAI_API_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
```

```bash
# .gitignore — always include
.env
*.pem
secrets/
```

**Checklist:**
- [ ] No API keys, passwords, or tokens in source code
- [ ] Use `.env` files locally (never commit them)
- [ ] Use environment variables or a secrets manager in production
- [ ] Scan commits with `git-secrets` or `gitleaks`

---

### A09 — Logging & Monitoring Failures
**What it is:** No audit trail, secrets logged, insufficient alerting.

```python
# VULNERABLE: Logging sensitive data
logger.info(f"User login: {username} password={password}")

# SECURE: Log only non-sensitive context
logger.info(f"Login attempt: username={username} success={success} ip={ip}")
```

**Checklist:**
- [ ] Never log passwords, tokens, or PII
- [ ] Log authentication events (success and failure)
- [ ] Log access control failures
- [ ] Include timestamps and user context in security logs

---

### A10 — Server-Side Request Forgery (SSRF)
**What it is:** Attacker tricks server into making HTTP requests to internal services.

```python
# VULNERABLE: Fetch any URL the user provides
@app.get("/fetch")
def fetch_url(url: str):
    return requests.get(url).text

# SECURE: Allowlist of permitted domains
from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}

@app.get("/fetch")
def fetch_url(url: str):
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="URL not allowed")
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only http/https allowed")
    return requests.get(url, timeout=5).text
```

---

## Quick Code Review Checklist

When reviewing LLM-generated or human-written code, check for:

- [ ] SQL queries use parameterized inputs
- [ ] No `shell=True` with user input
- [ ] Secrets come from environment variables
- [ ] Auth checks on every protected endpoint
- [ ] Password hashing uses bcrypt/argon2
- [ ] JWT has expiry
- [ ] CORS is not `*` unless intentional
- [ ] User-supplied URLs are validated before fetching
- [ ] No sensitive data in logs
- [ ] Dependencies scanned for CVEs

---

## Pairs Well With

- `spec-first-development` — specify security requirements in the spec before coding
- `sql-and-databases` — parameterized queries in depth
- `structured-output-local` — validate and sanitize all model output before use

---

## License

CC0-1.0 — public domain, free to use for any purpose.
