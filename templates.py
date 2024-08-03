
def base_html(text: str) -> str:
    return f"""
    <html>
        <head></head>
        <body>
            <p>{text}</p>
        </body>
    </html>
    """

def generate_cold_email(contact_name: str, your_name: str, company: str) -> str:
    return base_html(
        f"""
        Hello {contact_name},
        <br><br>
        My name is {your_name} and I’m currently a Corporate Organizer for <a href="https://hack.ics.uci.edu/">Hack at UCI</a>, the largest collegiate STEM organization at UC Irvine and in Orange County. Established in 2013, our organization hosts hackathons, technical workshops, career panels, and other events that have brought in 800+ attendees in total each year. For hackathons, we organize Orange County’s biggest annual hackathon, IrvineHacks (previously known as HackUCI) with an expected 400+ attendees, as well as ZotHacks, a beginner-friendly hackathon with an expected 150+ attendees. IrvineHacks will be taking place Winter 2025 while Zothacks will be taking place Fall 2024.

        We’re always searching for ways to grow the club and plan the best events possible. Over the years, we’ve partnered with dozens of companies to build connections for our hackers and provide additional resources for both our events and our partner companies’ recruitment processes. This year, we’re reaching out to {company} because we’re interested in having you as a sponsor!

        I would love the opportunity to discuss how {company} can meet some of the best developers at our events and have a lasting impact on our hacker community. We can definitely hop onto a quick 20 minute call to discuss our sponsorship deck and any questions you may have!
        <br><br>
        Best Regards,
        <br><br>
        {your_name} - Corporate Outreach | Hack at UCI
        """
    )


def generate_follow_up(contact_name: str, your_name: str) -> str:
    return base_html(
        f"""
        Hi {contact_name},
        <br><br>
        Just wanted to follow up on this regarding a potential sponsorship with IrvineHacks or ZotHacks.
        Please let me know if you have any questions, and I look forward to hearing from you soon!
        <br><br>
        Best Regards,
        <br><br>
        {your_name} - Corporate Outreach | Hack at UCI
        """
    )
