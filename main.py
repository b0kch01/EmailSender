import datetime
from emailsender import UserSession, EmailFinder, FollowupBot
from tabulate import tabulate

session = UserSession()
session.login(
    email="nhchoi1@uci.edu",
    name="Nathan Choi",
    custom_session="follow-up-testing"
)

finder = EmailFinder(session)
followup_bot = FollowupBot(finder)

execute, contacts = followup_bot.send_followups(
    wave=1,
    subject="test",
    after=datetime.datetime(2023, 7, 29)
)

SUBJECT_WIDTH = 25
for contact in contacts:
    contact.subject = contact.subject[:SUBJECT_WIDTH] + \
        "..." if len(contact.subject) > SUBJECT_WIDTH else contact.subject

print(tabulate(contacts, headers="keys", showindex=True, tablefmt="rounded_grid"))

if input("Do you want to send followups? (y/n): ") == "y":
    execute()
    print("Followups sent!")
