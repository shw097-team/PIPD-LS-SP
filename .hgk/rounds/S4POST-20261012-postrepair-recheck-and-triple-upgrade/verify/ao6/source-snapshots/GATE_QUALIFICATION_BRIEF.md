# Lane qualification: two-tool round trip

You are being asked to prove that this exact model, on this exact endpoint and reasoning effort, can
survive more than one tool round trip inside this CLI. That is the shape that previously failed, so
this is a refusal gate, not a formality.

Do exactly this and nothing else:

1. Call the shell tool once with `echo Q1`.
2. Call the shell tool a second time with `echo Q2`.
3. Then print exactly two lines, in this order, and stop:
   Q1_OK
   Q2_OK

Rules: do not read, create, modify, or delete any repository file. Do not run the test suite. Do not
write any artifact. Your only job is the two shell calls and the two marker lines. If a tool call is
refused, print the refusal verbatim and stop.
