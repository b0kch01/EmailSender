import google_workspace
import datetime
import re
from templates import generate_follow_up

from google_workspace.gmail.message import BaseMessage, Message

class UserSession:
    def __init__(self) -> None:
        pass

    def login(self, email: str, name: str, *, custom_session: str=""):
        self._email = email
        self._name = name

        # Create a new session
        session_name = custom_session if custom_session else f"hack-uci-followup-{email}-{datetime.datetime.now().isoformat()}"
        print(f"session_name: {session_name}")

        self._service = google_workspace.service.GoogleService(
            api="gmail",
            session=session_name,
            client_secrets="secrets.json"
        )
        self._service.local_oauth()

        # Create a new Gmail client
        self._gmail_client = google_workspace.gmail.GmailClient(
            service=self._service,
            sender_name=name,
        )

    def client(self):
        return self._gmail_client

class EmailFinder:
    def __init__(self, session: UserSession) -> None:
        self._session = session

    def find(self, subject: str, limit: int=None, after: datetime.datetime=None, verbose: bool=False):
        messages = list(self._session.client().get_messages(
            from_=self._session._email,
            subject=subject,
            limit=limit,
            after=after,
            message_format="full"
        ))

        if verbose:
            for message in messages:
                self.display(message)

        return messages


    def display(self, message: type[BaseMessage] | BaseMessage):
        """
        Display the message in the console.
        Nicely formatted and truncated into columns
        """

        print(f"Subject: {message.subject} | To: {message.to} | Date: {message.date}")


class FollowupBot:
    def __init__(self, finder: EmailFinder) -> None:
        self.finder = finder

    def parse_name(self, name: str):
        # use regex to get the name from "Hello (name),"
        # only match first occurence
        match = re.match(r"Hello (.+),", name)
        if match:
            return match.group(1)
        return None


    def send_followup(self, message: Message, wave):
        count = 0
        for reply in message.get_thread().messages:
            count += 1

            if reply.from_ != self.finder._session._email:
                print("thread does not need followup")
                return

            if count > wave:
                print("thread does not need followup for this wave")
                return

        name = self.parse_name(message.html_text)
        html = generate_follow_up(name, your_name=self.finder._session._name)

        message.reply(html=html, follow_up=True)
        print(f"Sent followup to {name} for wave {wave}")

    def send_followups(self, wave: int, subject: str, limit: int=None, after: datetime.datetime=None):
        messages = self.finder.find(
            subject=subject,
            limit=limit,
            after=after,
            verbose=True
        )

        for message in messages:
            self.send_followup(message, wave)
