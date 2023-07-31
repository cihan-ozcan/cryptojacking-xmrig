#include <windows.h>
#include <stdio.h>

bool StopWindowsUpdateService()
{
    const wchar_t* serviceName = L"wuauserv"; // Windows Update Hizmeti

    // SCM veritabanýna bir kulp aç.
    SC_HANDLE schSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);

    if (NULL == schSCManager)
    {
        printf("OpenSCManager baþarýsýz (%d)\n", GetLastError());
        return false;
    }

    // Hizmete bir kulp aç.
    SC_HANDLE schService = OpenServiceW(schSCManager, serviceName, SERVICE_ALL_ACCESS);

    if (schService == NULL)
    {
        printf("OpenService baþarýsýz (%d)\n", GetLastError());
        CloseServiceHandle(schSCManager);
        return false;
    }

    SERVICE_STATUS serviceStatus;
    // Hizmete durdurma komutu gönder.
    if (!ControlService(schService, SERVICE_CONTROL_STOP, &serviceStatus))
    {
        printf("ControlService baþarýsýz (%d)\n", GetLastError());
    }

    CloseServiceHandle(schService);
    CloseServiceHandle(schSCManager);

    return true;
}

int main()
{
    StopWindowsUpdateService();
    return 0;
}
