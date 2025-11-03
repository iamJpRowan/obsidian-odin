# ODIN Documentation

Welcome to the ODIN documentation! This directory contains all user-facing and developer documentation for the project.

## Quick Links

### Getting Started
- **[Quickstart Guide](quickstart.md)** - Get ODIN running in 5 minutes
- **[Local LLM Setup](local-llm-setup.md)** - Run ODIN with complete privacy using Ollama
- **[Contributing Guide](contributing.md)** - How to develop and customize ODIN
- **[Testing Guide](testing.md)** - How to test your changes

### Technical Documentation
- **[Docker Build Guide](docker-build.md)** - Building and managing Docker images
- **[Plugin Development](plugin-development.md)** - Setting up plugin development environment
- **[Plugin Releases](plugin-releases.md)** - Releasing plugin updates to GitHub
- **[CI/CD Workflow](ci-workflow.md)** - GitHub Actions and PR status checking

## Documentation Structure

```
docs/
├── README.md              # This file - documentation index
├── quickstart.md         # Fast setup guide
├── local-llm-setup.md    # Local LLM setup with Ollama (privacy-focused)
├── contributing.md       # Developer contribution guide
├── testing.md            # Testing instructions
├── docker-build.md       # Docker image management
├── plugin-development.md # Plugin dev environment setup
├── plugin-releases.md    # Plugin release workflow
└── ci-workflow.md        # CI/CD and PR status checking
```

## Additional Resources

### In the Repository
- **[Main README](../README.md)** - Project overview and architecture
- **[Development Log](../devlog/)** - Detailed development history and decisions
- **[Changelog](../CHANGELOG.md)** - Version history and release notes

### External Links
- **[Obsidian Plugin API](https://github.com/obsidianmd/obsidian-api)** - Official Obsidian plugin documentation
- **[Memgraph Documentation](https://memgraph.com/docs)** - Graph database documentation
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)** - Backend framework docs
- **[LangChain Documentation](https://python.langchain.com/)** - AI integration framework

## Contributing to Documentation

Found an error or want to improve the docs? Here's how:

1. Edit the relevant `.md` file in the `docs/` directory
2. Follow the existing formatting and structure
3. Test any code examples you add
4. Submit a pull request with your changes

### Documentation Standards

- Use clear, concise language
- Include code examples where helpful
- Link to related documentation
- Keep the main README focused on overview/getting started
- Put detailed guides in the `docs/` directory

## Need Help?

- **Issues:** Open an issue on GitHub
- **API Documentation:** When running locally, visit http://localhost:8000/docs
- **Community:** Check discussions or start a new one

---

**Note:** This documentation covers the monorepo version of ODIN which includes both the plugin and backend in one repository for easier customization and development.
