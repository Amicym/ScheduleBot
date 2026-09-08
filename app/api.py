import datetime
from curl_cffi.requests import AsyncSession


async def fetch_api(session: AsyncSession, id_=None, date=None) -> list[str]:
    if date is None:
        date = datetime.datetime.today().strftime("%Y-%m-%d")
    
    if id_ is None:
        url = "https://kp-raspisanie.ru/api/groups?college=branch"
    else:
        url = f"https://kp-raspisanie.ru/api/schedule?college=branch&groupId={id_}&date={date}"
    
    response = await session.get(url)

    raw_data = response.json()

    return raw_data