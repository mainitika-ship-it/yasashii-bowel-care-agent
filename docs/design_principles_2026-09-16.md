# Product pillars, implementation flow and evolution policy — 2026-09-16

This is a **post-submission documentation record**, including product goals recovered from an earlier project discussion. Its publication date does not mean that all of these goals originated after submission. It does **not** change the verified scope of the hackathon submission or claim that the future items below are implemented.

## やさしい要約 / Plain-language summary

**元の5柱は「何を実現したいか」。処理の5段階は「内部でどう動くか」。別のものです。**

- 元の5柱は、継続検出・自動統計・遠方への定期送付・小型で堅牢・段階的なイレギュラー対応。
- その後、ローカルAIで不確かな事例を調べ、正解データを蓄積して改善する方針が追加されている。
- 今回整理した7項目は、元の5柱を置き換える新しい柱ではなく、実現・運用する際の補足原則。
- 今までの介護・記録・申し送りに、システム側が寄り添う。
- 入力・転記・確認・申し送り・保全に必要な人の作業を、安全を保ちながら年月とともに減らすことを目指す。
- 安さだけを追わず、導入から日常使用、保全までの総負担とストレスを小さくする。

> **今ある介護に寄り添い、人の判断を残しながら、人がしなければならない仕事を年月とともに減らしていく。**

> **Yasashii should fit the care already being given, preserve human judgment, and make the amount of work people must do smaller over time.**

## 1. 元の5柱 / Earlier five product pillars

Source: retrieved conversation summaries for the owner-identified discussion **「Codex再開依頼作成」**. The indexed owner statement is dated **2026-09-13 16:02:47 UTC / 2026-09-14 01:02:47 JST**, followed by an assistant restatement of the five pillars. The entries below are **paraphrases of the retrieved conversation record, not verbatim quotations from a complete transcript**. They are not reconstructed from the current implementation diagram.

| ID | 元の方針の要約 | English meaning |
|---|---|---|
| P1 | 排便を漏れなく検出し続けることを目指す。 | Aim for continuous bowel-event detection without missed events. |
| P2 | 自動検出・統計。人・時間・量を扱い、概略でよい。 | Automate detection and statistics, including person, time and approximate amount. |
| P3 | 遠方の人へ定期的に送付する。 | Send information periodically to people supporting care remotely. |
| P4 | 小型・パソコンは最小限・単純で堅牢にする。 | Keep the system compact, minimize PC dependence, and favor simplicity and robustness. |
| P5 | 段階的にイレギュラーへ対応できるようにする。 | Improve handling of irregular cases progressively. |

These are **product goals**, not verified capabilities. P1 is not a guarantee of zero missed events. P2 does not establish validated person identification or amount measurement; do not invent an identity or replace unknown data with a guess. Automatic records support the statistics and handoff goals; the earlier assistant restatement described detection → recording → statistics.

### 同じ過去会話で確認できた追加方針 / Recovered subsequent addition

The retrieved owner statement indexed at **2026-09-13 16:11:08 UTC / 2026-09-14 01:11:08 JST** adds a **local-AI improvement direction**: detect irregular cases, analyze UNCERTAIN cases, accumulate correctly labelled examples, and improve accuracy through measurement, comparison, failure analysis, modification and re-verification. The method was not fixed. Uncontrolled self-updating was not the intended approach.

The assistant's subsequent implementation proposal described an improvement loop:

**capture → primary detection → local-AI review → preserve evidence → human review and labels → offline evaluation → candidate update → regression tests → controlled adoption**.

This loop is an **implementation proposal following the owner's direction**, not evidence that the full loop is already implemented. It must not turn an uncertain observation into a confirmed result merely because a model reviewed it. These summaries recover the five goals and this subsequent addition; they do not establish an exhaustive inventory of every historical “plus alpha” item.

## 2. Separate implementation flow — unchanged

The current documented workflow in [architecture.md](architecture.md) remains the technical flow:

1. **Input** — accept a prepared observation input.
2. **QC** — apply fixed checks for signal, privacy flag, event type, confidence and relative amount.
3. **Strands Agents SDK** — select an allowed action.
4. **Guarded tools** — reject wrong actions, invented values and unsafe/repeated writes within the documented guard scope.
5. **Handoff** — include only normal PASS observations; keep HOLD requests and STOP alerts separate.

**These five implementation stages are not the owner's five product pillars.** Sharing the number five does not make the frameworks equivalent. The current duplicate-write guard covers one event execution, not protection across process restarts.

The safety policy also remains unchanged:

- **PASS — Record**
- **HOLD — Ask a person**
- **STOP — Stop & alert**
- **AI helps. People decide.**

## 3. How the later seven review items relate

The later seven-item grouping is a **cross-cutting design and operating checklist**, not a replacement for either the original product goals or the existing implementation flow.

Keep the distinctions clear:

