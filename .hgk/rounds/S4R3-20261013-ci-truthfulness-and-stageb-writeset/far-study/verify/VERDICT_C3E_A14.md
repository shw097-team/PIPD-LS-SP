CONFIRMED.

- C3e-1: yes. Block 3 ties `ba27309` and `ee5aa3e` to the same workflow blob `30a7b1a...`, and the path-specific diff between them is empty. `ee5aa3e` is the Stage B receipt head captured in Block 2.
- C3e-2: yes. Every change from `ba27309` to `ee5aa3e` is under `.hgk/rounds/...`; no product file changed in that range.
- C3e-3: yes. The re-extracted `ee5aa3e` Stage B sets reproduce exactly the two additions and retain the same Stage B DENIED set as the diff.

HGK_LANE_NONCE_OK