from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    EraMismatch,
    DigestBlake2BCredential,
    DelegationsAndRewardsByAccounts,
)
from pyogmios_client.models.response_model import DelegationsAndRewardsResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: DelegationsAndRewardsResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_delegations_and_rewards_by_accounts(
    response: DelegationsAndRewardsResponse,
) -> bool:
    result = response.result
    if len(result.__root__) <= 0:
        return True
    sample = list(result.__root__.values())[0]
    return sample.delegate is not None and sample.rewards is not None


async def delegations_and_rewards(
    context: InteractionContext, stake_key_hashes: List[DigestBlake2BCredential]
) -> DelegationsAndRewardsByAccounts:
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={"query": {"delegationsAndRewards": stake_key_hashes}},
    )

    try:
        response = await query(request_args, context)
        query_response = DelegationsAndRewardsResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("delegationsAndRewards")
        elif is_delegations_and_rewards_by_accounts(query_response):
            return query_response.result
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
