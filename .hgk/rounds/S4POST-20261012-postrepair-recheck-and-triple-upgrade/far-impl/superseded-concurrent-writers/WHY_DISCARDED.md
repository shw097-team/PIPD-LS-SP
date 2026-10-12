# Why these artifacts were discarded rather than continued

The previous FAR writer attempt(s) were run TWICE concurrently in this same worktree by mistake:
the stopped v1-backup lane (`opencode-go/deepseek-v4-flash`, v1 brief) and the v2 lane
(`opencode-go/deepseek-v4.1-flash`, v2 brief) were both writing the same allowed files. The v2
lane's own transcript noticed it ("A concurrent writer session is active in this same worktree ...
it has been overwriting the same allowed files").

Consequence: the produced files correspond to NO single specification - part v1, part v2 - so they
cannot be attributed to a lane, a spec or a model, and their self-written tests are evidence about a
mixture that never existed as a candidate. Kept here for the record only; the write paths were
reset to the committed state and the FAR implementation was re-run from scratch under the v2 brief
with ONE writer using the declared model.
