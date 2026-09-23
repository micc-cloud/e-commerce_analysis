const money = value => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(value || 0);
const number = value => new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(value || 0);
const pct = value => `${((value || 0) * 100).toFixed(1)}%`;
const palette = ['#0f766e', '#2563eb', '#d97706', '#7c3aed', '#b42318', '#64748b', '#0891b2', '#65a30d'];

function card(label, value, note) {
  return `<article class="kpi-card"><div class="kpi-label">${label}</div><div class="kpi-value">${value}</div><div class="kpi-note">${note}</div></article>`;
}

function chart(id, config) {
  const node = document.getElementById(id);
  if (node) new Chart(node, config);
}

function render(data) {
  const s = data.scope;
  const monthly = data.monthly;
  document.getElementById('overview-period').textContent = `${s.date_range[0]} to ${s.date_range[1]} | ${number(s.amazon_lines)} lines`;
  document.getElementById('coverage-badge').textContent = `Amount coverage ${pct(s.amount_coverage)}`;
  document.getElementById('overview-kpis').innerHTML = [
    card('Reported Gross Amount', money(s.reported_amount), 'Amazon source-local; not net sales'),
    card('Distinct Orders', number(s.amazon_orders), 'Distinct order_id'),
    card('Gross Units', number(s.gross_units), 'Source qty total'),
    card('Amount Coverage', pct(s.amount_coverage), `${number(s.amazon_lines - Math.round(s.amazon_lines * s.amount_coverage))} lines without amount`)
  ].join('');
  document.getElementById('operations-kpis').innerHTML = [
    card('Status Records', number(s.amazon_orders), 'Order-level proxy table'),
    card('Delivered Proxy Orders', number(s.delivered_proxy_orders), 'Status-based analytical proxy'),
    card('Mixed-status Orders', number(s.mixed_status_orders), 'No precedence rule applied'),
    card('Valid Price Proxy Lines', number(s.valid_price_lines), 'Amount present and qty > 0')
  ].join('');
  document.getElementById('mixed-status-count').textContent = number(s.mixed_status_orders);

  const labels = monthly.map(row => `${row.month_label}${row.is_partial_period ? ' *' : ''}`);
  chart('overview-trend', { type: 'line', data: { labels, datasets: [
    { label: 'Reported gross amount', data: monthly.map(row => row.reported_amount), borderColor: '#0f766e', backgroundColor: '#0f766e22', fill: true, tension: .25, yAxisID: 'amount' },
    { label: 'Gross units', data: monthly.map(row => row.gross_units), borderColor: '#d97706', tension: .25, yAxisID: 'units' }
  ] }, options: { responsive: true, interaction: { mode: 'index', intersect: false }, scales: { amount: { position: 'left', ticks: { callback: value => money(value) } }, units: { position: 'right', grid: { drawOnChartArea: false } } } } });
  chart('overview-category', donut(data.category.slice(0, 6), 'category', 'reported_amount', 'Reported gross amount'));
  chart('overview-status', donut(data.statuses, 'status_label', 'distinct_orders', 'Distinct orders; status proxy'));

  chart('sales-monthly', { type: 'bar', data: { labels, datasets: [{ label: 'Reported gross amount', data: monthly.map(row => row.reported_amount), backgroundColor: monthly.map(row => row.is_partial_period ? '#f3b562' : '#0f766e') }] }, options: { plugins: { tooltip: { callbacks: { footer: items => monthly[items[0].dataIndex].is_partial_period ? 'Partial observed period' : 'Complete observed month' } } }, scales: { y: { ticks: { callback: value => money(value) } } } } });
  chart('sales-b2b', donut(data.b2b, 'label', 'reported_amount', 'Reported gross amount'));
  chart('sales-states', horizontal(data.states, 'ship_state', 'distinct_orders', 'Distinct orders'));
  document.getElementById('international-table').innerHTML = `<table><thead><tr><th>Source</th><th>Lines</th><th>Reported amount</th><th>Pieces</th></tr></thead><tbody><tr><td>International</td><td>${number(s.international_lines)}</td><td>${money(s.international_reported_amount)}</td><td>${number(s.international_pieces)}</td></tr></tbody></table><p class="muted">Shown separately; no cross-currency aggregation with Amazon.</p>`;

  chart('product-sku', horizontal(data.sku, 'sku', 'reported_amount', 'Reported gross amount'));
  chart('product-bands', { type: 'bar', data: { labels: data.price_bands.map(row => row.reported_unit_price_band), datasets: [{ label: 'Reported gross amount', data: data.price_bands.map(row => row.reported_amount), backgroundColor: palette }] }, options: { scales: { y: { ticks: { callback: value => money(value) } } } } });
  chart('product-category-price', { type: 'bar', data: { labels: data.category_price.map(row => row.category), datasets: [{ label: 'Mean reported unit-price proxy', data: data.category_price.map(row => row.reported_unit_price_proxy), backgroundColor: '#2563eb' }] }, options: { indexAxis: 'y', scales: { x: { ticks: { callback: value => money(value) } } } } });
  chart('operations-status', donut(data.statuses, 'status_label', 'distinct_orders', 'Distinct orders; proxy composition'));
  chart('operations-states', horizontal(data.states, 'ship_state', 'distinct_orders', 'Distinct orders'));
}

function donut(rows, label, value, datasetLabel) {
  return { type: 'doughnut', data: { labels: rows.map(row => row[label]), datasets: [{ label: datasetLabel, data: rows.map(row => row[value]), backgroundColor: palette }] }, options: { plugins: { legend: { position: 'bottom' } } } };
}

function horizontal(rows, label, value, datasetLabel) {
  return { type: 'bar', data: { labels: rows.map(row => row[label]), datasets: [{ label: datasetLabel, data: rows.map(row => row[value]), backgroundColor: '#0f766e' }] }, options: { indexAxis: 'y', plugins: { legend: { display: false } } } };
}

document.querySelectorAll('.tab').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.tab').forEach(item => item.classList.toggle('active', item === button));
  document.querySelectorAll('.page').forEach(page => page.classList.toggle('active', page.id === `page-${button.dataset.page}`));
}));

fetch('dashboard_data.json').then(response => {
  if (!response.ok) throw new Error(`Unable to load dashboard data (${response.status})`);
  return response.json();
}).then(render).catch(error => {
  document.querySelector('main').innerHTML = `<div class="warning-banner"><strong>Dashboard data unavailable.</strong> ${error.message}. Serve this folder over HTTP so the browser can load dashboard_data.json.</div>`;
});
