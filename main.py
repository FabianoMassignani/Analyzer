import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from telegram import Bot

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
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("li", class_="job-card-list__job-card-container")

        job_details = []

        for job in jobs:
            job_title = job.find("a", class_="job-card-list__title").text.strip()
            company = job.find(
                "span", class_="job-card-container__primary-description"
            ).text.strip()
            location = job.find(
                "li", class_="job-card-container__metadata-item"
            ).text.strip()
            job_link = (
                "https://www.linkedin.com"
                + job.find("a", class_="job-card-list__title")["href"]
            )

            job_details.append(
                f"Vaga: {job_title}\nEmpresa: {company}\nLocalização: {location}\nLink: {job_link}\n"
            )

        message = "\n".join(job_details)

    except Exception as e:
        print("Erro durante extração de vagas:", e)


def send_telegram_notification(message):
    bot = Bot(token=telegram_token)
    bot.send_message(chat_id=chat_id, text=message)


def job():
    print("Rodando script de coleta de dados...")
    content = asyncio.run(fetch())
    extract_jobs(content)


def main():
    # Executar o job imediatamente ao iniciar o script
    job()

    # Loop para manter o script em execução (descomentado se desejado)
    # schedule.every(1).hour.do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()
