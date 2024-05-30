import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from tests.utils.project import (
    generate_project,
    initialize_git_repo,
)


@pytest.fixture(scope="session")
def project_dir() -> Path:
    # Setup
    test_session_id: str = generate_test_session_id()
    template_values = {
        "repo_name": f"test-repo-{test_session_id}",
    }

    # generate a project using cookiecutter template
    generated_project_dir: Path = generate_project(
        template_values=template_values,
        test_session_id=test_session_id,
    )

    try:
        # initialize a git repository in the generated project directory for pre-commit-config.yaml to work
        initialize_git_repo(repo_dir=generated_project_dir)

        # The subprocess is being used to run the command "make lint-ci" in the generated project directory.
        # The check parameter is set to False because the command is expected to fail due to formatting errors.
        # However, it will also fix any formatting errors that can be automatically fixed.
        # The purpose is to catch any non-automatable fixes in a later test.
        subprocess.run(
            ["make", "lint-ci"],
            cwd=generated_project_dir,  # This will make the command run in the project directory.
            check=False,  # we expect this to fail due to formatting errors
        )

        yield generated_project_dir
    finally:
        # Teardown
        shutil.rmtree(generated_project_dir)


def generate_test_session_id() -> str:
    """Generate a unique session id for the test session."""
    test_session_id = str(uuid4())[:6]
    return test_session_id
