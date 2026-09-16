# Design spine and evolution policy — 2026-09-16

This note records a **post-submission design direction** for Yasashii Bowel Care Agent. It does **not** change the verified scope of the hackathon submission and does not claim that the future items below are implemented.

## やさしい要約 / Plain-language summary

難しく考えないために、まずここだけを正本として残します。

- 今までの実装の流れは壊さない。
- 今回話した内容は、新しい「7本柱」へ置き換える話ではない。
- 新しい仕組みに人を合わせるのではなく、**今までの介護・記録・申し送りにシステム側が寄り添う**。
- 使う年月が長くなるほど、**人が入力・転記・確認・申し送り・保全に使う作業を少しずつ減らす**。
- 安さだけを追わず、導入・学習・日常操作・保全まで含めた**総負担とストレスを小さくする**。
- 現場の困りごと、例外、HOLD、故障や手戻りを次の改善材料として残す。

**一言で言えば：**

> **今ある介護に寄り添い、人の判断を残しながら、人がしなければならない仕事を年月とともに減らしていく。**

> **Yasashii should fit the care already being given, preserve human judgment, and make the amount of work people must do smaller over time.**

### Important terminology note

The five-step flow below is the **current implementation spine** documented in this repository. It should not be retroactively described as an older canonical “five pillars” framework unless a separate historical source is found and verified. The later seven-item grouping is a **cross-cutting review checklist**, not a replacement architecture.

## 1. Preserve the existing five-step implementation spine

The current documented workflow remains the technical spine:

1. **Input** — accept a prepared observation input.
2. **QC** — apply fixed checks for signal, privacy flag, event type, confidence and relative amount.
3. **Strands Agents SDK** — select an allowed action.
4. **Guarded tools** — reject wrong actions, invented values and unsafe/repeated writes.
5. **Handoff** — include only normal PASS observations; keep HOLD requests and STOP alerts separate.

The safety policy also remains unchanged:

- **PASS — Record**
- **HOLD — Ask a person**
- **STOP — Stop & alert**
- **AI helps. People decide.**

## 2. Do not replace the five-step spine with a new numbered framework

A later discussion grouped several management and product ideas into seven items. That grouping is useful as a review checklist, but it is **not a replacement for the established five-step architecture** and should not be presented as if it had always been the project's canonical pillar structure.

The safer structure is:

**Five-step implementation spine + cross-cutting design principles ("plus alpha")**.

## 3. Cross-cutting design principles — the “plus alpha”

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

A later version should aim to require **less human work than the earlier version**, while keeping safety and human judgment visible.

### C. Carry detection through to usable records and handoff

The long-term direction is not merely “detect bowel movement.” It is:

**observe → detect → structure → record → hand off → support the next care action**.

Output should be convertible into the form needed by the person receiving it instead of forcing every recipient into one new interface.

### D. Keep maintenance burden away from the care site where possible

Caregivers and care staff should not become system administrators.

The product direction should favor:

- health checks
- failure detection
- safe retry/recovery
- backup paths
- traceable incident records
- clear escalation only when human attention is truly needed

This extends the project's existing guarded, traceable and fail-safe design rather than replacing it.

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

These should feed a controlled improvement loop: **observe the friction → preserve evidence → improve → verify → deploy carefully**.

### G. Optimize total burden, not only hardware price

Low price is important, but “cheap” can become expensive if it creates more setup, training, transcription, maintenance or troubleshooting work.

Evaluate total burden across:

- purchase/setup
- learning
- daily operation
- manual review
- maintenance
- migration from existing records
- recovery after failure

The target is **low total burden and low stress**, not simply the lowest component cost.

## 4. Product direction in one sentence

> **Yasashii should fit the care already being given, preserve human judgment, and make the amount of work people must do smaller over time.**

## 5. What remains current versus future

### Current verified submission scope

- synthetic-data guarded workflow
- PASS / HOLD / STOP
- Strands orchestration
- guarded writes
- pending review records
- handoff output
- saved verification evidence documented elsewhere in this repository

### Future direction recorded here, not yet claimed as complete

- automatic adaptation to existing record formats
- broader family/professional handoff integration
- progressively lower human workload
- provider-side maintenance and recovery automation
- systematic field-friction feedback into product improvement

This separation is intentional. Future design goals should be visible without being mistaken for verified hackathon results.
