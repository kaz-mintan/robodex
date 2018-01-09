/*---------------------------------------------------------------------------*/
/* Copyright(C)  2017  OMRON Corporation                                     */
/*                                                                           */
/* Licensed under the Apache License, Version 2.0 (the "License");           */
/* you may not use this file except in compliance with the License.          */
/* You may obtain a copy of the License at                                   */
/*                                                                           */
/*     http://www.apache.org/licenses/LICENSE-2.0                            */
/*                                                                           */
/* Unless required by applicable law or agreed to in writing, software       */
/* distributed under the License is distributed on an "AS IS" BASIS,         */
/* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  */
/* See the License for the specific language governing permissions and       */
/* limitations under the License.                                            */
/*---------------------------------------------------------------------------*/

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#define INVALID_HANDLE_VALUE -1
#define TRUE 1
typedef int HANDLE;
typedef short BOOL;
typedef unsigned short DWORD;
typedef long LONG;
typedef long long LONGLONG;
typedef union _LARGE_INTEGER {
    struct {
        DWORD LowPart;
        LONG HighPart;
    };
    struct {
        DWORD LowPart;
        LONG HighPart;
    } u;
    LONGLONG QuadPart;
} LARGE_INTEGER;
#endif
#include <stdio.h>
#include "uart.h"

static HANDLE hCom = INVALID_HANDLE_VALUE;

/* UART */
void com_close(void)
{
    if ( hCom != INVALID_HANDLE_VALUE ) {
        close(hCom);
        //CloseHandle(hCom);
        hCom = INVALID_HANDLE_VALUE;
    }
}

int com_init(S_STAT *stat)
{
    BOOL fSuccess;
    char device[16];
    struct termios oldtio, newtio;    /* シリアル通信設定 */

    com_close();
   
    hCom =open("/dev/ttyACM0", O_RDWR | O_NOCTTY);
    printf("hCom = %d\n", hCom);
    ioctl(hCom, TCGETS, &oldtio);       /* 現在のシリアルポートの設定を待避させる */
    newtio = oldtio;                  /* ポートの設定をコピー */


		struct termios tty;
        //int baudRate = 921600;
        int baudRate=9600;
		memset(&tty,0,sizeof(tty));
		tty.c_cflag=CS8|CLOCAL|CREAD;
		tty.c_cc[VMIN]=0;
		tty.c_cc[VTIME]=0;
		cfsetospeed(&tty, baudRate);
		cfsetispeed(&tty, baudRate);
		tcflush(hCom,TCIFLUSH);
		tcsetattr(hCom,TCSANOW,&tty);
   // ioctl(hCom, TCSETS, &newtio);       /* ポートの設定を有効にする */ 

/*
    
    DCB dcb;
    sprintf_s(device, 16, "\\\\.\\COM%d", stat->com_num);
    hCom = CreateFile(device,
                        GENERIC_READ | GENERIC_WRITE,
                        0,
                        NULL,
                        OPEN_EXISTING,
                        0,
                        NULL);

    if ( hCom == INVALID_HANDLE_VALUE ) {
        return(FALSE);
    }

    fSuccess = GetCommState(hCom,&dcb);
    if ( !fSuccess ) {
        com_close();
        return(FALSE);
    }

    dcb.BaudRate = stat->BaudRate;
    dcb.ByteSize = 8;
    dcb.Parity   = NOPARITY;
    dcb.StopBits = ONESTOPBIT;
    dcb.fDsrSensitivity = FALSE;
    dcb.fOutxCtsFlow = 0;
    dcb.fTXContinueOnXoff = 0;
    dcb.fRtsControl = RTS_CONTROL_DISABLE;
    dcb.fDtrControl = DTR_CONTROL_DISABLE;

    fSuccess = SetCommState(hCom,&dcb);
    if ( !fSuccess ) {
        com_close();
        return(FALSE);
    }

    fSuccess = SetupComm(hCom, 10240, 10240);
    if ( !fSuccess ) {
        com_close();
        return(FALSE);
    }
*/
    return TRUE;
}

int com_send(unsigned char *buf, int len)
{
    DWORD dwSize = 0;
    if ( hCom != INVALID_HANDLE_VALUE ) {

        dwSize = write(hCom, buf, len);
        //WriteFile(hCom,buf,len,&dwSize,NULL);
    }
    return (int)dwSize;
}

int com_recv(int inTimeOutTimer, unsigned char *buf, int len)
{
    DWORD ierr;
    //COMSTAT stat;
    DWORD dwSize = 0;

    int ret = 0;
    int totalSize = 0;
    int retSize = 0;
    int offSize = 0;
    double finishTime = 0.0;

    LARGE_INTEGER timeFreq = {0, 0};
    LARGE_INTEGER stopTime = {0, 0};
    LARGE_INTEGER startTime = {0, 0};

    // QueryPerformanceFrequency(&timeFreq);

    static char lbuf[19200 * 4];
    int cntErr = 0;
    if ( hCom != INVALID_HANDLE_VALUE ) {
        //QueryPerformanceCounter(&startTime);
        do{
            offSize = len - totalSize;
            // printf("%d, %d, %d\n", offSize, totalSize, len);
            retSize = read(hCom, &lbuf[totalSize], offSize);
            // printf("retSize = %d\n", retSize);
            memcpy(&buf[totalSize], &lbuf[totalSize], retSize);
            usleep(1000);
            if(retSize > 0)
                totalSize += retSize;
            else{
                cntErr++;
            }
            if(cntErr > 2500)
                break;            
	    /*
            ClearCommError(hCom,&ierr,&stat);
            if ( stat.cbInQue >= 1 ) {
                ret = len - totalSize;
                if ( ret > (int)stat.cbInQue ) ret = stat.cbInQue;
                ReadFile(hCom,&buf[totalSize],ret,&dwSize,NULL);
                totalSize += (int)dwSize;
            }
	    */
            if ( totalSize >= len ) break;

           // QueryPerformanceCounter(&stopTime);
           // finishTime = (double)(stopTime.QuadPart - startTime.QuadPart) * 1000 / (double)timeFreq.QuadPart;
           // if ( finishTime >= (double)inTimeOutTimer ) break;
           // break;
        }while(1);
    }
    return totalSize;
}
