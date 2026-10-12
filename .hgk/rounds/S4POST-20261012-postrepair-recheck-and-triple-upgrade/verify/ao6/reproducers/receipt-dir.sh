#!/usr/bin/env bash
set -u
B="$(cd "$(dirname "$0")" && pwd -P)"; W="$B/h/clone"; REL=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
# This separate suite clone is external and contains no officer delivery writes.
case "$(cygpath -m "$W")" in C:/Users/user/AppData/Local/Temp/a6*/h/clone) ;; *) exit 90;; esac
cat > "$B/receipt-dir-stub.sh" <<'EOF'
#!/usr/bin/env bash
mkdir -p "$LANE_WT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/WRITE_fixed.receipt"
echo stub-success
exit 0
EOF
chmod +x "$B/receipt-dir-stub.sh"
# Prior suite intentionally left its TMPDIR containment fixture; remove only named external dirt.
rm -rf "$W/tmp-inside"
echo 'COMMAND: LANE_TOKEN=fixed CODEX_BIN=receipt-dir-stub.sh run_lane.sh WRITE brief_nt.md verify/ao6'
TMPDIR="$B/logs" LANE_WT="$W" LANE_TOKEN=fixed CODEX_BIN="$B/receipt-dir-stub.sh" bash "$W/$REL/stage-b/run_lane.sh" WRITE brief_nt.md verify/ao6
echo RECEIPT_DIRECTORY_EXIT=$?
git -C "$W" status --porcelain; echo STATUS_EXIT=$?
if [ -d "$W/$REL/stage-b/WRITE_fixed.receipt" ]; then echo RECEIPT_IS_DIRECTORY; fi
if [ -f "$W/$REL/stage-b/WRITE_fixed.receipt" ]; then echo RECEIPT_IS_FILE; else echo RECEIPT_IS_NOT_FILE; fi