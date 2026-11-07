# gift.py
from TikTokLive import TikTokLiveClient
from TikTokLive.events import GiftEvent

def run_gift_client(target_user, on_new_gift, on_update_stats):
    client = TikTokLiveClient(unique_id=target_user)

    @client.on(GiftEvent)
    async def on_gift(event: GiftEvent):
        if not event.gift:
            return

        gift_name = getattr(event.gift, "name", "Unknown Gift")
        count = getattr(event, "repeat_count", 1)
        diamond_count = getattr(event.gift, "diamond_count", 1)
        diamonds = diamond_count * count

        nickname = event.user.nickname if event.user else "Someone"
        gift_msg = f"{nickname} sent {count}x {gift_name} (+{diamonds} 💎)"
        
        # Pass data back to the GUI
        on_new_gift(gift_msg)
        on_update_stats(count, diamonds)

    client.run()