#!/usr/bin/env bash
# Kiem: input_id trong run_a2.sh doi khi INPUT doi (loi 08/09 khien paf2bed/annotate bi SKIP).
# Chay: bash pipeline/p02_core_map/tests/test_params_identity.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
# Nap dinh nghia ham input_id tu run_a2.sh (khong chay phan than script).
eval "$(awk '/^input_id\(\) \{/,/^\}/' "$ROOT/pipeline/p02_core_map/run_a2.sh")"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
f="$tmp/in.txt"; printf 'aaa' > "$f"
a="$(input_id "$f")"
sleep 1; printf 'bbbbbb' > "$f"
b="$(input_id "$f")"
m="$(input_id "$tmp/khong-ton-tai.txt")"
fail=0
[ "$a" != "$b" ] || { echo "FAIL: input_id khong doi khi noi dung/size doi"; fail=1; }
case "$a" in *":3:"*) ;; *) echo "FAIL: thieu size trong '$a'"; fail=1;; esac
case "$m" in *":missing") ;; *) echo "FAIL: file thieu phai tra ':missing', duoc '$m'"; fail=1;; esac
[ "$fail" -eq 0 ] && echo "OK test_params_identity (3 assert)"
exit "$fail"
