# EmailSender
```
✉️ Automate followups and email sending; designed and built for Hack at UCI Corporate
```

# Development Setup
1. Go to Google Cloud Console, make a new project and enable the Gmail API
2. Create a OAUTH2 credential and then downoad it. (Client secret etc. in JSON)
3. Put it in root and call it `cred.json`
4. For now: Change `main.py` to your stuff
## Python deps
> Tested on Python 3.11 but should work on anything higher than that too.
6. Install deps
```console
pip install -r requirements.txt
```
7. Run `main.py` to see basic features
```console
python main.py
```

# TODO
- [ ] Python UI Client
  - [ ] Select follow-up wave #
  - [ ] Colors
  - [ ] Menu select for different functions 
- [ ] Find easy way to package and run the client
- [ ] Mass email send feature?
- [ ] Set your name and email
- [ ] Different templates for different follow-up waves
- [ ] Cache some functionality?

# Crazy TODO
- [ ] Email tracking feature / compatibility with Streak
