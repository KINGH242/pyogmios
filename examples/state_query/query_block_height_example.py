import asyncio

from pyogmios_client.connection import (
    create_interaction_context,
    InteractionContextOptions,
)
from pyogmios_client.enums import InteractionType
from pyogmios_client.ouroboros_mini_protocols.state_query.state_query_client import (
    create_state_query_client,
)


async def main():
    """
    This will query the block height of the node through Ogmios.
    """
    interaction_context_options = InteractionContextOptions(
        interaction_type=InteractionType.ONE_TIME
    )
    interaction_context = await create_interaction_context(
        options=interaction_context_options
    )
    client = await create_state_query_client(interaction_context)
    bh = await client.block_height()
    # await client.shutdown()
    print(bh)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
