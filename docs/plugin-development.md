# Plugin Development Guide

Guide for setting up a plugin development environment with automatic hot-reload to your Obsidian vault.

## Prerequisites

- [ ] Node.js and npm installed
- [ ] Obsidian installed with an active vault
- [ ] Plugin dependencies installed (`cd packages/plugin && npm install`)

## Quick Start

### 1. Configure Your Vault Path

```bash
cd packages/plugin
npm run setup:vault
```

This creates a `.env` file. Edit it and set your vault path:

```bash
OBSIDIAN_VAULT_PATH=/Users/yourname/Documents/MyVault
PLUGIN_ID=ODIN
```

### 2. Start Development Mode

```bash
npm run dev
```

This starts esbuild in watch mode and automatically copies files to your vault.

### 3. Development Workflow

```
Edit src/file.ts
  ↓
Save file
  ↓
esbuild rebuilds automatically
  ↓
Files copy to vault at .obsidian/plugins/ODIN/
  ↓
Press Cmd+R (Mac) or Ctrl+R (Windows/Linux) in Obsidian
  ↓
See your changes instantly!
```

## How It Works

The development setup uses an enhanced esbuild configuration that:

1. **Watches for changes** - Monitors all files in `src/` directory
2. **Rebuilds automatically** - Triggers on any file save
3. **Copies to vault** - Uses a custom esbuild plugin to copy files
4. **Includes source maps** - Inline source maps for debugging

### Files Copied Automatically

The dev build copies these files to your vault:
- `main.js` - The bundled plugin code
- `manifest.json` - Plugin metadata (required by Obsidian)
- `styles.css` - Plugin styles (if it exists)

### Build Configuration

The build process is configured in `esbuild.config.mjs`:

- **Development builds**: Include source maps, copy to vault
- **Production builds**: Minified, no source maps, no vault copying

## Project Structure

```
packages/plugin/
├── src/                    # Source code
│   ├── index.ts           # Plugin entry point
│   ├── model/             # Data models
│   │   ├── AnalyticsNode.ts
│   │   ├── GraphEdge.ts
│   │   ├── GraphNode.ts
│   │   └── Sentence.ts
│   ├── shared/            # Shared utilities and types
│   │   ├── animations.ts
│   │   ├── appContext.ts
│   │   ├── constants.ts
│   │   ├── messages.ts
│   │   ├── theme.ts
│   │   └── types/
│   ├── ui/                # React components
│   │   ├── Graph/
│   │   ├── Main/
│   │   ├── PromptBar/
│   │   └── RadioSelect/
│   └── util/              # Helper functions
├── esbuild.config.mjs     # Build configuration with vault copying
├── manifest.json          # Plugin metadata
├── package.json           # Dependencies and scripts
├── styles.css             # Plugin styles
├── .env                   # Your local config (gitignored)
└── .env.example           # Config template for team
```

## Available Scripts

```bash
# Development
npm run dev              # Start watch mode with auto-copy to vault

# Production
npm run build            # Build for production (no vault copying)

# Setup
npm run setup:vault      # Create .env from .env.example

# Releases (see plugin-releases.md)
npm run release          # Release patch version (1.0.0 → 1.0.1)
npm run release:minor    # Release minor version (1.0.0 → 1.1.0)
npm run release:major    # Release major version (1.0.0 → 2.0.0)
```

## Development Tips

### Fast Iteration

1. Keep `npm run dev` running in a terminal
2. Make changes to any `.ts` or `.tsx` file in `src/`
3. Save the file
4. Watch the terminal for build output
5. Reload Obsidian with `Cmd+R` / `Ctrl+R`

### Debugging

Development builds include inline source maps, so you can:

1. Open Obsidian DevTools (`Cmd+Option+I` on Mac, `Ctrl+Shift+I` on Windows/Linux)
2. Navigate to Sources tab
3. Find your TypeScript source files
4. Set breakpoints and debug normally

### TypeScript Types

The plugin uses TypeScript for type safety. Common types:

