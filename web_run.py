import os
import asyncio
from aiohttp import web


from Route import web_server

async def main():
    app = await web_server()
    port = int(os.environ.get("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"✅ Web server running on port {port}")

    # keep running forever
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
