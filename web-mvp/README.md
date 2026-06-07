# CGIF Web MVP

This is the GitHub Pages-ready web MVP for CGIF.

It contains two demo modes:

1. Healthcare evidence review workbench
2. UFIT IT asset inventory reconciliation workbench

## Main Healthcare Demo

URL after GitHub Pages deployment:

```text
https://eugenehehe.github.io/CGIF/
```

This static React app demonstrates:

1. Prototype login
2. Work Queue
3. Case Detail
4. Reviewer Action
5. Audit Receipts
6. Policy Pack
7. Browser localStorage persistence

## UFIT CGIF-ITAM Demo

URL after GitHub Pages deployment:

```text
https://eugenehehe.github.io/CGIF/ufit-itam/
```

CGIF-ITAM applies the same evidence-boundary and routing concept to UFIT inventory operations:

- Flowtrac reconciliation
- Vendor source comparison
- Warehouse receiving scan review
- Serial number mismatch detection
- Possible stale bin detection
- Missing bin transportation ticket review
- Technician confirmation routing
- Physical audit routing
- Flowtrac update preview
- Audit receipt export

The UFIT demo uses synthetic/anonymized records only.

## Important Boundary

This GitHub Pages version is a static prototype. It does not include a real backend, real authentication, production database, PHI-safe infrastructure, UFIT internal system integration, or production compliance controls.

It uses browser `localStorage` as prototype persistence so the workflow can be demonstrated directly on GitHub Pages.

Do not upload real UFIT serial numbers, bins, ticket IDs, device names, or internal records into the public demo.

## Local Development

```bash
cd web-mvp
npm install
npm run dev
```

## Build

```bash
cd web-mvp
npm install
npm run build
```

## GitHub Pages Deployment

A workflow is included at:

```text
.github/workflows/deploy-web-mvp.yml
```

To deploy:

1. Go to the repository Settings.
2. Open Pages.
3. Under Build and deployment, choose GitHub Actions.
4. Push to `main` or manually run the workflow.

The app uses Vite base path:

```js
base: '/CGIF/'
```
