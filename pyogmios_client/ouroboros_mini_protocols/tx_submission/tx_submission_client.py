from typing import Callable, Optional, Coroutine, Any, List

from pyogmios_client.connection import InteractionContext
from pyogmios_client.models import BaseModel, Utxo, TxId
from pyogmios_client.models.generated import EvaluationResult
from pyogmios_client.models.response_model import (
    SubmitTxResponse,
    Response,
    EvaluateTxResponse,
)
from pyogmios_client.ouroboros_mini_protocols.tx_submission.evaluate_tx import (
    evaluate_tx,
)
from pyogmios_client.ouroboros_mini_protocols.tx_submission.submission_errors import (
    SubmitTxErrorShelley,
)
from pyogmios_client.ouroboros_mini_protocols.tx_submission.submit_tx import submit_tx
from pyogmios_client.utils.socket_utils import ensure_socket_is_open


class TxSubmissionClient(BaseModel):
    context: InteractionContext
    evaluate_tx: Callable[
        [str, Utxo], Coroutine[Any, Any, EvaluationResult | List[Exception]]
    ]
    submit_tx: Callable[[str], Coroutine[Any, Any, TxId | List[SubmitTxErrorShelley]]]
    shutdown: Callable[[], Coroutine[Any, Any, None]]


def match_submit_tx(response: Response) -> SubmitTxResponse | None:
    """
    Check if is a submit tx response.
    :param response: The response
    :return: The submit tx response
    """
    if isinstance(response, SubmitTxResponse):
        return response
    return None


def match_evaluate_tx(response: Response) -> EvaluateTxResponse | None:
    """
    Check if is an evaluate tx response.
    :param response: The response
    :return: The evaluate tx response
    """
    if isinstance(response, EvaluateTxResponse):
        return response
    return None


async def create_tx_submission_client(
    context: InteractionContext,
) -> TxSubmissionClient:
    """
    Creates a tx submission client.
    :param context: The interaction context
    :return: The tx submission client
    """
    websocket_app = context.socket

    try:

        async def default_submit_tx(bytes_: str) -> TxId | List[SubmitTxErrorShelley]:
            """
            Submit a transaction.
            :param bytes_: The bytes
            :return: The tx id
            """
            await ensure_socket_is_open(context.socket)
            return await submit_tx(context, bytes_)

        async def default_evaluate_tx(
            bytes_: str, additional_utxo_set: Optional[Utxo] = None
        ) -> EvaluationResult | List[Exception]:
            """
            Evaluate a transaction.
            :param bytes_: The bytes
            :param additional_utxo_set: The additional utxo set
            :return: The evaluation result
            """
            await ensure_socket_is_open(context.socket)
            return await evaluate_tx(context, bytes_, additional_utxo_set)

        async def shutdown() -> None:
            """
            Shutdown the tx submission client.
            """
            try:
                await ensure_socket_is_open(websocket_app)
                websocket_app.close()
            except Exception as err:
                print(err)
            else:
                print("Shutting down TxSubmission Client...")

        return TxSubmissionClient(
            context=context,
            shutdown=shutdown,
            evaluate_tx=default_evaluate_tx,
            submit_tx=default_submit_tx,
        )
    except Exception as e:
        print(e)
