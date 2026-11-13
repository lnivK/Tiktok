from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent

def run_comment_client(target_user, on_new_comment):
    client = TikTokLiveClient(unique_id=target_user)

    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        nickname = event.user.nickname if event.user else "User"
        message = f"[{nickname}]: {event.comment}"
        # Pass the message back to the GUI
        on_new_comment(message)

    client.run()