```typescript
// Obsidian types (from obsidian package)
import { Plugin, PluginManifest, TFile } from 'obsidian';

// Plugin-specific types
import { GraphNode, GraphEdge } from './model';
import { Selection } from './shared/types';
```

## Troubleshooting

### Plugin Doesn't Appear in Obsidian

**Check vault path:**
```bash
cd packages/plugin
cat .env
# Verify OBSIDIAN_VAULT_PATH is correct
```

**Verify files were copied:**
```bash
ls -la /path/to/vault/.obsidian/plugins/ODIN/
# Should show: main.js, manifest.json, styles.css
```

**Enable the plugin:**
1. Open Obsidian Settings
2. Go to Community Plugins
3. Find "ODIN" in the list
4. Toggle it ON

### Changes Not Showing Up

**Check dev server is running:**
- Terminal should show "👁 Watching for changes..."
- Look for "✓ Copied to vault at [time]" messages

**Check for build errors:**
- TypeScript errors appear in the terminal
- Fix any errors before reloading Obsidian

**Hard reload:**
```bash
# Stop npm run dev (Ctrl+C)
# Restart it
npm run dev
```

### Build Errors

**TypeScript errors:**
```bash
# Type check without building
npx tsc -noEmit -skipLibCheck
```

**Missing dependencies:**
```bash
# Reinstall all dependencies
rm -rf node_modules
npm install
```

**Import errors:**
- Check all imports use correct paths
- Obsidian modules must be imported from 'obsidian'
- React components need proper extensions

### "OBSIDIAN_VAULT_PATH not set" Warning

This means `.env` doesn't exist or is empty:

```bash
# Create from template
npm run setup:vault

# Edit with your vault path
nano .env  # or use your preferred editor
```

Set:
```
OBSIDIAN_VAULT_PATH=/path/to/your/vault
PLUGIN_ID=ODIN
```

### Permission Errors

**Cannot write to vault directory:**
```bash
# Check directory exists and is writable
ls -la /path/to/vault/.obsidian/plugins/

# Create directory if needed
mkdir -p /path/to/vault/.obsidian/plugins/ODIN
```

## Testing Your Changes

### Manual Testing Checklist

When making changes, test:

- [ ] Plugin loads without errors (check DevTools console)
- [ ] UI renders correctly
- [ ] Graph visualization works
- [ ] Prompt bar accepts input
- [ ] Backend API calls succeed
- [ ] No TypeScript errors in build
- [ ] Hot reload works correctly

### Test in Different Scenarios

- [ ] Empty vault
- [ ] Vault with many notes
- [ ] Notes with special characters
- [ ] Large graph structures
- [ ] Different Obsidian themes

## Working with React Components

The plugin uses React for UI components. Key patterns:

### Component Structure

```typescript
// Using styled-components for styling
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
`;

export const MyComponent: React.FC<Props> = ({ data }) => {
  return (
    <Container>
      {/* Component content */}
    </Container>
  );
};
```

### State Management

```typescript
// Using React context for app state
import { useApp } from './hooks/useApp';

export const MyComponent = () => {
  const { state, dispatch } = useApp();
  // Use state and dispatch
};
```

### Obsidian Integration

```typescript
// Access Obsidian app instance
import { App } from 'obsidian';

// In your component
const handleClick = () => {
  // Access vault, workspace, etc.
  const files = app.vault.getMarkdownFiles();
};
```

## Next Steps

- **[Plugin Releases](plugin-releases.md)** - Learn how to release updates
- **[Contributing Guide](contributing.md)** - General contribution guidelines
- **[Obsidian Plugin API](https://github.com/obsidianmd/obsidian-api)** - Official API docs
- **[React Documentation](https://react.dev/)** - React best practices
- **[TypeScript Handbook](https://www.typescriptlang.org/docs/)** - TypeScript reference

## Getting Help

- **Console errors:** Open DevTools in Obsidian (`Cmd+Option+I` or `Ctrl+Shift+I`)
- **Build errors:** Check the terminal running `npm run dev`
- **Issues:** Open an issue on GitHub
- **Backend problems:** See [Quickstart Guide](quickstart.md) for backend troubleshooting

---

Happy developing! 🚀

