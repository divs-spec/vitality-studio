# Frontend Plugins

Plugins for the frontend should be placed under `frontend/plugins/<plugin-name>`.
Each plugin can expose UI components and a `plugin.json` manifest.

Example manifest:

```
{
  "name": "example-plugin",
  "version": "0.1.0",
  "entry": "dist/index.js"
}
```
