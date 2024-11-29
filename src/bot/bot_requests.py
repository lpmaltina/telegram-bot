import httpx

from src.bot import utils

URL = "http://127.0.0.1:8000"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}


def handle_request(make_request):
    async def wrapper(*args, **kwargs):
        try:
            response = await make_request(*args, **kwargs)
            answer = utils.stringify_response(response)
        except:
            answer = utils.REQUEST_ERROR
        return answer
    return wrapper


@handle_request
async def get_all_request() -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL}/get_all")
        print(type(response))
    return response


@handle_request
async def get_by_id_request(review_id: int) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL}/get/{review_id}")
    return response


@handle_request
async def edit_by_id_request(review_id: int, review: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{URL}/edit",
            headers=HEADERS,
            json={"id": review_id, "review": review}
        )
    return response


@handle_request
async def add_request(review: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{URL}/add", headers=HEADERS, json={"review": review}
        )
    return response


@handle_request
async def delete_by_id_request(review_id: int) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{URL}/delete/{review_id}")
    return response


@handle_request
async def delete_all_request():
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{URL}/delete_all")
    return response


@handle_request
async def sentiment_request(review: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL}/sentiment/{review}")
    return response
