"""Validate a GitHub repository to be used with RACELANDSHOP."""
import asyncio
import json
import os

import aiohttp
from aiogithubapi import GitHub
from homeassistant.core import HomeAssistant

from custom_components.racelandshop.const import RACELANDSHOP_ACTION_GITHUB_API_HEADERS
from custom_components.racelandshop.racelandshopbase.configuration import Configuration
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.functions.logger import getLogger
from custom_components.racelandshop.helpers.functions.register_repository import (
    register_repository,
)
from custom_components.racelandshop.share import get_racelandshop

TOKEN = os.getenv("INPUT_GITHUB_TOKEN")
GITHUB_WORKSPACE = os.getenv("GITHUB_WORKSPACE")
GITHUB_ACTOR = os.getenv("GITHUB_ACTOR")
GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
CHANGED_FILES = os.getenv("CHANGED_FILES", "")


REPOSITORY = os.getenv("REPOSITORY", os.getenv("INPUT_REPOSITORY"))
CATEGORY = os.getenv("CATEGORY", os.getenv("INPUT_CATEGORY", ""))


CATEGORIES = [
    "appdaemon",
    "integration",
    "netdaemon",
    "plugin",
    "python_script",
    "theme",
]

logger = getLogger()


def error(error: str):
    logger.error(error)
    exit(1)


def get_event_data():
    if GITHUB_EVENT_PATH is None or not os.path.exists(GITHUB_EVENT_PATH):
        return {}
    with open(GITHUB_EVENT_PATH) as ev:
        return json.loads(ev.read())


def chose_repository(category):
    if category is None:
        return
    with open(f"/default/{category}") as cat_file:
        current = json.loads(cat_file.read())
    with open(f"{GITHUB_WORKSPACE}/{category}") as cat_file:
        new = json.loads(cat_file.read())

    for repo in current:
        if repo in new:
            new.remove(repo)

    if len(new) != 1:
        error(f"{new} is not a single repository")

    return new[0]


def chose_category():
    for name in CHANGED_FILES.split(" "):
        if name in CATEGORIES:
            return name


async def preflight():
    """Preflight checks."""
    logger.warning(
        "This action is deprecated. Use https://github.com/racelandshop/action instead"
    )
    event_data = get_event_data()
    ref = None
    if REPOSITORY and CATEGORY:
        repository = REPOSITORY
        category = CATEGORY
        pr = False
    elif GITHUB_REPOSITORY == "racelandshop/default":
        category = chose_category()
        repository = chose_repository(category)
        pr = False
        logger.info(f"Actor: {GITHUB_ACTOR}")
    else:
        category = CATEGORY.lower()
        pr = True if event_data.get("pull_request") is not None else False
        if pr:
            head = event_data["pull_request"]["head"]
            ref = head["ref"]
            repository = head["repo"]["full_name"]
        else:
            repository = GITHUB_REPOSITORY

    logger.info(f"Category: {category}")
    logger.info(f"Repository: {repository}")

    if TOKEN is None:
        error("No GitHub token found, use env GITHUB_TOKEN to set this.")

    if repository is None:
        error("No repository found, use env REPOSITORY to set this.")

    if category is None:
        error("No category found, use env CATEGORY to set this.")

    async with aiohttp.ClientSession() as session:

        github = GitHub(TOKEN, session, headers=RACELANDSHOP_ACTION_GITHUB_API_HEADERS)
        repo = await github.get_repo(repository)
        if not pr and repo.description is None:
            error("Repository is missing description")
        if not pr and not repo.attributes["has_issues"]:
            error("Repository does not have issues enabled")
        if ref is None and GITHUB_REPOSITORY != "racelandshop/default":
            ref = repo.default_branch

    await validate_repository(repository, category, ref)


async def validate_repository(repository, category, ref=None):
    """Validate."""
    async with aiohttp.ClientSession() as session:
        racelandshop = get_racelandshop()
        racelandshop.hass = HomeAssistant()
        racelandshop.session = session
        racelandshop.configuration = Configuration()
        racelandshop.configuration.token = TOKEN
        racelandshop.core.config_path = None
        racelandshop.github = GitHub(
            racelandshop.configuration.token,
            racelandshop.session,
            headers=RACELANDSHOP_ACTION_GITHUB_API_HEADERS,
        )
        try:
            await register_repository(repository, category, ref=ref)
        except RacelandshopException as exception:
            error(exception)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(preflight())
