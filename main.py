import asyncio
from pyppeteer import launch
from telegram import Bot
import re
from bs4 import BeautifulSoup

linkedin_url = "https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=3954919377&f_TPR=r86400&f_WT=2&geoId=106057199&keywords=Desenvolvedor%20full%20stack&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=DD"
telegram_token = ""
chat_id = ""


async def fetch():
    browser = await launch(
        executablePath="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    )
    page = await browser.newPage()
    await page.goto(linkedin_url)
    content = await page.content()
    await browser.close()
    return content


def extract_jobs(content):
    print("Extraindo vagas...")
    try:
        job_details = []

        ul_regex = r'<ul\s+class="jobs-search__results-list"[^>]*>(.*?)</ul>'
        ul_match = re.search(ul_regex, content, re.DOTALL)

        if ul_match:
            ul_content = ul_match.group(1)

            soup = BeautifulSoup(ul_content, "html.parser")

            for li in soup.find_all("li"):
                job_title = li.find("h3").get_text().strip()
                company_name = li.find("h4").get_text().strip()
                location = (
                    li.find("span", class_="job-search-card__location")
                    .get_text()
                    .strip()
                )
                job_link = li.find("a")["href"]

                print(
                    f"Vaga: {job_title}\nEmpresa: {company_name}\nLocalização: {location}\nLink: {job_link}\n"
                )

        else:
            print("Não foi possível encontrar a lista de vagas.")

    except Exception as e:
        print("Erro durante extração de vagas:", e)


def send_telegram_notification(message):
    bot = Bot(token=telegram_token)
    bot.send_message(chat_id=chat_id, text=message)


async def job():
    print("Rodando script de coleta de dados...")
    content = await fetch()
    extract_jobs(content)


def main():
    asyncio.get_event_loop().run_until_complete(job())


if __name__ == "__main__":
    main()
