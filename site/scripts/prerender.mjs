import { readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(__dirname, '..');
const distRoot = resolve(siteRoot, 'dist');

const escapeHtml = (value) =>
  String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

const readJson = async (filename) => {
  const distPath = resolve(distRoot, filename);
  const publicPath = resolve(siteRoot, 'public', filename);
  const raw = await readFile(distPath, 'utf8').catch(() => readFile(publicPath, 'utf8'));
  return JSON.parse(raw);
};

const timeToSeconds = (timeString) => {
  if (!timeString) return Infinity;
  const parts = timeString.split(':');
  if (parts.length === 3) {
    const hours = Number(parts[0]);
    const minutes = Number(parts[1]);
    const seconds = Number(parts[2]);
    return hours * 3600 + minutes * 60 + seconds;
  }
  return Infinity;
};

const getCityInfo = (city, info) => info.filter((time) => time.City === city);

const getCityInfoByGender = (city, info, gender) =>
  info.filter((time) => time.City === city && time.Gender === gender);

const getBestTimeForCity = (city, bestTimes) => {
  const menTimes = getCityInfoByGender(city, bestTimes, 'Men');
  const womenTimes = getCityInfoByGender(city, bestTimes, 'Women');
  const allTimes = [...menTimes, ...womenTimes];

  if (allTimes.length === 0) return null;

  return allTimes.reduce((best, current) => {
    const bestSeconds = timeToSeconds(best.Time);
    const currentSeconds = timeToSeconds(current.Time);
    return currentSeconds < bestSeconds ? current : best;
  }).Time;
};

const renderTableRow = (item) => `
  <tr>
    <td>${escapeHtml(item['Country Count'])}</td>
    <td>${escapeHtml(item['People Count'])}</td>
    <td>${escapeHtml(item.Men)}</td>
    <td>${escapeHtml(item.Women)}</td>
  </tr>
`;

const renderTimeItem = (item, links) => {
  const name = escapeHtml(item.Name);
  const link = links[item.Name];
  const nameHtml = link
    ? `<a href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer" class="wikipedia-link">${name}</a>`
    : `<span>${name}</span>`;

  return `
    <li>
      ${escapeHtml(item.Time)} -
      ${nameHtml}
      <span class="fi fi-${escapeHtml(item.Country)}"></span>
      (${escapeHtml(item.Year)})
    </li>
  `;
};

const renderGenderSection = (title, items, links) => {
  if (!items || items.length === 0) return '';
  const listItems = items.map((item) => renderTimeItem(item, links)).join('');
  return `
    <div class="gender-section">
      <h4 class="gender-heading">${escapeHtml(title)}</h4>
      <ul>
        ${listItems}
      </ul>
    </div>
  `;
};

const renderCity = (marathon, marathons, bestTimes, latestTimes, links) => {
  const city = marathon.City;
  const cityInfo = getCityInfo(city, marathons);
  const bestMen = getCityInfoByGender(city, bestTimes, 'Men');
  const bestWomen = getCityInfoByGender(city, bestTimes, 'Women');
  const latestMen = getCityInfoByGender(city, latestTimes, 'Men');
  const latestWomen = getCityInfoByGender(city, latestTimes, 'Women');

  const tableRows = cityInfo
    .slice(0, 1)
    .map((item) => renderTableRow(item))
    .join('');

  return `
    <li class="list-group-item">
      <header class="item-header">
        <h2>
          ${escapeHtml(city)}
          <div class="flag" role="img" aria-label="${escapeHtml(city)} country flag">
            <span class="fi fi-${escapeHtml(marathon.Country)}"></span>
          </div>
        </h2>
      </header>

      <div class="table-container">
        <table role="table" aria-label="Statistics for ${escapeHtml(city)} marathon">
          <caption class="sr-only">Marathon statistics for ${escapeHtml(city)}</caption>
          <thead>
            <tr>
              <th scope="col">Countries</th>
              <th scope="col">Athletes</th>
              <th scope="col">Men</th>
              <th scope="col">Women</th>
            </tr>
          </thead>
          <tbody>
            ${tableRows}
          </tbody>
        </table>
      </div>

      <div class="times-section">
        <div class="times-row">
          <div class="times-col">
            <h3 class="section-heading">Best</h3>
            ${renderGenderSection('Men', bestMen, links)}
            ${renderGenderSection('Women', bestWomen, links)}
          </div>

          <div class="times-col">
            <h3 class="section-heading">Latest</h3>
            ${renderGenderSection('Men', latestMen, links)}
            ${renderGenderSection('Women', latestWomen, links)}
          </div>
        </div>
      </div>
    </li>
  `;
};

const renderApp = (marathons, bestTimes, latestTimes, links) => {
  const sortedMarathons = [...marathons].sort((a, b) => {
    const aBestTime = getBestTimeForCity(a.City, bestTimes);
    const bBestTime = getBestTimeForCity(b.City, bestTimes);

    if (!aBestTime && !bBestTime) return 0;
    if (!aBestTime) return 1;
    if (!bBestTime) return -1;

    return timeToSeconds(aBestTime) - timeToSeconds(bBestTime);
  });

  const listItems = sortedMarathons
    .slice(0, 1)
    .map((marathon) => renderCity(marathon, marathons, bestTimes, latestTimes, links))
    .join('');

  return `
    <div>
      <header>
        <div class="wrapper">
          <div class="site-header">
            <h1>Marathon Records</h1>
          </div>
        </div>
      </header>

      <main>
        <div class="wrapper">
          <section class="marathons-table" role="main" aria-label="Marathon records by city">
            <ul class="list-group" role="list">
              ${listItems}
            </ul>
          </section>
        </div>
      </main>
    </div>
  `;
};

const run = async () => {
  const [marathons, bestTimes, latestTimes, links] = await Promise.all([
    readJson('marathons.json'),
    readJson('best_times.json'),
    readJson('latest_times.json'),
    readJson('links.json'),
  ]);

  const indexPath = resolve(distRoot, 'index.html');
  const indexHtml = await readFile(indexPath, 'utf8');

  const appHtml = renderApp(marathons, bestTimes, latestTimes, links);
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
