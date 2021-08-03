"""Helpers: Information: get_repository."""
# pylint: disable=missing-docstring
import json

import pytest

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.functions.validate_repository import common_validate
from custom_components.racelandshop.share import get_removed
from tests.sample_data import (
    release_data,
    repository_data,
    repository_data_archived,
    response_rate_limit_header,
    response_rate_limit_header_with_limit,
    tree_files_base,
)


@pytest.mark.asyncio
async def test_common_base(racelandshop, repository, aresponses):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test",
        "get",
        aresponses.Response(
            body=json.dumps(repository_data), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/releases",
        "get",
        aresponses.Response(
            body=json.dumps(release_data), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/git/trees/3",
        "get",
        aresponses.Response(
            body=json.dumps(tree_files_base), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/contents/racelandshop.json",
        "get",
        aresponses.Response(
            body=json.dumps({"name": "test"}), headers=response_rate_limit_header
        ),
    )
    repository.ref = None
    repository.racelandshop = racelandshop

    await common_validate(repository)


@pytest.mark.asyncio
async def test_get_releases_exception(repository, aresponses):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test",
        "get",
        aresponses.Response(
            body=json.dumps(repository_data), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(
            body=json.dumps({"message": "X"}),
            headers=response_rate_limit_header_with_limit,
            status=403,
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/git/trees/3",
        "get",
        aresponses.Response(
            body=json.dumps(tree_files_base), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/contents/racelandshop.json",
        "get",
        aresponses.Response(body=json.dumps({}), headers=response_rate_limit_header),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/releases",
        "get",
        aresponses.Response(
            body=json.dumps(release_data),
            headers=response_rate_limit_header_with_limit,
            status=403,
        ),
    )
    repository.ref = None
    await common_validate(repository)
    assert not repository.data.releases


@pytest.mark.asyncio
async def test_common_archived(repository, aresponses):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test",
        "get",
        aresponses.Response(
            body=json.dumps(repository_data_archived()),
            headers=response_rate_limit_header,
        ),
    )
    repository.data.archived = True
    with pytest.raises(RacelandshopException):
        await common_validate(repository)


@pytest.mark.asyncio
async def test_common_blacklist(repository, aresponses):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test",
        "get",
        aresponses.Response(
            body=json.dumps(repository_data), headers=response_rate_limit_header
        ),
    )
    removed = get_removed("test/test")
    assert removed.repository == "test/test"
    with pytest.raises(RacelandshopException):
        await common_validate(repository)


@pytest.mark.asyncio
async def test_common_base_exception_does_not_exsist(racelandshop, repository, aresponses):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(headers=response_rate_limit_header_with_limit, status=500),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test",
        "get",
        aresponses.Response(
            body=json.dumps({"message": "X"}),
            headers=response_rate_limit_header_with_limit,
            status=500,
        ),
    )
    racelandshop.status.startup = False
    with pytest.raises(RacelandshopException):
        await common_validate(repository)


@pytest.mark.asyncio
async def test_common_base_exception_tree_issues(repository, aresponses, racelandshop):
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test",
        "get",
        aresponses.Response(
            body=json.dumps(repository_data), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/releases",
        "get",
        aresponses.Response(
            body=json.dumps(release_data), headers=response_rate_limit_header
        ),
    )
    aresponses.add(
        "api.github.com",
        "/rate_limit",
        "get",
        aresponses.Response(body=b"{}", headers=response_rate_limit_header, status=200),
    )
    aresponses.add(
        "api.github.com",
        "/repos/test/test/git/trees/3",
        "get",
        aresponses.Response(
            body=json.dumps({"message": "X"}), headers=response_rate_limit_header
        ),
    )
    racelandshop.status.startup = False
    with pytest.raises(RacelandshopException):
        await common_validate(repository)
