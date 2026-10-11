import re
import pathlib

readme = pathlib.Path(r"C:/Projects/Agent_Workspace/PIPD-postrelease-wt/README.md")
text = readme.read_text(encoding="utf-8")
pat = re.compile(r"^```powershell[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
blocks = [b for b in pat.findall(text) if "Get-FileHash" in b]
assert len(blocks) == 1, f"expected exactly 1 powershell block with Get-FileHash, got {len(blocks)}"
block = blocks[0]
out = pathlib.Path(
    r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4post/repair/r3ps/quickstart.ps1"
)
out.write_text(block, encoding="utf-8", newline="\n")
print("EXTRACTED ->", out)
print("FIRSTLINE:", block.splitlines()[0])
print("NLINES:", len(block.splitlines()))
