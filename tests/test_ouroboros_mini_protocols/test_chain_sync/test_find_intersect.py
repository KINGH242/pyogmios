import pytest

from pyogmios_client.connection import (
    create_interaction_context,
)
from pyogmios_client.enums import MethodName, Type, Version, ServiceName
from pyogmios_client.exceptions import IntersectionNotFoundError
from pyogmios_client.models import Origin
from pyogmios_client.models.response_model import Response, QueryResponseReflection
from pyogmios_client.models.result_models import (
    IntersectionFound,
    IntersectionNotFound,
    FindIntersectResult,
)
from pyogmios_client.ouroboros_mini_protocols.chain_sync.find_intersect import (
    find_intersect,
)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "IntersectionFound": {
                    "point": {
                        "slot": 18446744073709552000,
                        "hash": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                    },
                    "tip": {
                        "slot": 18446744073709552000,
                        "hash": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                        "blockNo": 18446744073709552000,
                    },
                }
            },
            IntersectionFound,
        ),
        (
            {"IntersectionFound": {"point": "origin", "tip": "origin"}},
            IntersectionFound,
        ),
    ],
)
@pytest.mark.asyncio
async def test_find_intersect_success(mocker, test_input, expected):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.chain_sync.find_intersect.query",
        return_value=Response(
            type=Type.JSONWSP_RESPONSE,
            version=Version.v1_0,
            servicename=ServiceName.OGMIOS,
            methodname=MethodName.FIND_INTERSECT,
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=FindIntersectResult(**test_input),
        ),
    )
    context = await create_interaction_context()
    points = [Origin()]

    # Act
    result = await find_intersect(context, points)

    # Assert
    assert isinstance(result, expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "IntersectionNotFound": {
                    "tip": {
                        "slot": 18446744073709552000,
                        "hash": "c248757d390181c517a5beadc9c3fe64bf821d3e889a963fc717003ec248757d",
                        "blockNo": 18446744073709552000,
                    }
                }
            },
            IntersectionNotFound,
        ),
        ({"IntersectionNotFound": {"tip": "origin"}}, IntersectionNotFound),
    ],
)
@pytest.mark.asyncio
async def test_find_intersect_fail(mocker, test_input, expected):
    mocker.patch(
        "pyogmios_client.ouroboros_mini_protocols.chain_sync.find_intersect.query",
        return_value=Response(
            type=Type.JSONWSP_RESPONSE,
            version=Version.v1_0,
            servicename=ServiceName.OGMIOS,
            methodname=MethodName.FIND_INTERSECT,
            reflection=QueryResponseReflection(requestId="test-request-id"),
            result=FindIntersectResult(**test_input),
        ),
    )
    context = await create_interaction_context()
    points = [Origin()]

    # Act
    with pytest.raises(IntersectionNotFoundError):
        result = await find_intersect(context, points)

        # Assert
        assert isinstance(result, expected)
