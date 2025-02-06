import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lib import API_PORT, API_HOST, API_PREFIX

from auth.controller import auth_router
from endpoint.controller import endpoint_router, on_startup as chat_on_startup
from org.controller import org_router
from agent.controller import agent_router

from chat.channel.controller import channel_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await chat_on_startup()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(endpoint_router, prefix=API_PREFIX)
app.include_router(org_router, prefix=API_PREFIX)
app.include_router(agent_router, prefix=API_PREFIX)
app.include_router(channel_router, prefix=API_PREFIX)


def main():
    import uvicorn

    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)


if __name__ == "__main__":
    main()
