/* exp2m1_probe.c - cft-fp256's exp2m1 at x = emax+1, every attribute, all four of its formats, and
 * muse-softfloat's at the two formats it shares, against what IEEE 754-2019 7.4 requires:
 * 2^(emax+1) - 1 rounds to maxFinite with inexact alone under roundTowardZero and roundTowardNegative,
 * and overflows (+inf, overflow and inexact) under the other three.
 * Prints one line per case and a closing count. Exits 0 either way: a probe reports, the run judges. */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "muse_softfloat.h"
#include "cft.h"

static const char *RN[5] = { "roundTiesToEven", "roundTowardZero", "roundTowardNegative", "roundTowardPositive", "roundTiesToAway" };
static const cft_round CR[5] = { CFT_RNE, CFT_RTZ, CFT_RDN, CFT_RUP, CFT_RMM };
static const msf_rounding_t MR[5] = { MSF_ROUND_TIES_TO_EVEN, MSF_ROUND_TOWARD_ZERO, MSF_ROUND_TOWARD_NEGATIVE,
                                      MSF_ROUND_TOWARD_POSITIVE, MSF_ROUND_TIES_TO_AWAY };

int main(void) {
    cft_device *dev;
    if (cft_open(NULL, 0, &dev) != CFT_OK) { printf("cft_open failed\n"); return 2; }
    /* little-endian encodings of the integer emax+1 = 2^E, and of the expected results */
    struct { const char *name; cft_format f; int bytes, ebits; long x; } T[4] = {
        { "binary32", CFT_FP32, 4, 8, 128 }, { "binary64", CFT_FP64, 8, 11, 1024 },
        { "binary128", CFT_FP128, 16, 15, 16384 }, { "binary256", CFT_FP256, 32, 19, 262144 } };
    int bad = 0, cases = 0;
    for (int k = 0; k < 4; k++) {
        unsigned char x[32] = { 0 }, maxf[32] = { 0 }, inf[32] = { 0 };
        int bits = T[k].bytes * 8, fbits = bits - 1 - T[k].ebits, bias = (1 << (T[k].ebits - 1)) - 1, lg = 0;
        for (long v = T[k].x; v > 1; v >>= 1) lg++;
        for (int b = 0; b < T[k].ebits; b++) {
            if ((unsigned)(bias + lg) >> b & 1) x[(fbits + b) / 8] |= (unsigned char)(1u << ((fbits + b) % 8));
            inf[(fbits + b) / 8] |= (unsigned char)(1u << ((fbits + b) % 8));                 /* all-ones exponent */
            if (b) maxf[(fbits + b) / 8] |= (unsigned char)(1u << ((fbits + b) % 8));         /* exponent 1...10 */
        }
        for (int b = 0; b < fbits; b++) maxf[b / 8] |= (unsigned char)(1u << (b % 8));      /* all-ones fraction */
        for (int r = 0; r < 5; r++) {
            int to_max = (CR[r] == CFT_RTZ || CR[r] == CFT_RDN);
            unsigned char d[32] = { 0 }; uint32_t fl = 0;
            cft_status st = cft_exp2m1(dev, T[k].f, CR[r], x, d, 1, &fl);
            const unsigned char *want = to_max ? maxf : inf;
            uint32_t wfl = to_max ? 0x10u : 0x14u;
            int ok = st == CFT_OK && !memcmp(d, want, (size_t)T[k].bytes) && fl == wfl;
            cases++; bad += !ok;
            printf("cft  %-9s exp2m1(%ld) %-19s -> %s, flags 0x%02x; 754 requires %s, flags 0x%02x  %s\n", T[k].name, T[k].x, RN[r],
                   !memcmp(d, maxf, (size_t)T[k].bytes) ? "maxFinite" : !memcmp(d, inf, (size_t)T[k].bytes) ? "+inf" : "other",
                   fl, to_max ? "maxFinite" : "+inf", wfl, ok ? "ok" : "WRONG");
            if (k < 2) {
                msf_flags_t mf = 0; uint64_t md; uint64_t w64 = 0;
                memcpy(&w64, want, (size_t)T[k].bytes);
                if (k == 0) md = msf32_exp2m1(0x43000000u, MR[r], &mf); else md = msf64_exp2m1(0x4090000000000000ull, MR[r], &mf);
                int mok = md == w64 && mf == wfl;
                cases++; bad += !mok;
                printf("muse %-9s exp2m1(%ld) %-19s -> 0x%llx, flags 0x%02x  %s\n", T[k].name, T[k].x, RN[r], (unsigned long long)md, mf, mok ? "ok" : "WRONG");
            }
        }
    }
    printf("exp2m1 at emax+1: %d cases, %d not as 754-2019 7.4 requires\n", cases, bad);
    cft_close(dev);
    return 0;
}
