import asyncio
from TikTokLive import TikTokLiveClient
from TikTokLive.events import RoomUserSeqEvent, LikeEvent

def viewer(target_user, on_viewer, on_likes, on_top_viewers):
    client = TikTokLiveClient(unique_id=target_user)

    @client.on(RoomUserSeqEvent)
    async def on_room_user_seq(event: RoomUserSeqEvent):
        # Try retrieving the viewer count from 'total' or 'total_user'
        count = getattr(event, 'total', None)
        if count is None:
            count = getattr(event, 'total_user', None)
        
        # If it's still missing, check popularity
        if count is None:
            count = getattr(event, 'popularity', None)

        if count is not None:
            on_viewer(count)

        top_user = getattr(event,'top_viewer_list', None) or getattr(event, 'ranks', None)
        if top_user and on_top_viewers:
            on_top_viewers_names = [user.user.nickname for user in top_user if hasattr(user, 'user')]
            on_top_viewers(on_top_viewers_names)

    @client.on(LikeEvent)    
    async def on_like(event: LikeEvent):
        # Pass the number of likes from the event object
        on_likes(event.count)

    client.run()