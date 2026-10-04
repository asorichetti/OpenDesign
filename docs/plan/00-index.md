# Plan Index

## Overview

OpenDesign is an open-source, self-hostable design generation platform built as an Open WebUI extension. It takes conversational prompts and produces visual outputs — HTML prototypes, UI components, slide decks, email templates, and more — all rendered as interactive previews directly in chat.

## Chapters

| # | Title | Purpose |
|---|-------|---------|
| 01 | Scope | What we're building (and what we're not) |
| 02 | Architecture | Open WebUI plugin architecture, integration points |
| 03 | LLM Contracts | Model interfaces, prompt protocols, output formats |
| 04 | Foundations | Tech choices, conventions, non-negotiables |
| 05 | Data Model | Storage schema for designs, versions, assets |
| 06 | Design System | Preview rendering, component library, themes |
| 07 | Plugin Functions | Pipe, Filter, Action implementations |
| 08 | Preview Engine | HTML rendering, sandboxing, live edit |
| 09 | LLM Integration | Provider abstraction, prompt engineering, streaming |
| 10 | Deployment | Docker compose, standalone install, self-hosting |
| 11 | Testing | Unit, integration, preview validation |
| 12 | Accessibility | Preview a11y, plugin a11y, contrast, keyboard |
| 19 | Appendix | Glossary, references, output type matrix |
| 23 | Task Cards | Phased, shippable work items |

## Phases

| Phase | Name | Goal |
|-------|------|------|
| 0 | Foundations | Repo scaffold, Open WebUI plugin structure, CI |
| 1 | Core Generation | Design generation pipe that returns HTML prototypes |
| 2 | Preview Rendering | Sandbox preview panel with live HTML rendering |
| 3 | Version History | Save/load design iterations, diff between versions |
| 4 | Output Expansion | Presentations, email templates, social media assets |
| 5 | Live Editor | Split-pane code editor with real-time preview |
| 6 | Polish & Deploy | Docker, docs, community publishing, tests |

## How to read this

Each chapter is a standalone reference. The task cards in `23-task-cards.md`
are the source of truth for what to build next — always pick the lowest-numbered
unfinished card.
