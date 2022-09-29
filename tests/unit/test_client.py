from unittest.mock import patch

import pytest
from requests.exceptions import ReadTimeout

from solana.exceptions import SolanaRpcException
from solana.publickey import PublicKey
from solana.rpc.commitment import Finalized


def test_client_http_exception(unit_test_http_client):
    """Test AsyncClient raises native Solana-py exceptions."""

    with patch("requests.post") as post_mock:
        post_mock.side_effect = ReadTimeout()
        with pytest.raises(SolanaRpcException) as exc_info:
            unit_test_http_client.get_epoch_info()
        assert exc_info.type == SolanaRpcException
        assert (
            exc_info.value.error_msg
            == "<class 'requests.exceptions.ReadTimeout'> raised in \"getEpochInfo\" endpoint request"
        )


def test_client_address_sig_args_no_commitment(unit_test_http_client):
    expected = (
        "getSignaturesForAddress",
        "11111111111111111111111111111111",
        {"before": "before", "until": "until", "limit": 5},
    )
    actual = unit_test_http_client._get_signatures_for_address_args(PublicKey(0), "before", "until", 5, None)
    assert expected == actual


def test_client_address_sig_args_with_commitment(unit_test_http_client):
    expected = (
        "getSignaturesForAddress",
        "11111111111111111111111111111111",
        {"limit": 5, "commitment": "finalized"},
    )
    actual = unit_test_http_client._get_signatures_for_address_args(PublicKey(0), None, None, 5, Finalized)
    assert expected == actual
