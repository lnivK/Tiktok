import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import GiftEvent

#input target 
target = input("connect ke Live siapa: ")
client : TikTokLiveClient = TikTokLiveClient(unique_id=target)

gift_count = 0

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    global gift_count
    if not event.gift:
        return
    
    a = print(f"{event.user.nickname} -> {event.gift.name}")
    
    gift_count += 1
    print(a)
    print(f"total gift sejak masuk : {gift_count}\n")


if __name__ == "__main__":
    client.run()