# ODIN Plugin - Development Setup

Quick guide to set up your development environment.

## Initial Setup

1. **Install dependencies:**
   ```bash
   cd packages/plugin
   npm install
   ```

2. **Configure your vault path:**
   ```bash
   npm run setup:vault
   ```
   
   This creates a `.env` file. Edit it and set your vault path:
   ```bash
   OBSIDIAN_VAULT_PATH=/Users/yourname/Documents/MyVault
   PLUGIN_ID=ODIN
   ```

3. **Start development mode:**
   ```bash
   npm run dev
   ```

## Development Workflow

### How It Works

When you run `npm run dev`:
1. esbuild watches your `src/` files for changes
2. On any change, it automatically rebuilds the plugin
3. The built files are copied to your vault at `.obsidian/plugins/ODIN/`
4. You press `Cmd+R` (Mac) or `Ctrl+R` (Windows/Linux) in Obsidian to reload
5. Your changes appear instantly!

### What Gets Copied

The dev build automatically copies these files to your vault:
- `main.js` - The bundled plugin code
- `manifest.json` - Plugin metadata
- `styles.css` - Plugin styles (if it exists)

### Tips

- **Keep the terminal open** - You'll see build status and any errors
- **Watch for errors** - Build errors appear in the terminal
- **Hot reload** - Just save your file and reload Obsidian
- **Source maps** - Dev builds include inline source maps for debugging

## Project Structure

```
packages/plugin/
├── src/                    # Source code
│   ├── index.ts           # Plugin entry point
│   ├── model/             # Data models
│   ├── shared/            # Shared utilities and types
│   └── ui/                # React components
├── esbuild.config.mjs     # Build configuration
├── manifest.json          # Plugin metadata
├── package.json           # Dependencies and scripts
├── styles.css             # Plugin styles
├── .env                   # Your local config (gitignored)
└── .env.example           # Config template
```

## Available Scripts

```bash
npm run dev              # Start development with hot-reload
npm run build            # Production build
npm run setup:vault      # Create .env from template
npm run release          # Release patch version
npm run release:minor    # Release minor version
npm run release:major    # Release major version
```

## Troubleshooting

### Plugin doesn't appear in Obsidian

1. Check that the vault path in `.env` is correct
2. Make sure Obsidian is looking at the same vault
3. Enable the plugin in Settings → Community Plugins
4. Check the terminal for build errors

### Changes not showing up

1. Make sure `npm run dev` is still running
2. Check the terminal for build errors
3. Try reloading Obsidian with `Cmd+R` / `Ctrl+R`
4. Restart Obsidian if hot reload fails

### Build errors

1. Check the terminal output for specific errors
2. Make sure all dependencies are installed (`npm install`)
3. Verify your TypeScript/React code is valid
4. Check that imports are correct

### "OBSIDIAN_VAULT_PATH not set" warning

This means you haven't created the `.env` file yet:
```bash
npm run setup:vault
# Then edit .env with your vault path
```

## Next Steps

- **[Plugin Development Guide](../../docs/plugin-development.md)** - Comprehensive development documentation
- **[Plugin Release Guide](../../docs/plugin-releases.md)** - How to publish releases
- **[Obsidian Plugin API](https://github.com/obsidianmd/obsidian-api)** - Official API documentation
- **[Contributing Guide](../../docs/contributing.md)** - General contribution guidelines

## Documentation

- **Quick reference:** This file (DEV-SETUP.md)
- **Full dev guide:** [docs/plugin-development.md](../../docs/plugin-development.md)
- **Release process:** [docs/plugin-releases.md](../../docs/plugin-releases.md)
- **Project overview:** [Main README](../../README.md)

Happy coding! 🚀

