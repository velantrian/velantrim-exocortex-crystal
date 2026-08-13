from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import venv

import pytest


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "eval/reader_nli_neutral_filter_v1_requirements.txt"
RUNNER = ROOT / "scripts/bench_reader_nli_neutral_filter_v1.py"
DEPENDENCY_SHA = "9a2902d1b7d5b7ca5b5105be46d1a1151fddf683e0ed67b078a09c948b3f4bd9"
SEMANTIC_SHA = "eaa086f0ffee582aeb45b36e34cdd1fe2d6de2bef61f8a559a1bbc9bd955917b"
NLI_SHA = "91b323ccf247ec1e3b5925d566230bae7c52de8147e6062b42e250089a3fc80b"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS") != "true" or sys.version_info[:2] != (3, 11),
    reason="qualifying model run is intentionally single-run on GitHub Actions Python 3.11",
)
def test_preregistered_qualifying_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    env_dir = tmp_path / "exact-env"
    venv.EnvBuilder(with_pip=True, clear=True).create(env_dir)
    python_bin = env_dir / "bin/python"
    subprocess.run(
        [str(python_bin), "-m", "pip", "install", "-r", str(LOCK)],
        cwd=ROOT,
        check=True,
    )

    freeze_lines = subprocess.check_output(
        [str(python_bin), "-m", "pip", "freeze"], cwd=ROOT, text=True
    ).splitlines()
    dependency_file = tmp_path / "resolved-dependencies.txt"
    dependency_file.write_text("\n".join(sorted(freeze_lines)) + "\n", encoding="utf-8")
    assert _sha256(dependency_file) == DEPENDENCY_SHA
    assert dependency_file.read_text(encoding="utf-8") == LOCK.read_text(encoding="utf-8")

    semantic_dir = tmp_path / "semantic-model"
    nli_dir = tmp_path / "nli-model"
    preload = """
import os
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
    revision='e8f8c211226b894fcb81acc59f3b34ba3efd5f42',
    local_dir=os.environ['SEMANTIC_MODEL_DIR'],
    ignore_patterns=['onnx/*', 'openvino/*', '*.bin', '*.h5', '*.ot'],
)
snapshot_download(
    repo_id='MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli',
    revision='0a71e92a985b6e1ad1828cf67ce9c459639c1dca',
    local_dir=os.environ['NLI_MODEL_DIR'],
    ignore_patterns=['onnx/*', '*.bin'],
)
"""
    preload_env = os.environ.copy()
    preload_env["SEMANTIC_MODEL_DIR"] = str(semantic_dir)
    preload_env["NLI_MODEL_DIR"] = str(nli_dir)
    subprocess.run([str(python_bin), "-c", preload], cwd=ROOT, env=preload_env, check=True)
    assert _sha256(semantic_dir / "model.safetensors") == SEMANTIC_SHA
    assert _sha256(nli_dir / "model.safetensors") == NLI_SHA

    result_path = tmp_path / "reader-nli-neutral-filter-v1-result.json"
    command = [
        "sudo",
        "-E",
        "unshare",
        "--net",
        "env",
        "HF_HUB_OFFLINE=1",
        "TRANSFORMERS_OFFLINE=1",
        str(python_bin),
        str(RUNNER),
        "--semantic-model-path",
        str(semantic_dir),
        "--nli-model-path",
        str(nli_dir),
        "--dependencies",
        str(dependency_file),
        "--json-out",
        str(result_path),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert result["execution"]["repeatable"] is True
    assert result["execution"]["hf_hub_offline"] is True
    assert result["execution"]["transformers_offline"] is True
    assert result["authority"]["authority_violations"] == 0
    assert result["runtime_authorization"] is False

    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    with capsys.disabled():
        print("QUALIFYING_RESULT_JSON_BEGIN")
        print(payload)
        print("QUALIFYING_RESULT_JSON_END")
        print(f"QUALIFYING_RESULT_SHA256={_sha256(result_path)}")
        if completed.stdout:
            print("QUALIFYING_RUN_STDOUT_BEGIN")
            print(completed.stdout.strip())
            print("QUALIFYING_RUN_STDOUT_END")
