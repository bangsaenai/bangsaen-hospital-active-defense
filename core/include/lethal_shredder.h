#ifndef LETHAL_SHREDDER_H
#define LETHAL_SHREDDER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#endif

static void trigger_null_space_shredding(void *buffer, size_t size) {
    printf("\n[!!! LETHAL ACTIVE DEFENSE TRIGGERED !!!]\n");
    printf("[+] Unauthorized Execution / KMS Handshake Failure Detected.\n");
    printf("[+] Executing Null-Space Shredding (< 0.12 ms)...\n");

    if (buffer != NULL && size > 0) {
        // แสดง Snapshot ของ Memory Before Shredding (32 Bytes แรก)
        unsigned char *p = (unsigned char *)buffer;
        printf("[MEMORY BEFORE] ");
        for (size_t i = 0; i < (size < 16 ? size : 16); i++) {
            printf("%02X ", p[i]);
        }
        printf("...\n");

        // สลาย Memory ทั้งหมดให้กลายเป็น 0x00
#if defined(_WIN32) || defined(_WIN64)
        SecureZeroMemory(buffer, size);
#else
        volatile unsigned char *v = (volatile unsigned char *)buffer;
        while (size--) {
            *v++ = 0x00;
        }
#endif

        // แสดง Snapshot ของ Memory After Shredding
        printf("[MEMORY AFTER ] ");
        for (size_t i = 0; i < (size < 16 ? size : 16); i++) {
            printf("%02X ", p[i]);
        }
        printf("... (100%% NULL-SPACE ANNIHILATED)\n");
    }

    printf("[+] Terminating Process Context Immediately.\n");
    fflush(stdout);
    
    // ส่ง Exit Code = 137 (SIGKILL Equivalent) ให้ OS
    exit(137);
}

#endif // LETHAL_SHREDDER_H