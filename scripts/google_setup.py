"""Google sign-in for this skill: the user's own OAuth client and one token, kept outside any project folder.

Usage:
  google_setup.py check     what is set up, what is missing, and the next step to give the user
  google_setup.py login     open Google's consent page and save the token (pip3 install google-auth-oauthlib);
                            waits up to 10 minutes for the user, so run it with a long timeout

Files live in $MINUTES_HOME, default ~/.config/vin-meeting-minutes-zh/:
  oauth-client.json   the user's own OAuth client (type: Desktop app) from their own Google Cloud project
  google-token.json   the refresh token saved by `login`, plus the account and its company domain; never printed

One token covers Google Drive (create and update the minutes Docs), Gmail (read transcript mails, send the
minutes), Calendar (meeting time, room and attendees; the next meeting's invite) and the company directory
(look up a colleague's address). Turning a transcript into a Word file needs none of this.

The "company domain" is the Google Workspace domain of the signed-in account, as Google reports it at login
(personal accounts have none). A new Doc is shared with it as commenter, and colleagues on it get edit access
when the minutes are mailed. $MINUTES_SHARE_DOMAIN overrides both; set it to "none" for no company domain.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG = Path(os.environ.get('MINUTES_HOME') or '~/.config/vin-meeting-minutes-zh').expanduser()
CLIENT = CONFIG / 'oauth-client.json'
TOKEN = CONFIG / 'google-token.json'
SCOPES = ['openid',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events',
          'https://www.googleapis.com/auth/directory.readonly']
# used only for a token saved without the Workspace domain: free mail providers are never a company domain
PERSONAL_DOMAINS = {'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.com.tw', 'hotmail.com', 'hotmail.com.tw',
                    'outlook.com', 'live.com', 'msn.com', 'icloud.com', 'me.com', 'mac.com', 'msa.hinet.net',
                    'hinet.net', 'pchome.com.tw', 'seed.net.tw', 'kimo.com', 'proton.me', 'protonmail.com'}


def client_info() -> dict | None:
    try:
        blob = json.loads(CLIENT.read_text())
        client = blob.get('installed') or blob.get('web')
    except (OSError, ValueError, AttributeError):
        return None
    return client if isinstance(client, dict) and 'client_secret' in client else None


def saved_token() -> dict:
    return json.loads(TOKEN.read_text())


def access_token() -> str:
    if not (TOKEN.exists() and CLIENT.exists()):
        sys.exit(f'NO GOOGLE LOGIN: {TOKEN} or {CLIENT} is missing. Hand over the Word file from md_to_docx.py, '
                 'or walk the user through the Google setup (SKILL.md section 6, step 9; start with google_setup.py check).')
    client = client_info()
    if not client:
        sys.exit(f'STOP: {CLIENT} is not an OAuth client JSON. Run google_setup.py check.')
    data = urllib.parse.urlencode({'client_id': client['client_id'], 'client_secret': client['client_secret'],
                                   'refresh_token': saved_token()['refresh_token'],
                                   'grant_type': 'refresh_token'}).encode()
    try:
        return json.load(urllib.request.urlopen(client['token_uri'], data))['access_token']
    except urllib.error.HTTPError as err:
        sys.exit(f'GOOGLE LOGIN EXPIRED ({err.code} {err.read().decode(errors="replace")[:200]}). '
                 'Run google_setup.py login again.')


def company_domain(email: str) -> str | None:
    override = os.environ.get('MINUTES_SHARE_DOMAIN')
    if override is not None:
        override = override.strip().lower().lstrip('@')
        return None if override in ('', 'none') else override
    try:
        token = saved_token()
    except (OSError, ValueError):
        token = {}
    if 'hd' in token:                       # saved by login from Google's own answer; None for personal accounts
        return token['hd'] or None
    domain = email.lower().rsplit('@', 1)[-1]
    return None if domain in PERSONAL_DOMAINS else domain


def same_company(email: str, domain: str | None) -> bool:
    return bool(domain) and email.lower().endswith('@' + domain)


# ---------- check ----------

def probe(token: str, name: str, url: str):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + token})
    try:
        return True, json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as err:
        body = err.read().decode(errors='replace')
        if 'SERVICE_DISABLED' in body or 'has not been used' in body:
            why = f'{name} is not enabled in the Cloud project (step 2)'
        elif 'insufficient' in body.lower() or 'ACCESS_TOKEN_SCOPE_INSUFFICIENT' in body:
            why = 'the token lacks this permission; run google_setup.py login again and allow everything'
        else:
            why = f'HTTP {err.code}: {body[:160]}'
        return False, why


def check():
    print(f'settings folder: {CONFIG}')
    if not CLIENT.exists():
        print('[ ] OAuth client: missing')
        print('NEXT: SKILL.md section 6, step 9, items 1-4 (Cloud project, four APIs, consent screen, '
              f'Desktop app client), then save the downloaded JSON as {CLIENT}')
        return
    if not client_info():
        print('[ ] OAuth client: the file is not an OAuth client JSON')
        print('NEXT: download the client again (type: Desktop app) and save it over ' + str(CLIENT))
        return
    if 'installed' not in json.loads(CLIENT.read_text()):
        print('[ ] OAuth client: this is a "Web application" client; login needs a "Desktop app" one')
        print('NEXT: SKILL.md section 6, step 9, item 4: create a Desktop app client and save it over ' + str(CLIENT))
        return
    print('[x] OAuth client: Desktop app')
    try:
        import google_auth_oauthlib  # noqa: F401
        print('[x] google-auth-oauthlib installed')
    except ImportError:
        print('[ ] google-auth-oauthlib: not installed (needed only for login): pip3 install google-auth-oauthlib')
    if not TOKEN.exists():
        print('[ ] signed in: no token yet')
        print('NEXT: google_setup.py login')
        return
    token = access_token()
    ok, about = probe(token, 'Google Drive API', 'https://www.googleapis.com/drive/v3/about?fields=user(emailAddress)')
    email = about['user']['emailAddress'] if ok else ''
    print(f'[{"x" if ok else " "}] Google Drive: ' + (email if ok else about))
    checks = [('Gmail API', 'https://gmail.googleapis.com/gmail/v1/users/me/profile'),
              ('Google Calendar API', 'https://www.googleapis.com/calendar/v3/users/me/calendarList?maxResults=1'),
              ('People API', 'https://people.googleapis.com/v1/people:searchDirectoryPeople?' + urllib.parse.urlencode(
                  {'query': 'a', 'readMask': 'names', 'sources': 'DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE', 'pageSize': 1}))]
    for name, url in checks:
        ok, result = probe(token, name, url)
        if ok and name == 'Gmail API':
            email = email or result['emailAddress']
        note = '' if ok else result
        if not ok and name == 'People API' and email and not company_domain(email):
            note = 'a personal Google account has no company directory; looking up addresses will not work'
        print(f'[{"x" if ok else " "}] {name}' + (f': {note}' if note else ''))
    if email:
        domain = company_domain(email)
        print(f'signed in as {email}; company domain: ' + (domain or 'none (new Docs are not shared, nobody gets '
                                                           'edit access by mail)'))


# ---------- login ----------

def id_claims(id_token: str | None) -> dict:
    """The ID token comes straight from Google's token endpoint over TLS; only its payload is read."""
    if not id_token:
        return {}
    payload = id_token.split('.')[1]
    return json.loads(base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4)))


