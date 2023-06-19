from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
)
from pyogmios_client.models import RewardsProvenance
from pyogmios_client.models.response_model import RewardsProvenanceResponse
from pyogmios_client.models.result_models import EraMismatchResult
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_rewards_provenance(response: RewardsProvenanceResponse) -> bool:
    """
    Check if the response is a rewards provenance.
    :param response: The response to check.
    :return: True if the response is a rewards provenance, False otherwise.
    """
    result = response.result
    if isinstance(result, RewardsProvenance):
        return True
    return False


async def rewards_provenance(context: InteractionContext) -> RewardsProvenance:
    """
    Query the rewards provenance.
    :param context: The interaction context to use for the query.
    :return: The rewards provenance.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "rewardsProvenance"}
    )

    try:
        response = await query(request_args, context)
        query_response = RewardsProvenanceResponse(**response.dict())
        result = query_response.result
        if result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("rewardsProvenance")
        elif is_rewards_provenance(query_response):
            return result
        elif isinstance(result, EraMismatchResult):
            era_mismatch = result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            return result
    except Exception as error:
        raise error
