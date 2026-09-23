# E-commerence analysis web dashboard

This folder is a static, GitHub Pages-friendly web version of the validated
Power BI build package. It uses source-local Amazon analysis and keeps the
international monetary source separate.

## View locally

From the repository root, run:

```bash
python -m http.server 8000
```

Then open:
`http://localhost:8000/E-commerence%20analysis/`

Opening `index.html` directly may block the JSON data request in some browsers.

## Show it on GitHub

1. Push this folder to the repository.
2. In GitHub, open **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the branch containing this folder and `/(root)`, then save.
5. Open:
   `https://micc-cloud.github.io/e-commerce_analysis/E-commerence%20analysis/`

Use the default branch after merging if you want the public URL to remain stable.
The charts load Chart.js from jsDelivr, so the published page needs internet
access. The dashboard deliberately excludes profit, margin, customer, inventory,
forecasting, and official cancellation or return KPIs.
