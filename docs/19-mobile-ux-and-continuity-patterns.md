# Mobile UX and Continuity Patterns

This page captures public-safe lessons from running a private AI product on phones, tablets, and desktop browsers. It avoids product source, private routing rules, account data, connector internals, prompts, and infrastructure specifics.

## Mobile Answer Shape

Mobile answers should not expose long raw URL runs unless the URL itself is the point of the answer.

Prefer:

- named links for brands, products, docs, and related sites
- one thought per line when several related entities are listed
- compact answer-first wording before source links
- readable link labels that still make the destination obvious

Avoid:

- several full URLs inline in one paragraph
- answer text that looks like one site owns every other site because line breaks collapsed
- long link text that pushes controls or source cards off-screen

## Setup Defaults Must Match Platform Choice

If a setup flow asks the user to choose an operating system, every visible default below that choice should update with it.

Public-safe pattern:

| User choice | Example default shape |
|---|---|
| Windows | `C:\ProgramData\<Product>\connector` |
| macOS | `${HOME}/Library/Application Support/<Product>/connector` |
| Linux | `${HOME}/.config/<product>/connector` |

The important principle is not the exact private path. The principle is that a Mac or Linux user should never see a Windows path as the recommended default after selecting their platform.

When users enter a custom path, preserve it. When they are still on a known platform default, replace it automatically when the platform changes.

## Contact Flows Should Fail Softly

Contact and support forms should not depend on one delivery mechanism being perfect.

A robust pattern is:

- validate the request server-side
- try the normal notification channel
- if that channel is unavailable, persist the request durably
- return a truthful success only if at least one delivery or durable-capture path worked
- surface a friendly failure only if the request could not be delivered or persisted

This prevents a temporary email provider outage from becoming a product-visible `502` for a user trying to ask for help.

## Generated Artifact Continuity

When an AI product creates an artifact, follow-up turns should retain the artifact as conversational context.

Examples:

- user laughs at a generated image: respond as if the image is part of the current thread
- user asks to change the background: create a revised generation request grounded in the last generated image prompt/context
- user asks to continue a story: continue the story rather than starting a new unrelated draft
- user asks to explain a generated code file: refer to that generated code, not a generic file

Public-safe design principle:

- store artifact identity and minimal useful context with the conversation
- keep the visible reply honest about whether the system is regenerating, editing pixels directly, or asking for a source upload
- do not claim access to a physical object or local file that the system does not have

## Hardware and Cache Truth

Large local storage and accelerator hardware are useful only when the product path actually uses them.

Good public-facing documentation should distinguish:

- hardware that exists
- hardware that is healthy
- hardware that is attached to the platform
- hardware that is actively used by a specific runtime path

That distinction matters for trust. A product should not imply that a cache drive, GPU, or workstation is accelerating a feature unless the shipped path really uses it.
