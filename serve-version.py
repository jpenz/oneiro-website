#!/usr/bin/env python3
"""
Serve the site with the hero video swapped out for one of the archived versions.

Usage:
    python3 serve-version.py <port> <version_filename>

Example:
    python3 serve-version.py 5174 v1-original-bouzouki-crowd.mp4

Every request for /video/hero.mp4 is rewritten to /video/versions/<version_filename>.
All other requests served normally from the current directory.
"""

import sys
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(1)

port = int(sys.argv[1])
version_file = sys.argv[2]
version_path = os.path.join("video", "versions", version_file)

if not os.path.exists(version_path):
    print(f"ERROR: version file not found: {version_path}")
    sys.exit(1)


class HeroSwapHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Reroute /video/hero.mp4 to the chosen version
        if path.split("?")[0].rstrip("/").endswith("/video/hero.mp4"):
            return os.path.abspath(version_path)
        return super().translate_path(path)

    def log_message(self, fmt, *args):
        # Quieter logs
        sys.stderr.write(f"[:{port} {version_file}] {fmt % args}\n")


server = ThreadingHTTPServer(("0.0.0.0", port), HeroSwapHandler)
print(f"Serving {os.getcwd()} on http://0.0.0.0:{port}/  (hero.mp4 = {version_file})")
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
