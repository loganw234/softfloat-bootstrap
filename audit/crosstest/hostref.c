/* Host-FPU reference cases (x86 SSE: tininess after rounding) for checking oracle.py. */
#include <fenv.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#pragma STDC FENV_ACCESS ON
static uint64_t s = 0x9e3779b97f4a7c15u;
static uint64_t rnd(void) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; }
static uint64_t gen64(void) {
    uint64_t r = rnd(), sign = (r & 1) << 63; int k = (r >> 1) % 8; uint64_t m = rnd() & 0xFFFFFFFFFFFFFull, e;
    switch (k) { case 0: e = 0; break; case 1: e = 1 + rnd() % 3; break; case 2: e = 2046 - rnd() % 3; break;
                 case 3: e = 1023 + (int)(rnd() % 7) - 3; break; case 4: e = 0x7FF; m = (rnd()&1) ? 0 : m; break;
                 default: e = rnd() % 2047; }
    if (rnd() % 4 == 0) m = (rnd() & 1) ? (m | 0xFFFFFFF000000ull) & 0xFFFFFFFFFFFFFull : (m & 0xFFFFFull);
    return sign | (e << 52) | m;
}
static uint32_t gen32(void) {
    uint32_t r = (uint32_t)rnd(), sign = (r & 1) << 31; int k = (r >> 1) % 8; uint32_t m = rnd() & 0x7FFFFF, e;
    switch (k) { case 0: e = 0; break; case 1: e = 1 + rnd() % 3; break; case 2: e = 254 - rnd() % 3; break;
                 case 3: e = 127 + (int)(rnd() % 7) - 3; break; case 4: e = 0xFF; m = (rnd()&1) ? 0 : m; break;
                 default: e = rnd() % 255; }
    if (rnd() % 4 == 0) m = (rnd() & 1) ? (m | 0x7FF000) : (m & 0xFFF);
    return sign | (e << 23) | m;
}
static const int RM[4] = {FE_TONEAREST, FE_TOWARDZERO, FE_UPWARD, FE_DOWNWARD};
static const char *RN[4] = {"rne", "rtz", "rup", "rdn"};
static void flags(char *o) { int f = fetestexcept(FE_ALL_EXCEPT); char *p = o;
    if (f & FE_INVALID) *p++ = 'i'; if (f & FE_DIVBYZERO) *p++ = 'z'; if (f & FE_OVERFLOW) *p++ = 'o';
    if (f & FE_UNDERFLOW) *p++ = 'u'; if (f & FE_INEXACT) *p++ = 'x'; *p = 0; }
int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 2000; char fl[8];
    const char *ops[] = {"add", "sub", "mul", "div", "sqrt", "fma"};
    for (int r = 0; r < 4; r++) for (int o = 0; o < 6; o++) for (int i = 0; i < n; i++) {
        uint64_t a = gen64(), b = gen64(), c = gen64(), x; double da, db, dc, dx; memcpy(&da,&a,8); memcpy(&db,&b,8); memcpy(&dc,&c,8);
        fesetround(RM[r]); feclearexcept(FE_ALL_EXCEPT);
        volatile double va = da, vb = db, vc = dc; double res;
        switch (o) { case 0: res = va + vb; break; case 1: res = va - vb; break; case 2: res = va * vb; break;
                     case 3: res = va / vb; break; case 4: res = sqrt(va); break; default: res = fma(va, vb, vc); }
        volatile double vr = res; flags(fl); fesetround(FE_TONEAREST); dx = vr; memcpy(&x,&dx,8);
        printf("%s 64 %s %016llx %016llx %016llx %016llx %s\n", ops[o], RN[r], (unsigned long long)a, (unsigned long long)b, (unsigned long long)c, (unsigned long long)x, fl);
        uint32_t a3 = gen32(), b3 = gen32(), c3 = gen32(), x3; float fa, fb, fc, fx; memcpy(&fa,&a3,4); memcpy(&fb,&b3,4); memcpy(&fc,&c3,4);
        fesetround(RM[r]); feclearexcept(FE_ALL_EXCEPT);
        volatile float wa = fa, wb = fb, wc = fc; float rf;
        switch (o) { case 0: rf = wa + wb; break; case 1: rf = wa - wb; break; case 2: rf = wa * wb; break;
                     case 3: rf = wa / wb; break; case 4: rf = sqrtf(wa); break; default: rf = fmaf(wa, wb, wc); }
        volatile float wr = rf; flags(fl); fesetround(FE_TONEAREST); fx = wr; memcpy(&x3,&fx,4);
        printf("%s 32 %s %08x %08x %08x %08x %s\n", ops[o], RN[r], a3, b3, c3, x3, fl);
    }
    return 0;
}
