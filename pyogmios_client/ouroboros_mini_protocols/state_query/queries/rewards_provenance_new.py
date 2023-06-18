from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
)
from pyogmios_client.models import EraMismatch, RewardsProvenanceNew
from pyogmios_client.models.response_model import RewardsProvenanceNewResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: RewardsProvenanceNewResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_rewards_provenance_new(response: RewardsProvenanceNewResponse) -> bool:
    result = response.result
    if isinstance(result, RewardsProvenanceNew):
        return True
    return False


async def rewards_provenance_new(context: InteractionContext) -> RewardsProvenanceNew:
    request_args = RequestArgs(
        method_name=MethodName.QUERY, args={"query": "rewardsProvenance'"}
    )

    try:
        response = await query(request_args, context)
        query_response = RewardsProvenanceNewResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("rewardsProvenance'")
        elif is_rewards_provenance_new(query_response):
            return query_response.result
        elif is_era_mismatch(query_response):
            era_mismatch = response.result.eraMismatch
            raise EraMismatchError(
                str(era_mismatch.queryEra), str(era_mismatch.ledgerEra)
            )
        else:
            return query_response.result
    except Exception as error:
        raise error
