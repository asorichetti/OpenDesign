# Plan Index

## Overview

OpenDesign is an open-source, self-hostable recreation of Claude Design — the capability to take conversational design prompts and generate visual assets, interactive prototypes, and presentations. This project implements Claude Design as an **Open WebUI extension** (Pipe + Action + Filter functions) that works alongside any LLM backend.

## Chapters

| # | Title | Purpose |
|---|-------|---------|
| 01 | Scope | What Claude Design does (and doesn't do) |
| 02 | Architecture | Open WebUI plugin architecture, integration points |
| 03 | API Design | LLM contracts, tool definitions, rendering protocols |
| 04 | Foundations | Tech choices, conventions, non-negotiables |
| 05 | Data Model | Storage schema for designs, versions, assets |
| 06 | Design System | Preview rendering, component library, themes |
| 07 | Plugin Functions | Pipe, Filter, Action implementations |
| 08 | Preview Engine | HTML/CSS/JS rendering, sandboxing, live edit |
| 09 | LLM Integration | Prompt engineering, provider abstraction, streaming |
| 10 | Deployment | Docker compose, standalone install, self-hosting |
| 11 | Testing | Unit, integration, preview validation |
| 12 | Accessibility | Preview a11y, plugin a11y, contrast, keyboard |
| 19 | Appendix | Glossary, references, Claude Design feature mapping |
| 23 | Task Cards | Phased, shippable work items |

## Phases

| Phase | Name | Goal |
|-------|------|------|
| 0 | Foundations | Repo scaffold, Open WebUI plugin structure, CI |
| 1 | Core Pipe | Design generation pipe that returns HTML prototypes |
| 2 | Preview Rendering | Sandbox preview panel with live HTML rendering |
| 3 | Version History | Save/load design iterations, diff between versions |
| 4 | Presentation Mode | Slide deck generation, presenter view |
| 5 | Asset Library | Reusable component templates, design system presets |
| 6 | Polish & Deploy | Docker, docs, Open WebUI community publishing |

## How to read this

Each chapter is a standalone reference. The task cards in `23-task-cards.md`
are the source of truth for what to build next — always pick the lowest-numbered
unfinished card.