def login():
    if not CLIENT.exists():
        sys.exit(f'STOP: {CLIENT} is missing. Finish items 1-4 of SKILL.md section 6, step 9 first.')
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit('STOP: run pip3 install google-auth-oauthlib first')
    os.environ.setdefault('OAUTHLIB_RELAX_TOKEN_SCOPE', '1')   # an unticked permission is reported below, not a crash
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT), SCOPES)
    hint = {'login_hint': os.environ['MINUTES_OWNER']} if os.environ.get('MINUTES_OWNER') else {}
    creds = flow.run_local_server(port=0, open_browser=True, prompt='consent', timeout_seconds=600,
                                  authorization_prompt_message='Opening the consent page. If no browser opens, '
                                                               'give the user this link: {url}', **hint)
    granted = getattr(creds, 'granted_scopes', None) or creds.scopes or SCOPES
    granted = sorted(granted.split() if isinstance(granted, str) else granted)
    claims = id_claims(creds.id_token)
    CONFIG.mkdir(parents=True, exist_ok=True)
    os.chmod(CONFIG, 0o700)
    fd = os.open(TOKEN, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as fh:
        fh.write(json.dumps({'refresh_token': creds.refresh_token, 'scopes': granted,
                             'email': claims.get('email'), 'hd': claims.get('hd')}))
    os.chmod(TOKEN, 0o600)                         # also when the file already existed with wider rights
    missing = [s.rsplit('/', 1)[-1] for s in SCOPES if s not in granted]
    if missing:
        print('saved, but these permissions were not ticked: ' + ', '.join(missing)
              + '. Run google_setup.py login again and tick every box.')
    else:
        print(f'saved for {claims.get("email") or "the account"}; now run google_setup.py check')


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('check', 'login'):
        sys.exit(__doc__)
    check() if sys.argv[1] == 'check' else login()
