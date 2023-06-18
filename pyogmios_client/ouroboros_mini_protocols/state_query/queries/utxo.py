from typing import List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.enums import MethodName
from pyogmios_client.exceptions import (
    QueryUnavailableInCurrentEraError,
    EraMismatchError,
    UnknownResultError,
)
from pyogmios_client.models import EraMismatch, Address, TxIn, Utxo
from pyogmios_client.models.response_model import UtxoResponse
from pyogmios_client.ouroboros_mini_protocols.state_query.query import (
    query,
    RequestArgs,
)


def is_era_mismatch(response: UtxoResponse) -> bool:
    if isinstance(response, EraMismatch):
        return response.eraMismatch is not None


def is_utxo_list(response: UtxoResponse) -> bool:
    result = response.result
    if isinstance(result, Utxo):
        return True
    return False


async def utxo(
    context: InteractionContext, filters: List[Address] | List[TxIn]
) -> Utxo:
    request_args = RequestArgs(
        method_name=MethodName.QUERY,
        args={
            "query": {"utxo": filters}
            if isinstance(filters, List) and len(filters) > 0
            else "utxo"
        },
    )

    try:
        response = await query(request_args, context)
        query_response = UtxoResponse(**response.dict())
        if query_response.result == "QueryUnavailableInCurrentEra":
            raise QueryUnavailableInCurrentEraError("utxo")
        elif is_utxo_list(query_response):
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
