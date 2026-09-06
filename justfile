uv := require("uv")
uvx := require("uvx")
version := `uv version --short`
source_distribution := "dist/pylabrat-" + version + ".tar.gz"
wheel := "dist/pylabrat-" + version + "-py3-none-any.whl"

default:
    @just --list

[group("python")]
build-py:
    "{{ uv }}" build --no-sources --clear

[group("python")]
check-py: build-py
    "{{ uvx }}" twine check "{{ source_distribution }}" "{{ wheel }}"

[group("python")]
publish-test-pypi: check-py
    TWINE_USERNAME=__token__ "{{ uvx }}" twine upload \
        --repository testpypi "{{ source_distribution }}" "{{ wheel }}"

[group("python")]
publish-pypi: check-py
    TWINE_USERNAME=__token__ "{{ uvx }}" twine upload \
        "{{ source_distribution }}" "{{ wheel }}"
