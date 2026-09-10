# Local Strands demo / ローカルAIでのデモ

The organizer permits any model with Strands. This optional route uses an already installed Ollama model on the same computer. It adds no AWS calls and never falls back to Bedrock. It still uses the real Strands SDK and guarded action tools. Actual Ollama inference has **not** been verified on the owner's Mac by this update.

主催者は特定モデルを指定していません。この経路は、同じPC内のOllamaとStrandsを使います。AWSに自動切替えはしません。Macでの実推論は今回まだ確認していません。

## 1. Check an existing model without generation / 既存モデルの確認

The simplest check discovers installed models automatically:

```bash
python3 src/check_local_setup.py
```

Run from the downloaded repository root on your Mac. This standard-library-only helper reads the [Ollama model list](https://docs.ollama.com/api/tags) and checks at most eight valid local model names using the same metadata checks as the live route. It checks the pinned Python package versions without importing or invoking a model. Once the packages and at least one candidate are verified, it prints safely quoted commands containing the actual model name and project path; choose one. A zero exit code means metadata/packages checked, not successful inference. Unreachable services, malformed responses, absent tools support, or missing packages remain incomplete. The helper never runs a command, installs packages, downloads a model, writes a report, changes settings, or falls back to AWS.

Macで上の1行を実行すると、モデル名を自分で調べずに準備確認できます。確認済みの候補があれば、実行コマンドを表示します。「確認必要」は実行条件がまだそろっていない意味です。Ollamaに接続できない場合は、MacでOllamaを開き、同じ確認を再実行します。ライブラリが不足する場合は下の手順2を済ませ、仮想環境のPythonで再確認します。まだモデルを追加購入する必要はありません。

If more than eight models are present, excess names are reported as unchecked; check a known model directly with the command below. Model-list and per-model requests each time out after ten seconds. The helper prints progress between checks. It cannot reach the owner's Mac from a separate Codex workspace; it must run on the computer hosting Ollama.

### Direct check of one named model

From the project root on the computer where Ollama is already running:

```bash
python src/local_model.py --model-id YOUR_INSTALLED_MODEL
```

Replace `YOUR_INSTALLED_MODEL` with the exact name shown by `ollama list`. The metadata check needs only Python and the existing local Ollama server. It uses `http://127.0.0.1:11434/api/show`, sends only the model name, ignores proxy settings, refuses redirects, and does not call generation, pull a model, sign in, or modify the server. Success prints `local_metadata_ok: true`, `tools_supported: true`, and `inference_called: false`.

`YOUR_INSTALLED_MODEL`は、`ollama list` に表示される名前へ置き換えます。モデル名の照会だけで、生成・ダウンロード・ログイン・サーバー設定変更は行いません。画像が読めるモデルでもツール呼出しに対応するとは限りません。

The check requires local GGUF/parameter metadata and the advertised `tools` capability, rejects cloud model names and reported remote forwarding, and fails closed when metadata is insufficient. This assumes the owner's loopback server truthfully describes its models; it is not a network isolation or attestation system. For strict local-only operation, configure the Ollama server's [local-only mode](https://docs.ollama.com/cloud) before using this route. No private care data belongs in this prototype.

ローカルモデルの形式・パラメータ情報と `tools` 対応を確認します。未対応なら止まります。照会に失敗しても、別モデルを勝手に追加したり、有料モデルへ切り替えたりしません。

## 2. Install optional Python support / 接続ライブラリを用意

Use the project virtual environment described in README:

```bash
python -m pip install -r requirements-local.txt
```

This downloads Python packages only. No model weights are downloaded. If the environment uses a SOCKS proxy, its HTTPX proxy support must already be configured; a dependency/import error must be resolved locally before a demo can succeed.

ダウンロードするのはPythonライブラリです。AIモデル本体の追加は行いません。

## 3. Run the synthetic live agent / 模擬入力で実際のAIを動かす

```bash
python src/demo.py --mode live --provider ollama --model-id YOUR_INSTALLED_MODEL
```

Each event gets a fresh Strands agent, a checked local model, the same no-argument guarded tools, and a two-model-cycle limit. The client uses loopback only, no proxy environment, no redirects, and a finite request timeout. The application does not fall back to another provider. Local CPU/GPU and electricity are used; actual latency depends on hardware/model. A timeout or invalid tool response means an incomplete run, not success.

各ケースでモデル対応を確認し、Strandsから安全な処理を1回だけ呼びます。ローカルPCの計算資源を使います。時間切れや不正なツール応答を、成功として扱いません。

Expected successful report: `verified: true`, `is_live_agent_evidence: true`, `model_provider: ollama`, and `bedrock_called: false` in all three cases. Open its `report.html`; the banner must say **Live local model via Strands**. The legacy `is_live_evidence` field remains Bedrock-only and is correctly false on a local-model run. Metadata success alone is not inference success, and scripted-model tests are not actual Ollama evidence.

成功時は日英の結果画面に「ローカルAIで実行」と表示されます。モデル情報の確認成功と、3ケースの動作成功は別です。`--mode offline` はAIを呼ばない練習用です。

## Remaining boundary / 残る確認

The same public synthetic samples are used on both provider routes. This does not test a camera, clinical accuracy, caregiver approval UI, or constant monitoring. For the hackathon video, show an actual successful Strands/model run and keep the mode banner visible. Review logs before retrying a failed run; some writes may already have happened.

両経路とも安全な模擬データを使います。実機カメラ・医療精度・常時監視の検証とは別です。動画では、実際に成功したStrandsの動作と実行方式を示してください。
