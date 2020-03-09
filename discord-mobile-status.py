class MobileWebSocket(discord.gateway.DiscordWebSocket):
    async def identify(self):
        """Sends the IDENTIFY packet."""
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "ios",
                    "$browser": "Discord iOS",
                    "$device": "discord.py",
                    "$referrer": "",
                    "$referring_domain": "",
                },
                "compress": True,
                "large_threshold": 250,
                "v": 3,
            },
        }

        if not self._connection.is_bot:
            payload["d"]["synced_guilds"] = []

        if self.shard_id is not None and self.shard_count is not None:
            payload["d"]["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            payload["d"]["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        await self.send_as_json(payload)
        discord.gateway.log.info(
            "Shard ID %s has sent the IDENTIFY payload.", self.shard_id
        )


discord.client.DiscordWebSocket = MobileWebSocket
