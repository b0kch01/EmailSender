import google_workspace
import datetime
import re
from templates import generate_follow_up
from dataclasses import dataclass
from alive_progress import alive_it
import time

from google_workspace.gmail.message import BaseMessage, MessageMetadata


@dataclass(frozen=False, order=True)
class Contact:
    subject: str
    name: str
    email: str
    date: datetime.datetime


class UserSession:
    def __init__(self) -> None:
        pass

    def login(self, email: str, name: str, *, custom_session: str = ""):
        self._email = email
        self._name = name

        # Create a new session
        session_name = custom_session if custom_session else f"hack-uci-followup-{email}-{datetime.datetime.now().isoformat()}"

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

    def find(self, subject: str, limit: int = None, after: datetime.datetime = None, verbose: bool = False):
        if verbose:
            print(
                f"Finding emails with subject (this could take a while): {subject}")

        messages_generator = self._session.client().get_messages(
            from_=self._session._email,
            subject=subject,
            # TO NOT BLOW OUT THE API QUOTA LOL,
            # but if you're a 10x corporate organizer you can increase ofc
            limit=350,
            after=after,
            message_format="metadata"
        )

        messages: list[MessageMetadata] = list(
            filter(
                lambda m: not m.is_reply,
                messages_generator
            )
        )

        if verbose:
            print(f"Found {len(messages)} emails with subject: {subject}")

        return messages

    def display(self, message: type[BaseMessage] | BaseMessage):
        """
        Display the message in the console.
        Nicely formatted and truncated into columns
        """

        print(
            f"Subject: {message.subject} | To: {message.to[0]} | Date: {message.date}", flush=True)


class FollowupBot:
    def __init__(self, finder: EmailFinder) -> None:
        self.finder = finder
        self.follow_up_list: list[tuple[MessageMetadata, str]] = []

    def _create_contact_list(self):
        return [
            Contact(
                subject=message.subject or "No subject",
                name=self.find_first_name(message.snippet) or "No name",
                email=", ".join(message.to),
                date=message.date
            )
            for message, _ in self.follow_up_list
        ]

    def find_first_name(self, name: str) -> str | None:
        """
        ### Summary
        Find the first name of the contact from the email message.
        The name is assumed to be in the format: "Hello [name],"
        """
        match = re.search(r"Hello (.+?),", name)
        if match:
            return match.group(1)
        return None

    def send_followup(self, message: BaseMessage, wave, _double_check: bool = True, verbose: bool = False):
        """
        ### Summary
        Send a follow-up email to the given message object and wave, if the conditions are met.

        ### Technical notice:
        - Fetching minimal is much lighter than full/metadata, but 95% of the time,
          we don't get replies so we can just keep everything to one request instead of two
          (minimal for checking thread size and metadata for checking sender)

        As we develop this script, we need to add more checks to make sure we're sending followups to the right people
        For now, we are using two basic heuristics:
        - Check the number of messages in the thread (for safety, must be exactly the wave number)
        - Check the sender of the messages in the thread (if not us, then we don't need to send followup)
        """

        thread = message.get_thread("metadata")  # note: heavy operation

        if thread.number_of_messages != wave:
            if verbose:
                print("-- [skip] not in the current wave")
            return

        for reply in thread.messages:
            if reply.from_ != self.finder._session._email:
                if verbose:
                    print("-- [skip] has replies from other senders. great job!")
                return

        contact_fname = self.find_first_name(message.snippet)
        html = generate_follow_up(
            contact_name=contact_fname,
            your_name=self.finder._session._name
        )

        if _double_check:
            self.follow_up_list.append((message, html))
        else:
            message.reply(html=html, follow_up=True)

    def send_followups(self, wave: int, subject: str, limit: int = None, after: datetime.datetime = None, double_check: bool = True):
        messages = self.finder.find(
            subject=subject,
            limit=limit,
            after=after,
            verbose=True
        )

        if double_check:
            self.follow_up_list = []

        for message in messages:
            self.send_followup(
                message=message,
                wave=wave,
                verbose=True,
                _double_check=True
            )

        # Not the cleanest paradigm but it works for now
        if double_check:
            def execute_followups():
                for message, html in alive_it(self.follow_up_list):
                    time.sleep(0.5)
                    # message.get_full_message().reply(html=html, follow_up=True)

            return execute_followups, self._create_contact_list()
        else:
            return None
