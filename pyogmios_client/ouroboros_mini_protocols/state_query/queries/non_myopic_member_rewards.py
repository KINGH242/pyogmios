from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    Lovelace,
    DigestBlake2bCredential,
    NonMyopicMemberRewards,
    StakeAddress,
)
from pyogmios_client.models.response_model import NonMyopicMemberRewardsResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_non_myopic_member_rewards(response: NonMyopicMemberRewardsResponse) -> bool:
    """
    Check if the given response is a NonMyopicMemberRewards.
    :param response: The response to check.
    :return: True if the response is a NonMyopicMemberRewards, False otherwise.
    """
    result = response.result
    if isinstance(result, NonMyopicMemberRewards):
        return True
    return False


async def non_myopic_member_rewards(
    context: InteractionContext,
    input_list: List[Lovelace] | List[DigestBlake2bCredential] | List[StakeAddress],
) -> NonMyopicMemberRewards:
    """
    Query the non-myopic member rewards for the given stake key hashes.
    :param context: The interaction context to use for the query.
    :param input_list: The stake key hashes to query.
    :return: The non-myopic member rewards for the given stake key hashes.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={"query": {"nonMyopicMemberRewards": input_list}},
    )

    try:
        response = await query(request_args, context)
        query_response = NonMyopicMemberRewardsResponse(**response.dict())
        result = query_response.result
        if result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("nonMyopicMemberRewards")
        elif is_non_myopic_member_rewards(query_response):
            return result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
