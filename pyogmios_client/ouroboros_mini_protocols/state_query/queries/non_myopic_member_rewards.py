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
    Lovelace,
    DigestBlake2bCredential,
    NonMyopicMemberRewards,
    StakeAddress,
)
from pyogmios_client.models.response_model import NonMyopicMemberRewardsResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: NonMyopicMemberRewardsResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_non_myopic_member_rewards(response: NonMyopicMemberRewardsResponse) -> bool:
    result = response.result
    if isinstance(result, NonMyopicMemberRewards):
        return True
    return False


async def non_myopic_member_rewards(
    context: InteractionContext,
    input_list: List[Lovelace] | List[DigestBlake2bCredential] | List[StakeAddress],
) -> NonMyopicMemberRewards:
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={"query": {"nonMyopicMemberRewards": input_list}},
    )

    try:
        response = await query(request_args, context)
        query_response = NonMyopicMemberRewardsResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("nonMyopicMemberRewards")
        elif is_non_myopic_member_rewards(query_response):
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
