"""Build a downloadable, verifiable archive of reconstructed research documents."""

from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-04"
ORIGINALS = [
    {
        "name": "中长线投资方法提炼-v0.1.md",
        "historical_bytes": 41609,
        "historical_sha256": "82b3a31ac5029502d8fa400a281aa79056bb464411fe7a3af405998a5c8d7ae5",
        "status": "original_unavailable_not_verified",
    },
    {
        "name": "中长线投资方法提炼-v0.2.md",
        "historical_bytes": 70802,
        "historical_sha256": "43f8f3b1e705c940714e0a6b77183586a1791985d14e34b64c2cdb2e8a0710e0",
        "status": "original_unavailable_not_verified",
    },
]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    documents = sorted((ROOT / "reports").glob("*.md"))
    if len(documents) != 4:
        raise RuntimeError(f"Expected four reconstructed reports, got {len(documents)}")
    for path in documents:
        if "重建版" not in path.read_text(encoding="utf-8").splitlines()[0]:
            raise RuntimeError(f"Missing reconstruction label: {path.name}")
    manifest = {
        "reconstructed_on": DATE,
        "timezone": "UTC+8",
        "source": "conversation_record",
        "is_original_archive": False,
        "originals": ORIGINALS,
        "missing_original_materials": [
            "Original frozen Markdown files",
            "Original extracted source text and images",
            "Uploaded PDF and Word files (not included)",
        ],
        "reconstructed_documents": [
            {
                "path": str(p.relative_to(ROOT)),
                "bytes": p.stat().st_size,
                "sha256": digest(p),
                "status": "reconstructed_not_byte_identical_claim",
            }
            for p in documents
        ],
    }
    manifest_path = ROOT / "reconstruction-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    files = [ROOT / "README.md", *documents, manifest_path, Path(__file__).resolve()]
    sums = ROOT / "SHA256SUMS"
    sums.write_text(
        "".join(f"{digest(p)}  {p.relative_to(ROOT)}\n" for p in files), encoding="utf-8"
    )
    files.append(sums)
    destination = ROOT / "downloads"
    destination.mkdir(exist_ok=True)
    archive = destination / f"stock-research-reconstructed-{DATE}.zip"
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, str(path.relative_to(ROOT)))
    with ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise RuntimeError("ZIP CRC validation failed")
        for path in files:
            if bundle.read(str(path.relative_to(ROOT))) != path.read_bytes():
                raise RuntimeError(f"Archive content mismatch: {path.name}")
    (destination / "SHA256SUMS").write_text(
        f"{digest(archive)}  {archive.name}\n", encoding="utf-8"
    )
    print(f"Verified {len(documents)} reports and {len(files)} archive entries")
    print(f"Archive: {archive.relative_to(ROOT)} ({archive.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
