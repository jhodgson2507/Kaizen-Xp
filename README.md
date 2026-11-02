# Kaizen-Xp

Trifecta Cleaning commercial site, with scroll and entrance animation from [Motion](https://motion.dev).

```bash
npm install
npm run dev      # local dev server
npm run build    # production build into dist/
npm run preview  # serve the build
```

- `index.html`: the page (styles, the logo intro and the 3D proof report animation are inline).
- `src/motion.js`: the Motion layer (hero headline, section reveals, Founding Five, scroll progress, parallax, FAQ accordion, booking form steps, errors and the "Received" stamp, area checker).
- `public/assets/`: logo images.

All Motion effects are off for visitors with "reduce motion" switched on, and the page still works if the script fails to load.
