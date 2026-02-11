# Ordering Model Example: Hybrid Ordering

Each producer uses local sequence numbers; reconciliation combines streams with declared tie-break rules.

Benefits: resilient and scalable.  
Tradeoffs: reconciliation complexity and clock tolerance management.
