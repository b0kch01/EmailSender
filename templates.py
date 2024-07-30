
def base_html(text: str) -> str:
    return f"""
    <html>
        <head></head>
        <body>
            <p>{text}</p>
        </body>
    </html>
    """


def generate_follow_up(contact_name: str, your_name: str) -> str:
    return base_html(
        f"""
        Hi {contact_name},
        <br><br>
        Just wanted to follow up on this regarding a potential sponsorship with IrvineHacks.
        Please let me know if you have any questions, and I look forward to hearing from you soon!
        <br><br>
        Best Regards,
        <br><br>
        {your_name} Corporate Outreach | IrvineHacks 
        """
    )
