#ifndef TELEMETRY_GUARD_H
#define TELEMETRY_GUARD_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if defined(_WIN32) || defined(_WIN64)
#include <windows.h>
#include <winhttp.h>
#endif

// สลับจุดยิง Handshake มาที่ GCP Cloud Run Endpoint จริง
#define KMS_HOST L"bangsaen-kms-gateway-653731256449.asia-southeast1.run.app"
#define KMS_PATH L"/v1/auth-key"

static int verify_environment_telemetry(void) {
#if defined(_WIN32) || defined(_WIN64)
    HINTERNET hSession = WinHttpOpen(L"BangsaenActiveDefense/1.0",
                                     WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
                                     WINHTTP_NO_PROXY_NAME,
                                     WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) return -1;

    // เชื่อมต่อผ่าน HTTPS Port 443
    HINTERNET hConnect = WinHttpConnect(hSession, KMS_HOST, INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConnect) {
        WinHttpCloseHandle(hSession);
        return -1;
    }

    HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"GET", KMS_PATH,
                                            NULL, WINHTTP_NO_REFERER,
                                            WINHTTP_DEFAULT_ACCEPT_TYPES,
                                            WINHTTP_FLAG_SECURE); // ใช้ SSL/TLS
    if (!hRequest) {
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return -1;
    }

    // ดึง Bearer Token จาก Environment Variable ในเครื่อง
    char* bearer_token = getenv("BANGSAEN_GCP_AUTH_BEARER");
    wchar_t headers[256] = L"";
    if (bearer_token != NULL) {
        swprintf(headers, 256, L"Authorization: Bearer %hs\r\n", bearer_token);
        WinHttpAddRequestHeaders(hRequest, headers, (DWORD)-1L, WINHTTP_ADDREQ_FLAG_ADD);
    }

    BOOL bResults = WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0,
                                       WINHTTP_NO_REQUEST_DATA, 0, 0, 0);

    if (bResults) {
        bResults = WinHttpReceiveResponse(hRequest, NULL);
    }

    DWORD dwStatusCode = 0;
    DWORD dwSize = sizeof(dwStatusCode);

    if (bResults) {
        WinHttpQueryHeaders(hRequest,
                            WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
                            WINHTTP_HEADER_NAME_BY_INDEX,
                            &dwStatusCode, &dwSize, WINHTTP_NO_HEADER_INDEX);
    }

    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    // คืนค่า 0 หาก GCP Cloud Run ตอบกลับ 200 OK
    return (dwStatusCode == 200) ? 0 : -1;
#else
    return -1;
#endif
}

#endif // TELEMETRY_GUARD_H