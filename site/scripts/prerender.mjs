import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(__dirname, '..');
const distRoot = resolve(siteRoot, 'dist');

const renderApp = () => {
  return `
    <div>
      <header>
        <div class="wrapper">
          <div class="site-header">
            <h1>Marathon Records</h1>
          </div>
        </div>
      </header>
    </div>
  `;
};

const run = async () => {
  const indexPath = resolve(distRoot, 'index.html');
  const indexHtml = await readFile(indexPath, 'utf8');

  const appHtml = renderApp();
  const updatedHtml = indexHtml.replace(
    /<div id="app"><\/div>/,
    `<div id="app">${appHtml}</div>`
  );

  if (updatedHtml === indexHtml) {
    throw new Error('Unable to find #app mount point to prerender.');
  }

  await writeFile(indexPath, updatedHtml);
};

run().catch((error) => {
  console.error('Prerender failed:', error);
  process.exitCode = 1;
});
