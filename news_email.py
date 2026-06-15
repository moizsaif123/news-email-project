"""
Daily News Email Sender
Fetches top headlines and emails them using Gmail SMTP
"""

import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from newsapi import NewsApiClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_news():
    """Fetch top headlines from NewsAPI"""
    newsapi = NewsApiClient(api_key=os.environ.get("NEWSAPI_KEY"))
    
    # Get top 10 headlines from the US (English language)
    #top_headlines = newsapi.get_top_headlines(language='en', country='us', page_size=10)
    
    #top_headlines = newsapi.get_top_headlines(sources='al-jazeera-english,cnn,khaleej-times',page_size=20)

    top_headlines = newsapi.get_top_headlines(
        sources='al-jazeera-english,cnn,bloomberg,abc-news',
        page_size=30
    )
    
    return top_headlines['articles']
    
def format_news_email(articles):
    """Format news articles into HTML email content"""
    today_date = datetime.datetime.now().strftime("%B %d, %Y")
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .article {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; background: #f8f9fa; }}
            .article h3 {{ margin: 0 0 10px 0; color: #2c3e50; }}
            .article p {{ margin: 5px 0; color: #555; }}
            .article a {{ color: #3498db; text-decoration: none; }}
            .article a:hover {{ text-decoration: underline; }}
            .source {{ font-size: 0.9em; color: #888; font-style: italic; }}
            .date {{ color: #888; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <h1>📰 Daily News Headlines</h1>
        <p class="date">{today_date}</p>
    """
    
    for i, article in enumerate(articles, 1):
        title = article.get("title") or "No title available"
        description = article.get("description") or "No description available."
        source = article.get("source", {}).get("name") or "Unknown source"
        url = article.get("url") or "#"
    
        html_content += """
        <div class="article">
            <h3>{num}. {title}</h3>
            <p>{description}</p>
            <p class="source">Source: {source}</p>
            <p><a href="{url}">Read more</a></p>
        </div>
        """.format(
            num=i,
            title=title,
            description=description[:200],
            source=source,
            url=url
        )
    
    html_content += """
    </body>
    </html>
    """
    
    return html_content

def send_email(html_content):
    """Send email using Gmail SMTP"""
    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_password:
        print("Error: Gmail credentials not found in environment variables")
        return False

    recipients_str = os.environ.get("EMAIL_RECIPIENTS", gmail_address)
    recipients = [email.strip() for email in recipients_str.split(",") if email.strip()]

    if not recipients:
        recipients = [gmail_address]

    print(f"Recipients list: {recipients}")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Daily News Headlines - {datetime.datetime.now().strftime('%B %d, %Y')}"
    msg["From"] = gmail_address
    msg["To"] = ", ".join(recipients)

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_address, gmail_password)
            server.sendmail(gmail_address, recipients, msg.as_string())

        print(f"Email sent successfully to {len(recipients)} recipient(s): {', '.join(recipients)}!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication error: {e}")
        print("Please check your Gmail address and app password.")
        return False

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
        
def main():
    """Main function to fetch news and send email"""
    print("Fetching news headlines...")
    articles = get_news()
    
    if not articles:
        print("No articles found. Check NewsAPI configuration.")
        return False
    
    print(f"Found {len(articles)} articles. Formatting email...")
    html_content = format_news_email(articles)
    
    print("Sending email...")
    success = send_email(html_content)
    
    return success

if __name__ == "__main__":
    main()
