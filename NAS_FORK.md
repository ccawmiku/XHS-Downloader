# NAS fork

Based on upstream XHS-Downloader 2.8. The only application change extends Converter.YAML_ILLEGAL to remove C1 controls rejected by PyYAML, preserving U+0085. Existing JSON/JavaScript normalization, API, downloads, settings and /app/Volume remain compatible. No image-format fallback patches are included.

Regression tests cover the U+0083 reproduction, every disallowed C1 code point, legal Unicode/whitespace, PC/mobile HTML and JavaScript sentinels. Tagged 2.8-nas.* builds publish ghcr.io/ccawmiku/xhs-downloader after source and actual-image regression tests.

Upstream: https://github.com/JoeanAmier/XHS-Downloader/releases/tag/2.8
