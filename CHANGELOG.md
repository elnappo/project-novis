# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
* OAuth provider
* Custom user model
* Current user data API endpoint, OAuth scops
    * APRS passcode for validated callsigns
* User verification process
* Ham radio database models
    * Country
    * DXCC Entry
    * Prefix
    * Call Sign
    * DMR ID
    * LOTW, Clublog, and EQSL User
    * Repeater
    * Federal Network Agencies
* DXCC to country mapping
* Ham radio prefix mapping
* Management commands to import data from various ham radio web services
* API endpoints for
    * Countries
    * DXCC Entries
    * Prefixes 
    * Callsigns
    * DMR IDs
    * Repeaters
* Swagger/OpenAPI 2.0 schemas
* API endpoint for RADIUS authentication
* Sentry error tracking
* CORS header for `/api/*`
* Docker support
* Helm chart
* Callsign blacklist
* Geocode API to translate address to location (point)
* Piwik
* pytest
* Awesome logo (many thanks to @mirzazulfan)
