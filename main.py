import requests
from bs4 import BeautifulSoup
import schedule
import time
from pyppeteer import launch
from telegram import Bot

linkedin_url = "https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=3947524387&distance=25&f_TPR=a1718131920-&f_WT=2&geoId=106057199&keywords=Desenvolvedor%20full%20stack&origin=JOB_ALERT_IN_APP_NOTIFICATION&originToLandingJobPostings=3947524387&savedSearchId=3519597281&sortBy=R"
telegram_token = ""
chat_id = ""

def extract_jobs():
    print("Extraindo vagas...")
    try:

        async def fetch():
            browser = await launch()
            page = await browser.newPage()
            await page.goto(linkedin_url)
            content = await page.content()
            await browser.close()
            return content

        content = None
        
        try:
            content = fetch()
        except Exception as e:
            print("Erro ao carregar página com pyppeteer:", e)
            return

        soup = BeautifulSoup(content, "html.parser")

        jobs = soup.find_all(
            "li", class_="result-card job-result-card result-card--with-hover-state"
        )

        for job in jobs:
            job_title = job.find(
                "h3", class_="result-card__title job-result-card__title"
            ).text.strip()
            company = job.find(
                "a", class_="result-card__subtitle-link job-result-card__subtitle-link"
            ).text.strip()
            location = job.find("span", class_="job-result-card__location").text.strip()
            job_link = job.find("a", class_="result-card__full-card-link")["href"]

            print(f"Vaga: {job_title}")
            print(f"Empresa: {company}")
            print(f"Localização: {location}")
            print(f"Link: {job_link}")
            print("\n")

        #send_telegram_notification("Vagas extraídas com sucesso!")

    except Exception as e:
        print("Erro durante extração de vagas:", e)


def send_telegram_notification(message):
    bot = Bot(token=telegram_token)
    bot.send_message(chat_id=chat_id, text=message)


def job():
    print("Rodando script de coleta de dados...")
    extract_jobs()


def main():
    # # Executar o job a cada 1 hora
    # schedule.every(1).hour.do(job)

    # Rodar o job imediatamente ao iniciar o script
    job()

    # # Loop para manter o script em execução
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

if __name__ == "__main__":
    main()
