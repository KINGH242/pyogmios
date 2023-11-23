from __future__ import annotations

import json
from typing import Callable, Any, Coroutine, Union, List, Dict

from nanoid import generate

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import AcquireFailureDetails, EraWithGenesis
from pyogmios_client.exceptions import (
    UnknownResultError,
    AcquirePointTooOldError,
    AcquirePointNotOnChainError,
    RequestError,
)
from pyogmios_client.models import (
    BaseModel,
    PointOrOrigin,
    BlockNoOrOrigin,
    Epoch,
    ProtocolParametersShelley,
    ProtocolParametersAlonzo,
    ProtocolParametersBabbage,
    DelegationsAndRewardsByAccounts,
    DigestBlake2BCredential,
    Bound,
    EraSummary,
    Lovelace,
    DigestBlake2bCredential,
    NonMyopicMemberRewards,
    StakeAddress,
    PoolId,
    PoolParameters,
    PoolsRanking,
    RewardsProvenance,
    RewardsProvenanceNew,
    PoolDistribution,
    UtcTime,
)
from pyogmios_client.models.request_model import RequestRelease, RequestAwaitAcquire
from pyogmios_client.models.response_model import ReleaseResponse, AcquireResponse
from pyogmios_client.models.result_models import (
    AcquireSuccessResult,
    AcquireFailureResult,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.block_height import (
    block_height,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.chain_tip import (
    chain_tip,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.current_epoch import (
    current_epoch,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.current_protocol_parameters import (
    current_protocol_parameters,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.delegations_and_rewards import (
    delegations_and_rewards,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.era_start import (
    era_start,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.era_summaries import (
    era_summaries,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.genesis_config import (
    genesis_config,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.ledger_tip import (
    ledger_tip,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.non_myopic_member_rewards import (
    non_myopic_member_rewards,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.pool_ids import (
    pool_ids,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.pool_parameters import (
    pool_parameters,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.pools_ranking import (
    pools_ranking,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.proposed_protocol_parameters import (
    proposed_protocol_parameters,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.rewards_provenance import (
    rewards_provenance,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.rewards_provenance_new import (
    rewards_provenance_new,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.stake_distribution import (
    stake_distribution,
)
from pyogmios_client.ouroboros_mini_protocols.state_query.queries.system_start import (
    system_start,
)
from pyogmios_client.utils.socket_utils import ensure_socket_is_open


class Options(BaseModel):
    point: PointOrOrigin


class StateQueryClient(BaseModel):
    """
    Data model for the state query client
    """

    context: InteractionContext
    acquire: Callable[[PointOrOrigin], Coroutine[Any, Any, StateQueryClient]]
    release: Callable[[], Coroutine[Any, Any, ReleaseResponse | None]]
    shutdown: Callable[[], Coroutine[Any, Any, None]]
    block_height: Callable[[], Coroutine[Any, Any, BlockNoOrOrigin]]
    chain_tip: Callable[[], Coroutine[Any, Any, PointOrOrigin]]
    current_epoch: Callable[[], Coroutine[Any, Any, Epoch]]
    current_protocol_parameters: Callable[
        [],
        Coroutine[
            Any,
            Any,
            Union[
                ProtocolParametersBabbage,
                ProtocolParametersAlonzo,
                ProtocolParametersShelley,
            ],
        ],
    ]
    delegations_and_rewards: Callable[
        [List[DigestBlake2BCredential]],
        Coroutine[Any, Any, DelegationsAndRewardsByAccounts],
    ]
    era_start: Callable[[], Coroutine[Any, Any, Bound]]
    era_summaries: Callable[[], Coroutine[Any, Any, List[EraSummary]]]
    genesis_config: Callable[[EraWithGenesis], Coroutine[Any, Any, List[EraSummary]]]
    ledger_tip: Callable[[], Coroutine[Any, Any, PointOrOrigin]]
    non_myopic_member_rewards: Callable[
        [List[Lovelace] | List[DigestBlake2bCredential] | List[StakeAddress]],
        Coroutine[Any, Any, NonMyopicMemberRewards],
    ]
    pool_ids: Callable[[], Coroutine[Any, Any, List[PoolId]]]
    pool_parameters: Callable[
        [List[PoolId]], Coroutine[Any, Any, Dict[str, PoolParameters]]
    ]
    pools_ranking: Callable[[], Coroutine[Any, Any, PoolsRanking]]
    proposed_protocol_parameters: Callable[
        [],
        Coroutine[
            Any,
            Any,
            Union[
                Dict[str, ProtocolParametersShelley],
                Dict[str, ProtocolParametersAlonzo],
                Dict[str, ProtocolParametersBabbage],
                None,
            ],
        ],
    ]
    rewards_provenance: Callable[[], Coroutine[Any, Any, RewardsProvenance]]
    rewards_provenance_new: Callable[[], Coroutine[Any, Any, RewardsProvenanceNew]]
    stake_distribution: Callable[[], Coroutine[Any, Any, PoolDistribution]]
    system_start: Callable[[], Coroutine[Any, Any, UtcTime]]


async def create_state_query_client(
    context: InteractionContext, options: Options = None
) -> StateQueryClient | None:
    """
    Create a state query client
    :param context: The interaction context
    :param options: The options
    :return: A state query client
    """
    websocket_app = context.socket

    async def acquire(point: PointOrOrigin) -> StateQueryClient:
        """
        Acquire the a point
        """
        client = await create_state_query_client(context, Options(point=point))
        return client

    async def release() -> ReleaseResponse | None:
        """
        Release the state query client
        """
        await ensure_socket_is_open(websocket_app)
        request_id = generate(size=5)
        try:
            request = RequestRelease.from_base(mirror={"requestId": str(request_id)})
            websocket_app.send(request.model_dump_json())
            result = websocket_app.sock.recv()
            release_response = ReleaseResponse(**json.loads(result))

            if release_response.reflection.requestId != request_id:
                return None

            return release_response
        except Exception as e:
            raise e

    async def shutdown() -> None:
        """
        Shutdown the state query client
        """
        try:
            await ensure_socket_is_open(websocket_app)
            websocket_app.close()
        except Exception as err:
            print(err)
        else:
            print("Shutting down State Query Client...")

    async def query_block_height() -> BlockNoOrOrigin:
        """
        Query the block height
        """
        await ensure_socket_is_open(websocket_app)
        return await block_height(context)

    async def query_chain_tip() -> PointOrOrigin:
        """
        Query the chain tip
        """
        await ensure_socket_is_open(websocket_app)
        return await chain_tip(context)

    async def query_current_epoch() -> Epoch:
        """
        Query the current epoch
        """
        await ensure_socket_is_open(websocket_app)
        return await current_epoch(context)

    async def query_current_protocol_parameters() -> ProtocolParametersBabbage | ProtocolParametersAlonzo | ProtocolParametersShelley:
        """
        Query the current protocol parameters
        """
        await ensure_socket_is_open(websocket_app)
        return await current_protocol_parameters(context)

    async def query_delegations_and_rewards(
        stake_key_hashes: List[DigestBlake2BCredential],
    ) -> DelegationsAndRewardsByAccounts:
        """
        Query delegations and rewards
        """
        await ensure_socket_is_open(websocket_app)
        return await delegations_and_rewards(context, stake_key_hashes)

    async def query_era_start() -> Bound:
        """
        Query the era start
        """
        await ensure_socket_is_open(websocket_app)
        return await era_start(context)

    async def query_era_summaries() -> List[EraSummary]:
        """
        Query the era summaries
        """
        await ensure_socket_is_open(websocket_app)
        return await era_summaries(context)

    async def query_genesis_config(era: EraWithGenesis) -> List[EraSummary]:
        """
        Query the genesis config
        """
        await ensure_socket_is_open(websocket_app)
        return await genesis_config(context, era)

    async def query_ledger_tip() -> PointOrOrigin:
        """
        Query the ledger tip
        """
        await ensure_socket_is_open(websocket_app)
        return await ledger_tip(context)

    async def query_non_myopic_member_rewards(
        input_list: List[Lovelace] | List[DigestBlake2bCredential],
    ) -> NonMyopicMemberRewards:
        """
        Query non myopic member rewards
        """
        await ensure_socket_is_open(websocket_app)
        return await non_myopic_member_rewards(context, input_list)

    async def query_pool_ids() -> List[PoolId]:
        """
        Query pool ids
        """
        await ensure_socket_is_open(websocket_app)
        return await pool_ids(context)

    async def query_pool_parameters(pools: List[PoolId]) -> Dict[str, PoolParameters]:
        """
        Query pool parameters
        """
        await ensure_socket_is_open(websocket_app)
        return await pool_parameters(context, pools)

    async def query_pools_ranking() -> PoolsRanking:
        """
        Query pools ranking
        """
        await ensure_socket_is_open(websocket_app)
        return await pools_ranking(context)

    async def query_proposed_protocol_parameters() -> Dict[
        str, ProtocolParametersShelley
    ] | Dict[str, ProtocolParametersAlonzo] | Dict[
        str, ProtocolParametersBabbage
    ] | None:
        """
        Query proposed protocol parameters
        """
        await ensure_socket_is_open(websocket_app)
        return await proposed_protocol_parameters(context)

    async def query_rewards_provenance() -> RewardsProvenance:
        """
        Query rewards provenance
        """
        await ensure_socket_is_open(websocket_app)
        return await rewards_provenance(context)

    async def query_rewards_provenance_new() -> RewardsProvenanceNew:
        """
        Query rewards provenance new
        """
        await ensure_socket_is_open(websocket_app)
        return await rewards_provenance_new(context)

    async def query_stake_distribution() -> PoolDistribution:
        """
        Query stake distribution
        """
        await ensure_socket_is_open(websocket_app)
        return await stake_distribution(context)

    async def query_system_start() -> UtcTime:
        """
        Query system start
        """
        await ensure_socket_is_open(websocket_app)
        return await system_start(context)

    try:

        def create_client() -> StateQueryClient:
            """
            Create a state query client
            """
            return StateQueryClient(
                context=context,
                acquire=acquire,
                release=release,
                shutdown=shutdown,
                block_height=query_block_height,
                chain_tip=query_chain_tip,
                current_epoch=query_current_epoch,
                current_protocol_parameters=query_current_protocol_parameters,
                delegations_and_rewards=query_delegations_and_rewards,
                era_start=query_era_start,
                era_summaries=query_era_summaries,
                genesis_config=query_genesis_config,
                ledger_tip=query_ledger_tip,
                non_myopic_member_rewards=query_non_myopic_member_rewards,
                pool_ids=query_pool_ids,
                pool_parameters=query_pool_parameters,
                pools_ranking=query_pools_ranking,
                proposed_protocol_parameters=query_proposed_protocol_parameters,
                rewards_provenance=query_rewards_provenance,
                rewards_provenance_new=query_rewards_provenance_new,
                stake_distribution=query_stake_distribution,
                system_start=query_system_start,
            )

        if options and options.point:
            # point = options.point
            await_acquire_request_id = generate(size=5)
            # await ensure_socket_is_open(websocket_app)
            try:
                await_acquire_request = RequestAwaitAcquire.from_base(
                    mirror={"requestId": str(await_acquire_request_id)}
                )
                websocket_app.send(await_acquire_request.model_dump_json())
                await_acquire_result = websocket_app.sock.recv()
                acquire_response = AcquireResponse(**json.loads(await_acquire_result))

                if acquire_response.reflection.requestId != await_acquire_request_id:
                    return None

                if isinstance(acquire_response.result, AcquireSuccessResult):
                    return create_client()
                elif isinstance(acquire_response.result, AcquireFailureResult):
                    websocket_app.close()
                    failure = acquire_response.result.AcquireFailure.failure
                    match failure:
                        case AcquireFailureDetails.POINT_TOO_OLD:
                            raise AcquirePointTooOldError()
                        case AcquireFailureDetails.POINT_NOT_ON_CHAIN:
                            raise AcquirePointNotOnChainError()
                        case _:
                            raise RequestError(failure)
                else:
                    raise UnknownResultError(acquire_response.result)
            except Exception as error:
                raise error
        else:
            return create_client()
    except Exception as e:
        raise e
