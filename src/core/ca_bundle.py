"""CA bundle helpers.

On Windows, some libcurl builds have trouble opening CA bundle paths that contain
non-ASCII characters (e.g. a project located in a Chinese-named folder). This
manifests as curl error (77): "error setting certificate verify locations".

We fix this by copying certifi's cacert.pem to an ASCII-only temp directory and
pointing curl-cffi/libcurl at it via CURL_CA_BUNDLE.
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from pathlib import Path


def _is_ascii(s: str) -> bool:
    try:
        s.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def ensure_curl_cffi_ca_bundle() -> str | None:
    """Ensure curl-cffi can load a CA bundle on Windows.

    Returns the CA bundle path if set/ensured, otherwise None.
    """

    # Respect user/system overrides.
    if os.environ.get("CURL_CA_BUNDLE"):
        return os.environ["CURL_CA_BUNDLE"]

    if not sys.platform.startswith("win"):
        return None

    try:
        import certifi  # type: ignore
    except Exception:
        return None

    src_path = certifi.where()
    if _is_ascii(src_path):
        # If the path is already ASCII-only, leave it unchanged.
        return None

    src = Path(src_path)
    if not src.exists():
        return None

    # Copy to an ASCII-only temp directory.
    dest_dir = Path(tempfile.gettempdir()) / "sora2api" / "certs"
    dest_dir.mkdir(parents=True, exist_ok=True)

    data = src.read_bytes()
    digest = hashlib.sha256(data).hexdigest()[:12]
    dest = dest_dir / f"cacert-{digest}.pem"

    if not dest.exists():
        dest.write_bytes(data)

    os.environ["CURL_CA_BUNDLE"] = str(dest)
    os.environ.setdefault("SSL_CERT_FILE", str(dest))
    return str(dest)
