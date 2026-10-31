/* dense.c - every binary32 input in a contiguous range, one of the eight shared 9.2
 * functions, one rounding attribute: muse (native HEAD) against cft (native HEAD).
 *   dense <fn> <start_hex> <count> <RNE|RTZ|RUP|RDN|RMM>
 * Prints a one-line summary and every disagreement that is not a NaN-payload difference.
 * hypot sweeps x over the range with y taken from a fixed 61-value set. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "muse_softfloat.h"
#include "cft.h"

static int isnan32(uint32_t x) { return (x & 0x7f800000u) == 0x7f800000u && (x & 0x007fffffu); }

int main(int argc, char **argv) {
    if (argc != 5) return 2;
    const char *fn = argv[1]; uint32_t start = (uint32_t)strtoul(argv[2], 0, 16); long count = atol(argv[3]);
    const char *rs = argv[4];
    msf_rounding_t mr = !strcmp(rs, "RNE") ? MSF_ROUND_TIES_TO_EVEN : !strcmp(rs, "RTZ") ? MSF_ROUND_TOWARD_ZERO
                      : !strcmp(rs, "RUP") ? MSF_ROUND_TOWARD_POSITIVE : !strcmp(rs, "RDN") ? MSF_ROUND_TOWARD_NEGATIVE : MSF_ROUND_TIES_TO_AWAY;
    cft_round cr = !strcmp(rs, "RNE") ? CFT_RNE : !strcmp(rs, "RTZ") ? CFT_RTZ : !strcmp(rs, "RUP") ? CFT_RUP : !strcmp(rs, "RDN") ? CFT_RDN : CFT_RMM;
    cft_device *dev; if (cft_open(NULL, 0, &dev) != CFT_OK) return 3;
    enum { B = 4096 };
    static uint32_t a[B], b[B], d[B];
    static const uint32_t Y[61] = { 0x00000000, 0x80000000, 0x00000001, 0x007fffff, 0x00800000, 0x3f800000, 0xbf800000, 0x40000000,
        0x3f000000, 0x40400000, 0x40800000, 0x7f7fffff, 0x7f800000, 0xff800000, 0x3eaaaaab, 0x3f3504f3, 0x3fb504f3, 0x40490fdb,
        0x1f800000, 0x5f800000, 0x00400000, 0x3f7fffff, 0x3f800001, 0x4b800000, 0x33800000, 0x2b800000, 0x53800000, 0x0c000000,
        0x72800000, 0x3fc00000, 0x40a00000, 0x41200000, 0x42c80000, 0x447a0000, 0x461c4000, 0x47c35000, 0x49742400, 0x4b189680,
        0x1a000000, 0x65000000, 0x3dcccccd, 0x3e4ccccd, 0x3e99999a, 0x3ecccccd, 0x3f19999a, 0x3f333333, 0x3f4ccccd, 0x3f666666,
        0x3f8ccccd, 0x3f99999a, 0x3fa66666, 0x3fb33333, 0x3fcccccd, 0x3fd9999a, 0x3fe66666, 0x3ff33333, 0x00000010, 0x00100000,
        0x7f000000, 0x01000000, 0x7e800000 };
    long n = 0, same = 0, nanpay = 0, diff = 0;
    for (long base = 0; base < count; base += B) {
        int m = (int)(count - base < B ? count - base : B);
        for (int i = 0; i < m; i++) { a[i] = start + (uint32_t)(base + i); b[i] = Y[(base + i) % 61]; }
        uint32_t cfl_unused = 0; (void)cfl_unused;
        for (int i = 0; i < m; i++) {
            /* cft per element so each gets its own flag word */
            uint32_t cf = 0, cd = 0, x = a[i], y = b[i];
            if (!strcmp(fn, "exp2")) cft_exp2(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "exp2m1")) cft_exp2m1(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "log2")) cft_log2(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "log2p1")) cft_log2p1(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "sinpi")) cft_sinpi(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "cospi")) cft_cospi(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "rsqrt")) cft_rsqrt(dev, CFT_FP32, cr, &x, &cd, 1, &cf);
            else if (!strcmp(fn, "hypot")) cft_hypot(dev, CFT_FP32, cr, &x, &y, &cd, 1, &cf);
            msf_flags_t mf = 0; uint32_t md;
            if (!strcmp(fn, "exp2")) md = msf32_exp2(x, mr, &mf);
            else if (!strcmp(fn, "exp2m1")) md = msf32_exp2m1(x, mr, &mf);
            else if (!strcmp(fn, "log2")) md = msf32_log2(x, mr, &mf);
            else if (!strcmp(fn, "log2p1")) md = msf32_log2p1(x, mr, &mf);
            else if (!strcmp(fn, "sinpi")) md = msf32_sin_pi(x, mr, &mf);
            else if (!strcmp(fn, "cospi")) md = msf32_cos_pi(x, mr, &mf);
            else if (!strcmp(fn, "rsqrt")) md = msf32_r_sqrt(x, mr, &mf);
            else md = msf32_hypot(x, y, mr, &mf);
            n++;
            if (md == cd && mf == cf) same++;
            else if (isnan32(md) && isnan32(cd) && mf == cf) nanpay++;
            else { diff++; if (diff <= 20) printf("DIFF %s %s x=%08x y=%08x muse %08x/%02x cft %08x/%02x\n", fn, rs, x, y, md, mf, cd, cf); }
        }
    }
    printf("SUMMARY %s %s start=%08x count=%ld: same %ld nan-payload %ld differ %ld\n", fn, rs, start, n, same, nanpay, diff);
    cft_close(dev);
    return 0;
}
