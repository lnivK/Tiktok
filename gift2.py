import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import GiftEvent

#input target 
target = input("connect ke Live siapa: ")
client : TikTokLiveClient = TikTokLiveClient(unique_id=target)


@client.on(GiftEvent)
async def on_gift(event: GiftEvent):

        print(f"{event.user.nickname} -> {event.gift.name}")
    


if __name__ == "__main__":
    client.run()