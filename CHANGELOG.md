# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2024-07-27

### Added

- Separate endpoints for vector and graph-only options

### Changed

- Vector chain updated to create a vector index if none is already present in the database
- Mode option in POST payload, now only requires the 'message' key-value
- Dependencies updated

## [0.1.1] - 2024-06-05

### Added

- CORS middleware
- Neo4j exception middleware

### Changed

- Replaced deprecated LLMChain implementation
- Vector chain simplified to use RetrievalQA chain
- Dependencies updated

## [0.1.0] - 2024-04-05

### Added

- Initial release.
- Core functionality implemented, including:
  - FastAPI wrapper
  - Vector chain example
  - Graph chain example
  - Simple Agent example that aggregates results of the Vector and Graph retrievers
