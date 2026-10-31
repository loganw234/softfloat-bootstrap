/* Berkeley SoftFloat 3e reference cases for the oracle's untested paths:
   roundTiesToAway (round_near_maxMag) and tininess before rounding. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "softfloat.h"
static uint64_t s = 0x2545f4914f6cdd1du;
static uint64_t rnd(void) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
static uint64_t g64(void) { uint64_t r = rnd(); int k = r % 6; uint64_t e, m = rnd() & 0xFFFFFFFFFFFFFull;
  switch (k) { case 0: e = 0; break; case 1: e = 1 + rnd() % 2; break; case 2: e = 2046 - rnd() % 2; break; default: e = rnd() % 2047; }
  if (rnd() % 3 == 0) m &= 0xFFFFFull; return ((r >> 8) & 1) << 63 | e << 52 | m; }
static uint32_t g32(void) { uint32_t r = (uint32_t)rnd(); int k = r % 6; uint32_t e, m = rnd() & 0x7FFFFF;
  switch (k) { case 0: e = 0; break; case 1: e = 1 + rnd() % 2; break; case 2: e = 254 - rnd() % 2; break; default: e = rnd() % 255; }
  if (rnd() % 3 == 0) m &= 0xFFF; return ((r >> 8) & 1) << 31 | e << 23 | m; }
static void fl(char *o) { char *p = o; uint_fast8_t f = softfloat_exceptionFlags;
  if (f & softfloat_flag_invalid) *p++ = 'i'; if (f & softfloat_flag_infinite) *p++ = 'z'; if (f & softfloat_flag_overflow) *p++ = 'o';
  if (f & softfloat_flag_underflow) *p++ = 'u'; if (f & softfloat_flag_inexact) *p++ = 'x'; *p = 0; }
int main(int argc, char **argv) {
  int n = atoi(argv[1]); char f[8];
  struct { const char *rm; int m; } R[] = {{"rna", softfloat_round_near_maxMag}, {"rne", softfloat_round_near_even}, {"rtz", softfloat_round_minMag}};
  const char *ops[] = {"add", "mul", "div", "sqrt", "fma"};
  for (int t = 0; t < 2; t++) for (int r = 0; r < 3; r++) for (int o = 0; o < 5; o++) for (int i = 0; i < n; i++) {
    softfloat_detectTininess = t ? softfloat_tininess_beforeRounding : softfloat_tininess_afterRounding;
    softfloat_roundingMode = R[r].m;
    float64_t a = {g64()}, b = {g64()}, c = {g64()}, x; float32_t a3 = {g32()}, b3 = {g32()}, c3 = {g32()}, x3;
    softfloat_exceptionFlags = 0;
    x = o == 0 ? f64_add(a, b) : o == 1 ? f64_mul(a, b) : o == 2 ? f64_div(a, b) : o == 3 ? f64_sqrt(a) : f64_mulAdd(a, b, c);
    fl(f); printf("%s 64 %s %s %016llx %016llx %016llx %016llx %s\n", ops[o], R[r].rm, t ? "before" : "after",
       (unsigned long long)a.v, (unsigned long long)b.v, (unsigned long long)c.v, (unsigned long long)x.v, f);
    softfloat_exceptionFlags = 0;
    x3 = o == 0 ? f32_add(a3, b3) : o == 1 ? f32_mul(a3, b3) : o == 2 ? f32_div(a3, b3) : o == 3 ? f32_sqrt(a3) : f32_mulAdd(a3, b3, c3);
    fl(f); printf("%s 32 %s %s %08x %08x %08x %08x %s\n", ops[o], R[r].rm, t ? "before" : "after", a3.v, b3.v, c3.v, x3.v, f);
  }
  return 0;
}
