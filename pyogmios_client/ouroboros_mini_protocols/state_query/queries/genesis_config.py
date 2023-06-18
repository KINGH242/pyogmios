from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName, EraWithGenesis
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    EraMismatch,
    GenesisConfig,
    GenesisByron,
    GenesisShelley,
    GenesisAlonzo,
)
from pyogmios_client.models.response_model import GenesisConfigResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: GenesisConfigResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_genesis_config(response: GenesisConfigResponse) -> bool:
    result = response.result
    if isinstance(result, GenesisByron):
        return result.initialCoinOffering is not None
    elif isinstance(result, GenesisShelley):
        return result.initialPools is not None
    elif isinstance(result, GenesisAlonzo):
        return result.costModels is not None


async def genesis_config(
    context: InteractionContext, era: EraWithGenesis
) -> GenesisConfig:
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={"query": {"genesisConfig": str(era.value).lower()}},
    )

    try:
        response = await query(request_args, context)
        query_response = GenesisConfigResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("genesisConfig")
        elif is_genesis_config(query_response):
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
