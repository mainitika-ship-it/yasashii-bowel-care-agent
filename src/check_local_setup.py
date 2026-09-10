"""Read-only local model discovery; never generate, download, or change settings."""
from __future__ import annotations

import importlib.metadata
import json
import shlex
import sys
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

from local_model import LOCAL_HOST, NoRedirect, inspect_local_model, validate_model_id

ROOT = Path(__file__).resolve().parents[1]
MAX_MODELS = 8
EXPECTED_PACKAGES = {"strands-agents": "1.55.1", "boto3": "1.43.91", "ollama": "0.6.2"}


def discover_models() -> tuple[list[str], int]:
    """List at most eight valid names using metadata only, never follow redirects."""
    request = Request(LOCAL_HOST + "/api/tags", method="GET")
    opener = build_opener(ProxyHandler({}), NoRedirect())
    with opener.open(request, timeout=10) as response:
        payload = response.read(2_000_001)
    if len(payload) > 2_000_000:
        raise ValueError("model list exceeds check limit")
    data = json.loads(payload)
    if not isinstance(data, dict) or not isinstance(data.get("models"), list):
        raise ValueError("model list is malformed")
    names, skipped = set(), 0
    for item in data["models"]:
        try:
            name = validate_model_id(item.get("name") if isinstance(item, dict) else None)
        except ValueError:
            skipped += 1
            continue
        names.add(name)
    ordered = sorted(names)
    return ordered[:MAX_MODELS], skipped + max(0, len(ordered) - MAX_MODELS)


def missing_dependencies() -> list[str]:
    missing = []
    for package, expected in EXPECTED_PACKAGES.items():
        try:
            if importlib.metadata.version(package) != expected:
                missing.append(package)
        except importlib.metadata.PackageNotFoundError:
            missing.append(package)
    return missing


def demo_command(model_id: str, python: str = sys.executable) -> str:
    # Model names come from a server; validate and quote before suggesting shell text.
    return shlex.join([python, str(ROOT / "src/demo.py"), "--mode", "live",
                       "--provider", "ollama", "--model-id", validate_model_id(model_id)])


def main() -> int:
    print("1. 読み取り専用の準備確認 / Read-only setup check", flush=True)
    print("AI生成・モデル追加・AWS接続・設定変更は行いません。", flush=True)
    missing = missing_dependencies()
    print("2. Python環境 / Python packages: " + ("準備が必要" if missing else "指定版を確認"), flush=True)
    try:
        names, skipped = discover_models()
    except Exception:
        # No raw exception, endpoint response, or local configuration is printed.
        print("3. Ollamaのモデル一覧を確認できません / Model list unavailable")
        print("次：このMacでOllamaを開いてから、同じ確認コマンドを再実行してください。")
        print("起動済みならローカル接続を確認してください。実推論は未確認です。")
        return 1
    print(f"3. 既存モデルを確認 / Checking {len(names)} models", flush=True)
    candidates = []
    for name in names:
        print(f"  {name}: ", end="", flush=True)
        try:
            inspect_local_model(name)
        except Exception:
            print("確認必要：接続・ローカル形式・ツール対応のいずれかが未確認", flush=True)
        else:
            candidates.append(name)
            print("実行候補 / metadata OK (inference not tested)", flush=True)
    if skipped:
        print(f"  確認対象外 {skipped} 件（クラウド名・不正形式・上限超過）。最大{MAX_MODELS}件を確認。")
    if not candidates:
        print("4. 実行候補を確認できませんでした / No verified candidate")
        print("次：この確認結果を共有してください。モデルの追加購入・ダウンロードはまだ不要です。")
        return 1
    interpreter = sys.executable
    if missing:
        print("4. 接続ライブラリの準備が必要 / Python setup needed: " + ", ".join(missing))
        print("次：READMEの仮想環境を使い、requirements-local.txtをインストールしてください。")
        print("ライブラリ準備後に同じ確認コマンドを実行してください。")
        return 1
    print("4. 次に実行するコマンド / Choose ONE command below", flush=True)
    for name in candidates:
        print(demo_command(name, interpreter))
    print("5. 準備確認まで完了。実推論・3ケース成功・提出はまだです。")
    print("Metadata checked only; no inference, downloads, or submission performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
