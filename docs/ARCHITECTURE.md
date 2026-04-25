# Architecture

- API: бизнес-логика прогнозов + RAG endpoints + admin.
- Bot: командный интерфейс и deep-link к Mini App.
- Worker: ingestion официальных/вторичных источников, конфликт-детекция, reindex.
- Web: Mini App UI (calculator, results, cards, AI chat).
