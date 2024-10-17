## Command Line Options

### Basic test run
To run entire test suite from the cli using default values:
`pytest`

#### Default Values
Browser - Chrome
Headless - false
Isolated - true
Private - false
UserName - ADMIN_USER
Password - ADMIN_PASS

#### Alternate Values
To run tests with other than default vaules. 
`pytest --browser All --headless True --username "Bobby"`

The following options are available:

--browser [Chrome, Edge, Firefox, All]
--headless [True, False]
--private [True, False]
--username [string value]
--password [string value]

Not yet implimented
--isolated [True, False]

### Markers used
When desired, test can focus on specific test types using markers.
**Note** - marker uses a single dash, unlike other option flags
`pytest -m debug`

#### Markers Available
Currently implimented markers in bold:

authentication: marks authenitcation focused tests
**api**: marks API focused tests
chrome: marks test specifically designed to test Chrome Browsers
**connection**: marks tests involving connection to endpoints
**countries**: marks test involving the countries page
**debug**: marks tests being run for debugging purposes
e2e: marks End-to-End tests
edge: marks tests specifically designed to test Edge Browsers
**invalid_credentials**: marks tests that use invalid credentials
firefox: marks tests specifically designed to test FireFox Browsers
**functionality**: marks functionality focused tests
integration: marks Integration tests
**login**: marks login focused tests
performance: marks performance focused tests
regression: marks Regression tests
security: marks security focused tests
slow: marks tests that can be slow to run
smoke: marks Smoke tests
**table**: marks tests that involve table manipulation
**UI**: marks UI focused tests
**valid_credentials**: marks tests that use valid credentials
**video**: marks video focused tests

