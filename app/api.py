import datetime
from curl_cffi import requests


async def fetch_api(id_=None, date=None) -> list[str]:
    async with requests.AsyncSession(impersonate="chrome") as session:
        if date is None:
            date = datetime.datetime.today().strftime("%Y-%m-%d")
        
        if id_ is None:
            url = "https://kp-raspisanie.ru/api/groups?college=branch"
        else:
            url = f"https://kp-raspisanie.ru/api/schedule?college=branch&groupId={id_}&date={date}"
            # url = "https://kp-raspisanie.ru/api/schedule?college=branch&groupId=69fcb4ef7608632cd9e19473&date=2026-05-01"
        
        response = await session.get(url)

        raw_data = response.json()

        return raw_data