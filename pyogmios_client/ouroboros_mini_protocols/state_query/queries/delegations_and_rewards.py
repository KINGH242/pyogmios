from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    DigestBlake2BCredential,
    DelegationsAndRewardsByAccounts,
    QueryUnavailableInCurrentEra,
)
from pyogmios_client.models.response_model import DelegationsAndRewardsResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


async def delegations_and_rewards(
    context: InteractionContext, stake_key_hashes: List[DigestBlake2BCredential]
) -> DelegationsAndRewardsByAccounts:
    """
    Query the delegations and rewards for the given stake key hashes.
    :param context: The interaction context to use for the query.
    :param stake_key_hashes: The stake key hashes to query.
    :return: The delegations and rewards for the given stake key hashes.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={"query": {"delegationsAndRewards": stake_key_hashes}},
    )

    try:
        response = await query(request_args, context)
        query_response = DelegationsAndRewardsResponse(**response.model_dump())
        result = query_response.result
        if isinstance(result, QueryUnavailableInCurrentEra):
            raise QueryUnavailableInCurrentEraError("delegationsAndRewards")
        elif isinstance(result, DelegationsAndRewardsByAccounts):
            return query_response.result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                era_mismatch.queryEra.value, era_mismatch.ledgerEra.value
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
