# Self-test fixture — every citation here is deliberately broken

The checker must catch ALL of these, or its own self-test fails:

1. Sub-paragraph that does not exist: [reg 14(1)(z)]
2. Regulation not shipped in reference/: [reg 15(1)]
3. Notice section outside the shipped range: [700/21 §9.9]
4. Revoked sub-paragraph: [reg 14(1)(f)]
5. The other revoked sub-paragraph: [reg 14(1)(k)]
6. Malformed citation that a sloppy edit might produce: [Reg 14, para 1(d)]
7. Fabricated quote that reads plausibly but appears in no shipped text: the
   regulation requires "a security hologram affixed to every invoice" [reg 14(1)(a)]
