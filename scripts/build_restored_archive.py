"""Validate historical first editions and package them without editing their text."""

from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ROOT / "archive" / "restored-originals"
HISTORICAL = {
    "中长线投资方法提炼-v0.1.md": {
        "sha256": "82b3a31ac5029502d8fa400a281aa79056bb464411fe7a3af405998a5c8d7ae5",
        "bytes": 41609,
    },
    "中长线投资方法提炼-v0.2.md": {
        "sha256": "43f8f3b1e705c940714e0a6b77183586a1791985d14e34b64c2cdb2e8a0710e0",
        "bytes": 70802,
    },
}
HISTORICAL_CHARACTERS = {
    "宏观补充00-股债汇商品与对冲的底层关系.md": 6741,
    "宏观补充01-美国经济的运行与全球传导.md": 10452,
}


def digest(data):
    return sha256(data).hexdigest()


def main():
    files = sorted(DOCUMENTS.glob("*.md"))
    if {p.name for p in files} != set(HISTORICAL) | set(HISTORICAL_CHARACTERS):
        raise RuntimeError("Unexpected first-edition file set")
    records = []
    for path in files:
        data = path.read_bytes()
        text = data.decode("utf-8")
        record = {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": len(data),
            "characters": len(text),
            "sha256": digest(data),
            "source": "first_file_write_body_in_conversation",
        }
        if path.name in HISTORICAL:
            old = HISTORICAL[path.name]
            if len(data) != old["bytes"] or digest(data) != old["sha256"]:
                raise RuntimeError(f"Historical checksum mismatch: {path.name}")
            record["verification"] = "matches_historical_bytes_and_sha256"
            record["historical_sha256"] = old["sha256"]
        else:
            expected = HISTORICAL_CHARACTERS[path.name]
            if len(text) != expected:
                raise RuntimeError(f"Historical character count mismatch: {path.name}")
            record["verification"] = "conversation_text_restored_and_character_count_matches"
            record["historical_sha256"] = None
            record["historical_characters"] = expected
        records.append(record)
    report = (DOCUMENTS / "中长线投资方法提炼-v0.2.md").read_text()
    for n in range(20):
        if f"## {n}. " not in report:
            raise RuntimeError(f"Missing section {n} in v0.2")
    if sum(line.startswith("### ") for line in report.splitlines()) != 62:
        raise RuntimeError("v0.2 historical subsection count mismatch")
    historical_path = DOCUMENTS / "历史版本校验记录.json"
    historical_path.write_text(
        json.dumps(HISTORICAL, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest_path = ROOT / "restoration-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "restored_on": "2026-11-04",
                "timezone": "UTC+8",
                "documents": records,
                "previous_reconstructions_preserved": True,
                "unrecovered": ["Uploaded PDF/Word originals", "Extracted source text and images"],
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n", encoding="utf-8"
    )
    payload = [
        ROOT / "README.md", *files, historical_path, manifest_path,
        Path(__file__).resolve(), ROOT / "scripts" / "build_archive.py",
        ROOT / "reconstruction-manifest.json",
        *sorted((ROOT / "reports").glob("*.md")),
        ROOT / "downloads" / "stock-research-reconstructed-2026-11-04.zip",
        ROOT / "downloads" / "SHA256SUMS",
    ]
    sums = ROOT / "SHA256SUMS"
    sums.write_text(
        "".join(f"{digest(p.read_bytes())}  {p.relative_to(ROOT).as_posix()}\n" for p in payload),
        encoding="utf-8",
    )
    payload.append(sums)
    archive = ROOT / "downloads" / "stock-research-first-editions-restored-2026-11-04.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for p in payload:
            bundle.write(p, p.relative_to(ROOT).as_posix())
    with ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("Archive CRC error")
        for p in payload:
            if bundle.read(p.relative_to(ROOT).as_posix()) != p.read_bytes():
                raise RuntimeError(f"ZIP content differs: {p.name}")
    (ROOT / "downloads" / "first-editions-SHA256SUMS").write_text(
        f"{digest(archive.read_bytes())}  {archive.name}\n", encoding="utf-8"
    )
    for r in records:
        print(r["path"], r["bytes"], r["verification"])
    print("Verified archive:", archive.name, archive.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
