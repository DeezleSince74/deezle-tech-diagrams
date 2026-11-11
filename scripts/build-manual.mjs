#!/usr/bin/env node
/**
 * Build the user manual PDF by printing docs/manual/manual.html with headless Chrome.
 *
 *   node scripts/build-manual.mjs   → dist/manual/deezle-tech-diagrams-manual.pdf
 *
 * The screenshots in docs/manual/images are captures of real boards, so they're kept in
 * the repo rather than rebuilt. Needs Google Chrome; set CHROME if it isn't in the default
 * macOS spot.
 */
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const chrome = process.env.CHROME ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
if (!existsSync(chrome)) throw new Error(`Chrome not found at ${chrome}. Set CHROME to its path.`);

const html = join(root, 'docs/manual/manual.html');
const out = join(root, 'dist/manual/deezle-tech-diagrams-manual.pdf');
mkdirSync(dirname(out), { recursive: true });
execFileSync(chrome, ['--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=4000', `--print-to-pdf=${out}`, `file://${html}`], { stdio: 'ignore' });
console.log(`✓ ${out} (${Math.round(statSync(out).size / 1024)} KB)`);