- **Original five product pillars:** what the system is intended to achieve.
- **Recovered local-AI improvement direction:** a subsequent addition that particularly supports progressive exception handling.
- **Later seven review items:** how to build and operate the system with less burden on people.
- **Five implementation stages:** how the documented submitted prototype currently processes prepared inputs.

Do not rename, renumber or replace historical pillars merely to make a new explanation look tidy. Record later additions with their source, relationship to existing goals, and implementation/evidence status.

### Correction history — 2026-09-16

Earlier versions of this note emphasized “five-step implementation spine + plus alpha” before the original product pillars had been recovered. That wording was insufficient to answer the owner's question about the historical five pillars. This revision restores the recovered goals above and explicitly separates goals, operating principles and implementation stages. Earlier file versions remain in Git history.

This revision changes this document only. It does not change code, model settings, runtime data, submission evidence, or the Devpost project. No new model execution or runtime test result is claimed.

## 4. Cross-cutting design principles — later supplementary checklist

### A. Fit the care workflow instead of forcing the person to fit the system

Care differs by person, family and provider. A new system should adapt to the records and routines that already work: paper, CSV/Excel, local forms, family notes, or professional handoff formats where technically and legally appropriate.

**Goal:** avoid making people re-enter the same information or abandon a familiar workflow simply because Yasashii was introduced.

### B. Reduce required human work year by year

Progress is not only higher AI accuracy. It is also fewer actions that a caregiver must remember or perform.

Track, where possible:

- manual input count
- button presses
- duplicate transcription
- review time
- handoff preparation time
- maintenance/recovery work required from the user

A later version should aim to require **less human work than the earlier version**, while keeping safety and human judgment visible. This is an improvement goal, not a promised annual reduction or permission to remove necessary review. Compare like-for-like workloads and record changes in care needs.

### C. Carry detection through to usable records and handoff

The long-term direction is not merely “detect bowel movement.” It is:

**observe → detect → structure → record → hand off → support the next care action**.

Output should be convertible into the form needed by the person receiving it instead of forcing every recipient into one new interface. Generating a handoff is distinct from sending it: sharing needs a specified recipient, appropriate authorization and a verified delivery path.

### D. Keep maintenance burden away from the care site where possible

Caregivers and care staff should not become system administrators.

The product direction should favor:

- health checks
- failure detection
- safe retry/recovery
- backup paths
- traceable incident records
- clear escalation only when human attention is truly needed

This extends the project's existing guarded, traceable and fail-safe design rather than replacing it. Provider-side maintenance remains a service direction, not a currently delivered support commitment. Remote access or updates must use authorized, controlled procedures.

### E. Treat uncertainty and exceptions as normal

Real caregiving is full of irregular cases. The system should not hide that fact.

- uncertain input stays uncertain
- abnormal situations can be held or stopped
- a missing observation is not proof of “no bowel movement”
- exceptions should be recorded so they can improve future design

### F. Learn from real operating friction

Field problems are not merely support tickets; they are product evidence.

Examples include:

- a record format that cannot be reused
- a caregiver who cannot perform an expected operation
- a network outage
- camera misalignment
- an edge case that repeatedly causes HOLD
- a handoff format that creates extra transcription

These should feed a controlled improvement loop: **observe the friction → preserve evidence → improve → verify → deploy carefully**. Do not publish real care records or images as feedback examples. Keep field evidence private with appropriate consent and access controls.

### G. Optimize total burden, not only hardware price

Do not make low price the sole goal. “Cheap” can become expensive if it creates more setup, training, transcription, maintenance or troubleshooting work.

Evaluate total burden across:

- purchase/setup
- learning
- daily operation
- manual review
- maintenance
- migration from existing records
- recovery after failure

The target is **low total burden and low stress**, not simply the lowest component cost. Count provider-side work too, so that reduced care-site effort is not mistaken for sustainable improvement when it is only shifted elsewhere.

## 5. Product direction in one sentence

> **Yasashii should fit the care already being given, preserve human judgment, and make the amount of work people must do smaller over time.**

## 6. What remains current versus future

### Current documented submission scope

- synthetic-data guarded workflow
- PASS / HOLD / STOP
- Strands orchestration
- guarded writes within one event execution
- pending review records
- handoff output
- saved verification evidence documented elsewhere in this repository

See [architecture.md](architecture.md) and [verification_2026-09-11.md](verification_2026-09-11.md) for the evidence and limits. This documentation correction does not repeat those tests or establish live camera integration.

### Goals and future direction, not claimed complete

- the original five product goals as a complete real-care system
- validated automatic identity/amount handling and periodic delivery to remote recipients
- the full controlled local-AI improvement loop
- automatic adaptation to existing record formats
- broader family/professional handoff integration
- progressively lower human workload
- provider-side maintenance and recovery automation
- systematic field-friction feedback into product improvement

This separation is intentional. Earlier intent, later design principles, implemented components and verified results must not be mistaken for one another.
