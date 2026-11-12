// SPDX-License-Identifier: LicenseRef-Ultrastable-USL-1.0
// Copyright (c) 2026 Rowan Brad Quni-Gudzinas. Non-commercial use free; commercial use requires a license. See LICENSE.
// Verifies that LICENSE and COMMERCIAL-TERMS.md in every Ultrastable repository are byte-identical to this repository's.
// Usage: node scripts/check-copies.mjs [workers] [spec]     (fetches https://raw.githubusercontent.com/ultrastable/<repo>/main/<file>)
import { readFileSync } from 'node:fs';
const repos = process.argv.slice(2).length ? process.argv.slice(2) : ['workers', 'spec'];
const files = ['LICENSE', 'COMMERCIAL-TERMS.md'];
let bad = 0;
for (const repo of repos) for (const f of files) {
  const url = `https://raw.githubusercontent.com/ultrastable/${repo}/main/${f}`;
  const r = await fetch(url);
  if (!r.ok) { console.log(`MISSING ${repo}/${f} (${r.status})`); bad++; continue; }
  const same = (await r.text()) === readFileSync(new URL(`../${f}`, import.meta.url), 'utf8');
  console.log(`${same ? 'ok     ' : 'DIFFERS'} ${repo}/${f}`);
  if (!same) bad++;
}
process.exit(bad ? 1 : 0);
