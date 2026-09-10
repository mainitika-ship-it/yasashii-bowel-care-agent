# Hackathon fit recheck — 2026-09-10

This repository is specifically for **Agents for Humans Hackathon**. Official event data, rules, custom submission fields, dates, project status, and recent announcements were fetched from Devpost on 2026-09-10. This guide is a helper; the [official website](https://agentsforhumans.devpost.com/) and [rules](https://agentsforhumans.devpost.com/rules) prevail if there is any discrepancy. This review does not record a new rules agreement or submit anything.

## Fit and scope

The recommended track is **Everyday Agents**: this project assists family caregivers with observation, recordkeeping, and handoff. That is a project recommendation; the actual selected track must be checked in Devpost.

Official build requirement: "Build a new AI agent with Strands Agents SDK that does real work for people."

The new agent validates a structured event, selects a guarded tool, creates a record or review/alert item, and produces a handoff. This is the scope currently implemented in this public repository. The pre-existing vision prototype is disclosed separately. Camera sensing, continuous household operation, caregiver approval controls, and clinical effectiveness must not be presented as demonstrated by this repository's synthetic tests.

## Correction: a specific paid model is not mandatory

The host's September 9 announcement, **[Recording Available] Agent Speedrun: Ideate → Build → Validate → Deploy**, asks whether Nova Pro or a specific model is required and answers: "No — use whatever model you want. It won't affect your eligibility."

The same announcement says a working agent with tools and a clear system prompt is sufficient to build and enter; model choice is flexible. The official requirements make AgentCore deployment and a public live website optional. The project previously used Bedrock as its only implementation route, so its local checklist described a Bedrock run as a core gate. That was our project plan, not a requirement to pay for Bedrock.

The code now offers two explicit live-provider routes: Bedrock with paid-model opt-in, or an already installed, checked local Ollama model. Neither route has yet been run against a real model in this workspace. Offline and scripted-model tests are not substitutes for demonstrating an actual working Strands agent. Never automatically switch from a failing local model to a paid model.

## Official submission mapping

Deadline from Devpost key dates: **2026-09-15 00:00 UTC = 2026-09-15 09:00 Japan time**. The owner's earlier target remains September 14 evening.

| Actual field / deliverable | Current project evidence or remaining action |
|---|---|
| Submitter Type (27729) | Owner must verify the actual selection. |
| Country of Residence (27730) | Owner must verify the actual selection; do not publish personal form answers in source. |
| Track (27732) | Recommend Everyday Agents; verify actual selection. |
| PUBLIC URL to your code repo (27733) | Use `https://github.com/mainitika-ship-it/yasashii-bowel-care-agent`; the fetched Devpost project still points to the old `kenji` subfolder. |
| Architecture diagram (27734, required attachment) | `docs/architecture.png` is prepared. The field accepts PDF/PPT/PPTX/PNG/JPG/JPEG; Mermaid Markdown alone is not an attachment. Upload and verify the current diagram on Devpost. |
| AWS Builder ID (27735) | A prior project record says it was entered; current field value was not available through the project read. Owner recheck needed. |
| Video | Maximum five minutes; show the working project, problem, audience, and importance. Official rules require a public YouTube or Vimeo video. Current Devpost `video_url` is empty. |
| English materials | English README, architecture diagram and instructions exist; result screens have English and Japanese. Video must have English or an English translation. |
| Testing instructions (28191, optional field) | Link to the English README and local model guide. Give judges usable access to the working project as required by the rules; an offline report alone is not proof of live model behavior. |
| Final Submit | The fetched project is published in the portfolio, but this hackathon's `submitted_at` is null. Portfolio publication is not final entry. |

The official evaluation covers technical implementation, design, potential impact, creativity/originality, and presentation. Our priority is a complete, reproducible, truthful demonstration with inspectable safeguards. Additional deployment or blog features come after the required working demonstration and video.

## Next smallest useful action

On the owner's model-hosting computer, run `python3 src/check_local_setup.py` from this repository root, as described in [local model guide](local_model_guide.md). It discovers existing local models and prints a next command after checking metadata and Python packages. This sends no observation or inference prompt and downloads nothing. A model used for vision is not assumed to support tools. After a successful check, run one suggested synthetic live demo command, inspect its result, and record the actual successful workflow.
