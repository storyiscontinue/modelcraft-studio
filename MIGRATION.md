# Migration Notes

## Database

The local database schema is version 3. On first open, an older v0.2.9 database
is backed up as `agent.pre-v3.bak` and migrated in one SQLite transaction.

The migration preserves:

- workflow IDs, titles, parameters, and workspace contents;
- steps, logs, messages, token usage, and delivery records;
- legacy `waiting_review` state, mapped to a paused checkpoint;
- relative, portable workspace and runtime paths.

If migration fails, the transaction is rolled back and the original database
remains openable. Reopening an already migrated database is idempotent.

## Upgrade procedure

1. Close all ModelCraft processes.
2. Back up the existing application directory, `data/`, and `workspaces/`.
3. Verify both formal executable and portable ZIP hashes against
   `release-formal\SHA256.txt`.
4. Copy the existing `data/` and `workspaces/` into the new release only when
   they are not already present.
5. Run `OfflineModelingAgent.exe --self-test`.
6. Run `OfflineModelingAgent.exe --diagnose`.
7. Start the application and confirm existing workflows and checkpoints.

Do not copy `.agent` data into a final delivery archive. Do not replace the
pre-migration backup until the upgraded workflows have been inspected.

## Protected settings

Sensitive settings are migrated from legacy plaintext `settings.json` into
`protected-settings.json`, encrypted with Windows current-user DPAPI. The
public settings file retains only non-sensitive values and relay profile IDs
and display names.

DPAPI ciphertext cannot be decrypted by a different Windows user account. For
cross-machine or cross-account migration, copy `agent.db` and `workspaces`, but
re-enter relay URLs, model settings, runtime paths, and keys in Settings. Never
place plaintext keys into either release archive.

## Runtime compatibility

Claude Code sessions are resumed only with an exact tested CLI version. The
accepted versions are `2.1.132` and `2.1.177`. An unsupported version is
reported as blocking rather than accepted on the assumption that a newer
protocol is compatible.

The preserved v0.2.9 formal interface depends on the project-bundled Pillow
12.2.0 compatibility runtime. Do not replace `_internal\formal_runtime` with
files from another installed application.
