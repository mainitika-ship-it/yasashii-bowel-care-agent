# Agents for Humans — Final Submission Check

Updated: 2026-09-13 JST

This is a conservative final-submission checkpoint for **Yasashii Bowel Care Agent**. It records what has been verified and what still requires an owner-side check before Final Submit. It does not claim that the hackathon submission has been finalized.

## Official deadline

- **September 14, 2026 at 5:00 PM PDT**
- Equivalent project working deadline: **September 15, 2026 at 09:00 JST**

Official dates: https://agentsforhumans.devpost.com/details/dates

## Required submission items

Official requirements: https://agentsforhumans.devpost.com/

- Text description explaining what the project does, who it is for, and how it works
- Public code repository
- README
- MIT or Apache open-source license visible/detectable on the repository
- Architecture diagram
- Public YouTube/Vimeo demo video, maximum 5 minutes
- AWS Builder ID
- Required Devpost submission fields and Final Submit

AgentCore, a public live demo, and a builder.aws post can strengthen scoring but are not required for eligibility.

## Verified current state

- **Project description:** updated Devpost project text describes the family-care problem, audience, Strands workflow, synthetic-data scope, evidence, and limitations.
- **Demo video:** Devpost project now points to the public YouTube video: https://www.youtube.com/watch?v=Cuf4LXeQJCU
- **Video duration:** prepared final candidate is about **3:56**, below the 5-minute limit.
- **Canonical repository:** Devpost project now points to https://github.com/mainitika-ship-it/yasashii-bowel-care-agent
- **Repository visibility:** public.
- **License:** root `LICENSE` is MIT and GitHub detects the repository license as MIT.
- **README:** setup, architecture, safety limits, pre-existing-work disclosure, demo commands, and Strands usage are documented.
- **Architecture source:** `docs/architecture.png` and `docs/architecture.md` are present in the repository.
- **Technical evidence:** preserved September 11 Mac run covers PASS / HOLD / STOP with Strands Agents SDK + Ollama + `qwen3:8b`; the public documentation keeps that separate from scripted automated tests and from unverified camera performance.
- **Latest public CI observed before this checkpoint:** the GitHub Actions run for commit `c797ab57060af9e2ad82ea3d0d7a4890d234ca17` completed successfully.
- **Secret-pattern spot check:** a repository search for common AWS access-key / secret / password / token patterns returned no matches. This is a spot check, not a formal security audit.

## Required owner-side recheck before Final Submit

The connected Devpost project API does not expose all saved custom answers or the live attachment state, so these items must be checked on the Devpost submission form itself:

1. **Submitter Type:** expected `Individual`.
2. **Country of Residence:** expected `Japan`.
3. **Track:** expected `Everyday Agents`.
4. **PUBLIC URL to your code repo:** must be the dedicated repository above.
5. **Architecture diagram:** confirm the required file is still attached to the live submission form.
6. **AWS Builder ID:** Devpost's current FAQ says to enter the **email address used to create the AWS Builder ID**. Do not substitute a profile username unless Devpost explicitly accepts it.
7. Confirm the public YouTube video plays while signed out / anonymously.
8. Perform the owner's final review, then press **Final Submit**.

## Evidence limits that must remain unchanged

- Public demonstration uses synthetic data.
- Real camera integration and real-image detection performance are unverified.
- Real-care benefit and clinical safety are unverified.
- The caregiver approval screen is not implemented.
- Duplicate-write protection does not cover cross-process restarts.
- No successful Amazon Bedrock run is claimed.
- The project supports observation, documentation, and communication; it does not diagnose illness or replace clinical judgment.

## Submission status

**NOT FINAL-SUBMITTED as of this checkpoint.**

The project page being public is separate from the hackathon's Final Submit action.
