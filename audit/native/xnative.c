/* xnative.c - one C program linking BOTH libraries at HEAD (muse libmsf.a, cft libcft.a,
 * software device) for the operations msf.wasm cannot run: Clause 9.5 augmented pairs
 * and the 5.12 character conversions. Reads one request per line on stdin, writes one
 * line per request with each library's raw answer; judging happens in Python.
 *
 *   AUG <32|64> <add|sub|mul> <a> <b>
 *   FROMDEC <32|64> <RNE|RTZ|RUP|RDN|RMM> <string, no spaces; ~ = empty>
 *   FROMHEX <32|64> <rm> <string>
 *   TODEC <32|64> <rm> <a> <digits>        (digits >= 1: that many significant, scientific)
 *   TOHEX <32|64> <a>                      (shortest exact)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "muse_softfloat.h"
#include "cft.h"

static cft_device *dev;

static msf_rounding_t mrm(const char *s) {
    if (!strcmp(s, "RNE")) return MSF_ROUND_TIES_TO_EVEN;
    if (!strcmp(s, "RTZ")) return MSF_ROUND_TOWARD_ZERO;
    if (!strcmp(s, "RUP")) return MSF_ROUND_TOWARD_POSITIVE;
    if (!strcmp(s, "RDN")) return MSF_ROUND_TOWARD_NEGATIVE;
    if (!strcmp(s, "RMM")) return MSF_ROUND_TIES_TO_AWAY;
    fprintf(stderr, "bad rm %s\n", s); exit(2);
}
static cft_round crm(const char *s) {
    if (!strcmp(s, "RNE")) return CFT_RNE;
    if (!strcmp(s, "RTZ")) return CFT_RTZ;
    if (!strcmp(s, "RUP")) return CFT_RUP;
    if (!strcmp(s, "RDN")) return CFT_RDN;
    if (!strcmp(s, "RMM")) return CFT_RMM;
    fprintf(stderr, "bad rm %s\n", s); exit(2);
}

int main(void) {
    static char line[1 << 20], mbuf[1 << 19], cbuf[1 << 19];
    if (cft_open(NULL, 0, &dev) != CFT_OK) {   /* NULL artifact: the software backend */
        fprintf(stderr, "cft_open failed: %s\n", cft_last_error()); return 2;
    }
    while (fgets(line, sizeof line, stdin)) {
        char kind[16], fs[8], a1[64], a2[64], rm[8];
        size_t L = strlen(line);
        while (L && (line[L - 1] == '\n' || line[L - 1] == '\r')) line[--L] = 0;
        if (sscanf(line, "%15s %7s", kind, fs) != 2) continue;
        int F = atoi(fs);
        cft_format cf = F == 32 ? CFT_FP32 : CFT_FP64;
        if (!strcmp(kind, "AUG")) {
            char fn[8]; sscanf(line, "%*s %*s %7s %63s %63s", fn, a1, a2);
            uint64_t a = strtoull(a1, 0, 16), b = strtoull(a2, 0, 16), mh, mt, cr = 0, ce = 0;
            msf_flags_t mf = 0; uint32_t cfl = 0; cft_status st;
            if (F == 32) {
                msf32_pair_t p = !strcmp(fn, "add") ? msf32_augmented_add((msf32_t)a, (msf32_t)b, &mf)
                               : !strcmp(fn, "sub") ? msf32_augmented_sub((msf32_t)a, (msf32_t)b, &mf)
                               : msf32_augmented_mul((msf32_t)a, (msf32_t)b, &mf);
                mh = p.head; mt = p.tail;
                uint32_t x = (uint32_t)a, y = (uint32_t)b, r, e;
                st = (!strcmp(fn, "add") ? cft_augmented_add : !strcmp(fn, "sub") ? cft_augmented_sub : cft_augmented_mul)(dev, cf, &x, &y, &r, &e, 1, &cfl);
                cr = r; ce = e;
            } else {
                msf64_pair_t p = !strcmp(fn, "add") ? msf64_augmented_add(a, b, &mf)
                               : !strcmp(fn, "sub") ? msf64_augmented_sub(a, b, &mf)
                               : msf64_augmented_mul(a, b, &mf);
                mh = p.head; mt = p.tail;
                uint64_t r, e;
                st = (!strcmp(fn, "add") ? cft_augmented_add : !strcmp(fn, "sub") ? cft_augmented_sub : cft_augmented_mul)(dev, cf, &a, &b, &r, &e, 1, &cfl);
                cr = r; ce = e;
            }
            printf("%s | muse %llx %llx %02x | cft %d %llx %llx %02x\n", line, (unsigned long long)mh, (unsigned long long)mt, mf,
                   (int)st, (unsigned long long)cr, (unsigned long long)ce, cfl);
        } else if (!strcmp(kind, "FROMDEC") || !strcmp(kind, "FROMHEX")) {
            int hex = kind[4] == 'H';
            const char *p = line; for (int k = 0; k < 3; k++) { p = strchr(p, ' '); if (!p) break; p++; }
            sscanf(line, "%*s %*s %7s", rm);
            const char *s = (p && strcmp(p, "~")) ? p : "";
            size_t consumed = 0; msf_flags_t mf = 0; uint64_t mv; uint32_t cfl = 0; size_t bad = 0; cft_status st;
            uint64_t cv = 0;
            if (F == 32) {
                mv = hex ? msf32_from_hex(s, &consumed, mrm(rm), &mf) : msf32_from_decimal(s, &consumed, mrm(rm), &mf);
                uint32_t d = 0; st = (hex ? cft_from_hex_char : cft_from_decimal_char)(dev, cf, crm(rm), &s, &d, 1, &bad, &cfl); cv = d;
            } else {
                mv = hex ? msf64_from_hex(s, &consumed, mrm(rm), &mf) : msf64_from_decimal(s, &consumed, mrm(rm), &mf);
                uint64_t d = 0; st = (hex ? cft_from_hex_char : cft_from_decimal_char)(dev, cf, crm(rm), &s, &d, 1, &bad, &cfl); cv = d;
            }
            printf("%s | muse %llx %02x C=%zu len=%zu | cft %d %llx %02x\n", line, (unsigned long long)mv, mf, consumed, strlen(s),
                   (int)st, (unsigned long long)cv, cfl);
        } else if (!strcmp(kind, "TODEC")) {
            int digits; sscanf(line, "%*s %*s %7s %63s %d", rm, a1, &digits);
            uint64_t a = strtoull(a1, 0, 16); msf_flags_t mf = 0; uint32_t cfl = 0; size_t clen = 0; cft_status st;
            msf_decimal_spec_t spec = { digits, MSF_DECIMAL_STYLE_SCIENTIFIC, 0 };
            size_t ml;
            if (F == 32) {
                ml = msf32_to_decimal((msf32_t)a, &spec, mbuf, sizeof mbuf, mrm(rm), &mf);
                uint32_t x = (uint32_t)a; st = cft_to_decimal_char(dev, cf, crm(rm), &x, (size_t)digits, cbuf, sizeof cbuf, &clen, &cfl);
            } else {
                ml = msf64_to_decimal(a, &spec, mbuf, sizeof mbuf, mrm(rm), &mf);
                st = cft_to_decimal_char(dev, cf, crm(rm), &a, (size_t)digits, cbuf, sizeof cbuf, &clen, &cfl);
            }
            if (ml >= sizeof mbuf) strcpy(mbuf, "<overflow>");
            if (st != CFT_OK) strcpy(cbuf, "<refused>");
            printf("%s | muse %s %02x | cft %d %s %02x\n", line, mbuf, mf, (int)st, cbuf, cfl);
        } else if (!strcmp(kind, "TOHEX")) {
            sscanf(line, "%*s %*s %63s", a1);
            uint64_t a = strtoull(a1, 0, 16); msf_flags_t mf = 0; size_t clen = 0; cft_status st;
            msf_hex_spec_t spec; memset(&spec, 0, sizeof spec); spec.precision = -1;   /* shortest exact */
            if (F == 32) {
                msf32_to_hex((msf32_t)a, &spec, mbuf, sizeof mbuf, MSF_ROUND_TIES_TO_EVEN, &mf);
                uint32_t x = (uint32_t)a; st = cft_to_hex_char(dev, cf, &x, cbuf, sizeof cbuf, &clen);
            } else {
                msf64_to_hex(a, &spec, mbuf, sizeof mbuf, MSF_ROUND_TIES_TO_EVEN, &mf);
                st = cft_to_hex_char(dev, cf, &a, cbuf, sizeof cbuf, &clen);
            }
            if (st != CFT_OK) strcpy(cbuf, "<refused>");
            printf("%s | muse %s %02x | cft %d %s\n", line, mbuf, mf, (int)st, cbuf);
        }
    }
    cft_close(dev);
    return 0;
}
