# CGIF Web MVP

This is the GitHub Pages-ready web MVP for CGIF.

It is a static React app built with Vite. It demonstrates the product workflow:

1. Prototype login
2. Work Queue
3. Case Detail
4. Reviewer Action
5. Audit Receipts
6. Policy Pack
7. Browser localStorage persistence

## Important Boundary

This GitHub Pages version is a static prototype. It does not include a real backend, real authentication, production database, PHI-safe infrastructure, or healthcare compliance controls.

It uses browser `localStorage` as prototype persistence so the workflow can be demonstrated directly on GitHub Pages.

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

So the final Pages URL should be similar to:

```text
https://eugenehehe.github.io/CGIF/
```
