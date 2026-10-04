# Plan Index

## Overview

OpenDesign is an open-source, self-hostable recreation of the Claude.ai chat interface. This plan covers the architecture, data model, API contracts, design system, and task breakdown for building a production-quality clone.

## Chapters

| # | Title | Purpose |
|---|-------|---------|
| 01 | Scope | What we're building (and what we're not) |
| 02 | Architecture | Service layout, monorepo structure, deployment |
| 03 | API Design | Protocol, endpoints, streaming contracts |
| 04 | Foundations | Tech choices, conventions, non-negotiables |
| 05 | Data Model | Schema, migrations, seeding |
| 06 | Design System | Tokens, typography, components, themes |
| 07 | Frontend | Component hierarchy, state management, routing |
| 08 | Backend | Service layers, RPC handlers, middleware |
| 09 | Authentication | Auth flow, session management |
| 10 | AI Integration | Provider abstraction, LLM routing, streaming |
| 11 | Deployment | Docker, docker-compose, production config |
| 12 | Testing | Unit, integration, E2E strategy |
| 13 | Accessibility | A11y gates, keyboard navigation, contrast |
| 19 | Appendix | Glossary, references, migration notes |
| 23 | Task Cards | Phased, shippable work items |

## Phases

| Phase | Name | Goal |
|-------|------|------|
| 0 | Foundations | Repo scaffold, CI, build system, monorepo wiring |
| 1 | Core UI | Chat layout, sidebar, message rendering (static) |
| 2 | Streaming Chat | Real-time text streaming, markdown/code rendering |
| 3 | Conversation Mgmt | Create, list, rename, delete, search conversations |
| 4 | File Attachments | Upload images/files, attachment previews |
| 5 | Settings & Auth | User settings, self-hosted auth, API key config |
| 6 | Polish & Deploy | Docker compose, production hardening, docs |

## How to read this

Each chapter is a standalone reference. The task cards in `23-task-cards.md`
are the source of truth for what to build next — always pick the lowest-numbered
unfinished card.
