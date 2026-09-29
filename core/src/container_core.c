#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "../include/telemetry_guard.h"
#include "../include/chaos_matrix.h"
#include "../include/lethal_shredder.h"
#include "../include/generated_vip_data.h"

static PyObject* extract_vip_context(PyObject* self, PyObject* args) {
    // 1. จอง Writable Heap Memory Buffer สำหรับเก็บ Encrypted Payload
    unsigned char *volatile_buffer = (unsigned char *)malloc(VIP_RAW_DATA_LEN);
    if (volatile_buffer == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate volatile memory buffer");
        return NULL;
    }

    // คัดลอก Encrypted Bytes จาก Read-Only Header ลง Writable Heap
    memcpy(volatile_buffer, VIP_RAW_DATA, VIP_RAW_DATA_LEN);

    // 2. ตรวจสอบ Telemetry & GCP Cloud KMS Handshake
    if (verify_environment_telemetry() != 0) {
        // หากไม่ผ่าน Handshake -> สั่ง Thanos Null-Space Shredder ล้าง RAM ทิ้งทันที (< 0.12 ms)
        trigger_null_space_shredding((void*)volatile_buffer, VIP_RAW_DATA_LEN);
        return NULL;
    }

    // =========================================================================
    // 3. [จุดใส่โค้ด]: คลายรหัสชั่วคราว -> ส่งให้ Python String -> ล้าง RAM ทิ้งทันที!
    // =========================================================================
    for (size_t i = 0; i < VIP_RAW_DATA_LEN; i++) {
        unsigned char chaos_key = (unsigned char)((i * 17 + 0x5A) % 256);
        volatile_buffer[i] ^= chaos_key;
    }

    // แปลง Memory Buffer ชั่วคราวให้กลายเป็น PyObject (Python String)
    PyObject *result = PyUnicode_FromStringAndSize((const char*)volatile_buffer, VIP_RAW_DATA_LEN);

    // ทำความสะอาด RAM ด้วย 0x00 ทันทีหลังแปลงเป็น PyObject เสร็จสิ้น (Ephemeral Memory Lifecycle)
    SecureZeroMemory(volatile_buffer, VIP_RAW_DATA_LEN);
    free(volatile_buffer);
    // =========================================================================

    return result;
}

static PyMethodDef ActiveDefenseMethods[] = {
    {"extract_vip_context", extract_vip_context, METH_NOARGS, "Extract VIP record if inside trusted boundary."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef activedefensemodule = {
    PyModuleDef_HEAD_INIT,
    "active_defense_v27",
    "Bangsaen Sovereign Active Defense C-Container",
    -1,
    ActiveDefenseMethods
};

PyMODINIT_FUNC PyInit_active_defense_v27(void) {
    return PyModule_Create(&activedefensemodule);
}