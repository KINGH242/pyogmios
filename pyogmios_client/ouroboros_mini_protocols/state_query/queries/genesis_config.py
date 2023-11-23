from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName, EraWithGenesis
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import (
    GenesisConfig,
    GenesisByron,
    GenesisShelley,
    GenesisAlonzo,
    EraMismatch,
    QueryUnavailableInCurrentEra,
)
from pyogmios_client.models.response_model import GenesisConfigResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_genesis_config(response: GenesisConfigResponse) -> bool:
    """
    Check if the response is a genesis config response.
    :param response: The response to check.
    :return: True if the response is a genesis config response, False otherwise.
    """
    result = response.result
    return isinstance(result, (GenesisByron, GenesisShelley, GenesisAlonzo))


async def genesis_config(
    context: InteractionContext, era: EraWithGenesis
) -> GenesisConfig:
    """
    Query the genesis config.
    :param context: The interaction context to use for the query.
    :param era: The era to query the genesis config for.
    :return: The genesis config.
    """
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={"query": {"genesisConfig": str(era.value).lower()}},
    )

    try:
        response = await query(request_args, context)
        query_response = GenesisConfigResponse(**response.model_dump())
        result = query_response.result
        if isinstance(result, QueryUnavailableInCurrentEra):
            raise QueryUnavailableInCurrentEraError("genesisConfig")
        elif isinstance(result, (GenesisByron, GenesisShelley, GenesisAlonzo)):
            return query_response.result
        elif isinstance(result, EraMismatch):
            raise EraMismatchError(result.queryEra.value, result.ledgerEra.value)
        else:
            raise UnknownResultError(response)
    except Exception as error:
        raise error
