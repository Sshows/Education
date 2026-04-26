// apps/web/lib/ent-subjects.ts
// Re-exports the shared ENT subject system so web components can import from
// a stable path without needing a full symlinked package.
// All logic lives in packages/shared/src/ent-subjects.ts — do not duplicate!

export * from '../../packages/shared/src/ent-subjects';
