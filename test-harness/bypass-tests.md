# Bypass Tests (EAP-TEST-1)

## Objective
Demonstrate that non-bypassability and enforcement constraints remain effective under common bypass attempts.

## Required scenarios (L2+)
1. Direct tool/API invocation bypass (skip gateway)
2. Undeclared memory persistence / side-channel state storage
3. Unauthorized delegation / routing outside routing gateway constraints
4. Tool registry tampering without change control
5. Evidence tampering / replay attempts

## Evidence to retain
- test case ID and environment
- logs showing detection/prevention
- integrity verification outputs
- links to governance events (if triggered)
