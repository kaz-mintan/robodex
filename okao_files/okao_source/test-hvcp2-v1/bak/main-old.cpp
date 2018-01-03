#include <stdio.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include <stdarg.h>
#include <unistd.h>
#include <fcntl.h>

#include <termios.h>

#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define WINDOW_NAME "JBCRD-Face Recong"
#include "cvui.h"

#include "uart.h"
#include "HVCApi.h"
#include "HVCDef.h"
#include "HVCExtraUartFunc.h"

#define sprintf_s(__Dest, __Len, ...) sprintf(__Dest, __VA_ARGS__)

#define UART_SETTING_TIMEOUT              1000            /* HVC setting command signal timeout period */
#define UART_EXECUTE_TIMEOUT              ((10+10+6+3+15+15+1+1+15+10)*1000)
#define UART_REGIST_EXECUTE_TIMEOUT       7000            /* HVC registration command signal timeout period */
#define LOGBUFFERSIZE                   8192
#define SENSOR_ROLL_ANGLE_DEFAULT            0            /* Camera angle setting (0°) */
#define BODY_THRESHOLD_DEFAULT             500            /* Threshold for Human Body Detection */
#define FACE_THRESHOLD_DEFAULT             500            /* Threshold for Face Detection */
#define HAND_THRESHOLD_DEFAULT             500            /* Threshold for Hand Detection */
#define REC_THRESHOLD_DEFAULT              500            /* Threshold for Face Recognition */

#define BODY_SIZE_RANGE_MIN_DEFAULT         30            /* Human Body Detection minimum detection size */
#define BODY_SIZE_RANGE_MAX_DEFAULT       8192            /* Human Body Detection maximum detection size */
#define HAND_SIZE_RANGE_MIN_DEFAULT         40            /* Hand Detection minimum detection size */
#define HAND_SIZE_RANGE_MAX_DEFAULT       8192            /* Hand Detection maximum detection size */
#define FACE_SIZE_RANGE_MIN_DEFAULT         64            /* Face Detection minimum detection size */
#define FACE_SIZE_RANGE_MAX_DEFAULT       8192            /* Face Detection maximum detection size */

#define FACE_POSE_DEFAULT                    0            /* Face Detection facial pose (frontal face)*/
#define FACE_ANGLE_DEFAULT                   0            /* Face Detection roll angle (±15°)*/


/*----------------------------------------------------------------------------*/
/* UART send signal                                                           */
/* param    : int   inDataSize  send signal data                              */
/*          : UINT8 *inData     data length                                   */
/* return   : int               send signal complete data number              */
/*----------------------------------------------------------------------------*/
int UART_SendData(int inDataSize, UINT8 *inData)
{
    /* Send Data */
    int ret = com_send(inData, inDataSize);
    return ret;
}

/*----------------------------------------------------------------------------*/
/* UART receive signal                                                        */
/* param    : int   inTimeOutTime   timeout time (ms)                         */
/*          : int   *inDataSize     receive signal data size                  */
/*          : UINT8 *outResult      receive signal data                       */
/* return   : int                   receive signal complete data number       */
/*----------------------------------------------------------------------------*/
int UART_ReceiveData(int inTimeOutTime, int inDataSize, UINT8 *outResult)
{
    /* Receive Data */
    int ret = com_recv(inTimeOutTime, outResult, inDataSize);
    return ret;
}


int kbhit(void)
{
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if (ch != EOF) {
        ungetc(ch, stdin);
        return 1;
    }

    return 0;
}

/* Print Log Message */
static void PrintLog(char *pStr)
{
    puts(pStr);
}


int main(int argc, char *argv[])
{
    INT32 ret = 0;  /* Return code */

    INT32 inRate;
    int listBaudRate[] = {
                              9600,
                             38400,
                            115200,
                            230400,
                            460800,
                            921600
                         };

    UINT8 status;
    HVC_VERSION version;
    HVC_RESULT *pHVCResult = NULL;
    INT32 agleNo;
    HVC_THRESHOLD threshold;
    HVC_SIZERANGE sizeRange;
    INT32 pose;
    INT32 angle;
    INT32 timeOutTime;
    INT32 execFlag;
    INT32 imageNo;

    char *pExStr[] = {"?", "Neutral", "Happiness", "Surprise", "Anger", "Sadness"};

    int i;
    int ch = 0;
    int revision;
    char *pStr;                     /* String Buffer for logging output */

    S_STAT serialStat;              /* Serial port set value*/

    serialStat.com_num = 0;
    serialStat.BaudRate = 0;        /* Default Baudrate = 9600 */
    if ( argc >= 2 ){
        serialStat.com_num  = atoi(argv[1]);
    }
    if ( com_init(&serialStat) == 0 ) {
        PrintLog("Failed to open COM port.\n");
        return (-1);
    }

    if ( argc >= 3 ){
        serialStat.BaudRate = atoi(argv[2]);
        for ( inRate = 0; inRate<sizeof(listBaudRate); inRate++ ) {
            if ( listBaudRate[inRate] == (int)serialStat.BaudRate ) {
                break;
            }
        }
        if ( inRate >= sizeof(listBaudRate) ) {
            PrintLog("Failed to set baudrate.\n");
            return (-1);
        }

        /* Change Baudrate */
/*
        ret = HVC_SetBaudRate(UART_SETTING_TIMEOUT, inRate, &status);
        if ( (ret != 0) || (status != 0) ) {
            PrintLog("HVCApi(HVC_SetBaudRate) Error.\n");
            return (-1);
        }
        if ( com_init(&serialStat) == 0 ) {
            PrintLog("Failed to open COM port.\n");
            return (-1);
        }
*/
    }
    
    /*****************************/
    /* Logging Buffer allocation */
    /*****************************/
    pStr = (char *)malloc(LOGBUFFERSIZE);
    if ( pStr == NULL ) {
        PrintLog("Failed to allocate Logging Buffer.\n");
        return (-1);
    }
    memset(pStr, 0, LOGBUFFERSIZE);


    do {
        /*********************************/
        /* Result Structure Allocation   */
        /*********************************/
        pHVCResult = (HVC_RESULT *)malloc(sizeof(HVC_RESULT));
        if ( pHVCResult == NULL ) { /* Error processing */
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nMemory Allocation Error : %08x\n", sizeof(HVC_RESULT));
            break;
        }

        /*********************************/
        /* Get Model and Version         */
        /*********************************/
        ret = HVC_GetVersion(UART_SETTING_TIMEOUT, &version, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_GetVersion) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetVersion Response Error : 0x%02X\n", status);
            break;
        }
        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetVersion : ");
        for(i = 0; i < 12; i++){
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "%c", version.string[i] );
        }
        revision = version.revision[0] + (version.revision[1]<<8) + (version.revision[2]<<16) + (version.revision[3]<<24);
        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "%d.%d.%d.%d", version.major, version.minor, version.relese, revision);

        /*********************************/
        /* Set Camera Angle              */
        /*********************************/
        agleNo = SENSOR_ROLL_ANGLE_DEFAULT;
        ret = HVC_SetCameraAngle(UART_SETTING_TIMEOUT, agleNo, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_SetCameraAngle) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_SetCameraAngle Response Error : 0x%02X\n", status);
            break;
        }
        agleNo = 0xff;
        ret = HVC_GetCameraAngle(UART_SETTING_TIMEOUT, &agleNo, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_GetCameraAngle) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetCameraAngle Response Error : 0x%02X\n", status);
            break;
        }
        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetCameraAngle : 0x%02x", agleNo);

        /*********************************/
        /* Set Threshold Values          */
        /*********************************/
        threshold.bdThreshold = BODY_THRESHOLD_DEFAULT;
        threshold.hdThreshold = HAND_THRESHOLD_DEFAULT;
        threshold.dtThreshold = FACE_THRESHOLD_DEFAULT;
        threshold.rsThreshold = REC_THRESHOLD_DEFAULT;

        ret = HVC_SetThreshold(UART_SETTING_TIMEOUT, &threshold, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_SetThreshold) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_SetThreshold Response Error : 0x%02X\n", status);
            break;
        }
        threshold.bdThreshold = 0;
        threshold.hdThreshold = 0;
        threshold.dtThreshold = 0;
        threshold.rsThreshold = 0;
        ret = HVC_GetThreshold(UART_SETTING_TIMEOUT, &threshold, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_GetThreshold) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetThreshold Response Error : 0x%02X\n", status);
            break;
        }
        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetThreshold : Body=%4d Hand=%4d Face=%4d Recognition=%4d",
                 threshold.bdThreshold, threshold.hdThreshold, threshold.dtThreshold, threshold.rsThreshold);

        /*********************************/
        /* Set Detection Size            */
        /*********************************/
        sizeRange.bdMinSize = BODY_SIZE_RANGE_MIN_DEFAULT;
        sizeRange.bdMaxSize = BODY_SIZE_RANGE_MAX_DEFAULT;
        sizeRange.hdMinSize = HAND_SIZE_RANGE_MIN_DEFAULT;
        sizeRange.hdMaxSize = HAND_SIZE_RANGE_MAX_DEFAULT;
        sizeRange.dtMinSize = FACE_SIZE_RANGE_MIN_DEFAULT;
        sizeRange.dtMaxSize = FACE_SIZE_RANGE_MAX_DEFAULT;
        ret = HVC_SetSizeRange(UART_SETTING_TIMEOUT, &sizeRange, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_SetSizeRange) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_SetSizeRange Response Error : 0x%02X\n", status);
            break;
        }
        sizeRange.bdMinSize = 0;
        sizeRange.bdMaxSize = 0;
        sizeRange.hdMinSize = 0;
        sizeRange.hdMaxSize = 0;
        sizeRange.dtMinSize = 0;
        sizeRange.dtMaxSize = 0;
        ret = HVC_GetSizeRange(UART_SETTING_TIMEOUT, &sizeRange, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_GetSizeRange) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetSizeRange Response Error : 0x%02X\n", status);
            break;
        }
        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetSizeRange : Body=(%4d,%4d) Hand=(%4d,%4d) Face=(%4d,%4d)",
                                                            sizeRange.bdMinSize, sizeRange.bdMaxSize,
                                                            sizeRange.hdMinSize, sizeRange.hdMaxSize,
                                                            sizeRange.dtMinSize, sizeRange.dtMaxSize);
        /*********************************/
        /* Set Face Angle                */
        /*********************************/
        pose = FACE_POSE_DEFAULT;
        angle = FACE_ANGLE_DEFAULT;
        ret = HVC_SetFaceDetectionAngle(UART_SETTING_TIMEOUT, pose, angle, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_SetFaceDetectionAngle) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_SetFaceDetectionAngle Response Error : 0x%02X\n", status);
            break;
        }
        pose = 0xff;
        angle = 0xff;
        ret = HVC_GetFaceDetectionAngle(UART_SETTING_TIMEOUT, &pose, &angle, &status);
        if ( ret != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_GetFaceDetectionAngle) Error : %d\n", ret);
            break;
        }
        if ( status != 0 ) {
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetFaceDetectionAngle Response Error : 0x%02X\n", status);
            break;
        }
        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetFaceDetectionAngle : Pose = 0x%02x Angle = 0x%02x", pose, angle);


        cv::namedWindow(WINDOW_NAME, CV_WINDOW_NORMAL);
        cvui::init(WINDOW_NAME);

        cv::Mat frame = cv::Mat(240, 320, CV_8UC3);
        int count = 0;
        do {
            static int flgReg = 0;
            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nPress Space Key to end: ");

            /******************/
            /* Log Output     */
            /******************/
            PrintLog(pStr);

            memset(pStr, 0, LOGBUFFERSIZE);

            /*********************************/
            /* Execute Detection             */
            /*********************************/
            timeOutTime = UART_EXECUTE_TIMEOUT;
            execFlag = HVC_ACTIV_BODY_DETECTION | HVC_ACTIV_HAND_DETECTION | HVC_ACTIV_FACE_DETECTION | HVC_ACTIV_FACE_DIRECTION |
                     HVC_ACTIV_AGE_ESTIMATION | HVC_ACTIV_GENDER_ESTIMATION | HVC_ACTIV_GAZE_ESTIMATION | HVC_ACTIV_BLINK_ESTIMATION |
                     HVC_ACTIV_EXPRESSION_ESTIMATION | HVC_ACTIV_FACE_RECOGNITION;
            imageNo = HVC_EXECUTE_IMAGE_QVGA; /* HVC_EXECUTE_IMAGE_NONE; */

            ret = HVC_ExecuteEx(timeOutTime, execFlag, imageNo, pHVCResult, &status);
            if ( ret != 0 ) {
                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_ExecuteEx) Error : %d\n", ret);
                break;
            }
            if ( status != 0 ) {
                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_ExecuteEx Response Error : 0x%02X\n", status);
                break;
            }
            
            if ( imageNo == HVC_EXECUTE_IMAGE_QVGA_HALF ) {
                //SaveBitmapFile(pHVCResult->image.width, pHVCResult->image.height, pHVCResult->image.image, "SampleImage.bmp");
            }
            for (int i = 0;i < 240;i++)
            {
                for (int j = 0;j < 320;j++)
                {
                    frame.at<cv::Vec3b>(i,j)[0] =  (int)pHVCResult->image.image[i * 320 + j];
                    frame.at<cv::Vec3b>(i,j)[1] =  (int)pHVCResult->image.image[i * 320 + j];
                    frame.at<cv::Vec3b>(i,j)[2] =  (int)pHVCResult->image.image[i * 320 + j];
                }
            }

            if(pHVCResult->executedFunc & HVC_ACTIV_BODY_DETECTION){
                /* Body Detection result string */
                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n Body result count:%d", pHVCResult->bdResult.num);
                for(i = 0; i < pHVCResult->bdResult.num; i++){
                    sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Index:%d \t\tX:%d Y:%d Size:%d Confidence:%d", i,
                                pHVCResult->bdResult.bdResult[i].posX, pHVCResult->bdResult.bdResult[i].posY,
                                pHVCResult->bdResult.bdResult[i].size, pHVCResult->bdResult.bdResult[i].confidence);
                }
            }

            /* Hand Detection result string */
            if(pHVCResult->executedFunc & HVC_ACTIV_HAND_DETECTION){
                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n Hand result count:%d", pHVCResult->hdResult.num);
                for(i = 0; i < pHVCResult->hdResult.num; i++){
                    sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Index:%d \t\tX:%d Y:%d Size:%d Confidence:%d", i,
                                pHVCResult->hdResult.hdResult[i].posX, pHVCResult->hdResult.hdResult[i].posY,
                                pHVCResult->hdResult.hdResult[i].size, pHVCResult->hdResult.hdResult[i].confidence);
                }
            }

            /* Face Detection result string */
            if(pHVCResult->executedFunc &
                    (HVC_ACTIV_FACE_DETECTION | HVC_ACTIV_FACE_DIRECTION |
                     HVC_ACTIV_AGE_ESTIMATION | HVC_ACTIV_GENDER_ESTIMATION |
                     HVC_ACTIV_GAZE_ESTIMATION | HVC_ACTIV_BLINK_ESTIMATION |
                     HVC_ACTIV_EXPRESSION_ESTIMATION | HVC_ACTIV_FACE_RECOGNITION)){
                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n Face result count:%d", pHVCResult->fdResult.num);
                
                if(pHVCResult->fdResult.num == 1)
                {
                    flgReg = 1;
                }
                for(i = 0; i < pHVCResult->fdResult.num; i++){
                    cv::Scalar colorScalar;
                    int colorVal;
                    int centerX;
                    int centerY;
                    int centerW;
                    if(pHVCResult->executedFunc & HVC_ACTIV_FACE_RECOGNITION){
                        /* Recognition */
                        if(-128 == pHVCResult->fdResult.fcResult[i].recognitionResult.uid){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Recognition\tRecognition not possible");
                        }
                        else if(-127 == pHVCResult->fdResult.fcResult[i].recognitionResult.uid){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Recognition\tNot registered");
                        }
                        else{
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Recognition\tID:%d Confidence:%d",
                                        pHVCResult->fdResult.fcResult[i].recognitionResult.uid,
                                        pHVCResult->fdResult.fcResult[i].recognitionResult.confidence);
                        }
                        if(pHVCResult->fdResult.fcResult[i].recognitionResult.uid >= 0)
                        {
                            colorScalar = cv::Scalar( 0, 255, 0 );
                            colorVal = 0x00ff00;
                        }else
                        {
                            colorScalar = cv::Scalar( 255, 0, 0 );
                            colorVal = 0x0000ff;
                        }
                    }


                    if(pHVCResult->executedFunc & HVC_ACTIV_FACE_DETECTION){
                        /* Detection */
                        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Index:%d \t\tX:%d Y:%d Size:%d Confidence:%d", i,
                                    pHVCResult->fdResult.fcResult[i].dtResult.posX, pHVCResult->fdResult.fcResult[i].dtResult.posY,
                                    pHVCResult->fdResult.fcResult[i].dtResult.size, pHVCResult->fdResult.fcResult[i].dtResult.confidence);
                            
                        int sx = pHVCResult->fdResult.fcResult[i].dtResult.posX / 5;
                        int sy = pHVCResult->fdResult.fcResult[i].dtResult.posY / 5;
                        int w = pHVCResult->fdResult.fcResult[i].dtResult.size / 5;
                        cv::rectangle(frame, cv::Point(sx - w / 2,sy - w / 2), cv::Point(sx + w / 2, sy + w / 2), colorScalar, 1, 8);
                        
                        centerX = sx;
                        centerY = sy;
                        centerW = w;
                        char msgUse[16];
                        sprintf(msgUse, "Use:%03d", pHVCResult->fdResult.fcResult[i].recognitionResult.uid);
                        cvui::text(frame, centerX + centerW / 2 + 10, centerY - 36, msgUse, 0.4, colorVal);
                    }

                    if(pHVCResult->executedFunc & HVC_ACTIV_FACE_DIRECTION){
                        /* Face Direction */
                        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Face Direction\tLR:%d UD:%d Roll:%d Confidence:%d",
                                    pHVCResult->fdResult.fcResult[i].dirResult.yaw, pHVCResult->fdResult.fcResult[i].dirResult.pitch,
                                    pHVCResult->fdResult.fcResult[i].dirResult.roll, pHVCResult->fdResult.fcResult[i].dirResult.confidence);
                    }
                    if(pHVCResult->executedFunc & HVC_ACTIV_AGE_ESTIMATION){
                        /* Age */
                        if(-128 == pHVCResult->fdResult.fcResult[i].ageResult.age){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Age\t\tEstimation not possible");
                        } else {
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Age\t\tAge:%d Confidence:%d",
                                        pHVCResult->fdResult.fcResult[i].ageResult.age, pHVCResult->fdResult.fcResult[i].ageResult.confidence);
                        }
                        char msgAge[16];
                        sprintf(msgAge, "Age:%03d", pHVCResult->fdResult.fcResult[i].ageResult.age);
                        cvui::text(frame, centerX + centerW / 2 + 10, centerY - 18, msgAge, 0.4, colorVal);
                    }
                    if(pHVCResult->executedFunc & HVC_ACTIV_GENDER_ESTIMATION){
                        /* Gender */
                        if(-128 == pHVCResult->fdResult.fcResult[i].genderResult.gender){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Gender\t\tEstimation not possible");
                        }
                        else{
                            char msgGen[16];                            
                            if(1 == pHVCResult->fdResult.fcResult[i].genderResult.gender){
                                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Gender\t\tGender:%s Confidence:%d",
                                            "Male", pHVCResult->fdResult.fcResult[i].genderResult.confidence);
                                sprintf(msgGen, "Gender:%s", "Male");                
                            }
                            else{
                                sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Gender\t\tGender:%s Confidence:%d",
                                            "Female", pHVCResult->fdResult.fcResult[i].genderResult.confidence);
                                sprintf(msgGen, "Gender:%s", "Feale");                
                            }
                            cvui::text(frame, centerX + centerW / 2 + 10, centerY, msgGen, 0.4, colorVal);
    
                        }
                    }
                    if(pHVCResult->executedFunc & HVC_ACTIV_GAZE_ESTIMATION){
                        /* Gaze */
                        if((-128 == pHVCResult->fdResult.fcResult[i].gazeResult.gazeLR) ||
                            (-128 == pHVCResult->fdResult.fcResult[i].gazeResult.gazeUD)){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Gaze\t\tEstimation not possible");
                        }
                        else{
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Gaze\t\tLR:%d UD:%d",
                                        pHVCResult->fdResult.fcResult[i].gazeResult.gazeLR, pHVCResult->fdResult.fcResult[i].gazeResult.gazeUD);
                        }
                    }
                    if(pHVCResult->executedFunc & HVC_ACTIV_BLINK_ESTIMATION){
                        /* Blink */
                        if((-128 == pHVCResult->fdResult.fcResult[i].blinkResult.ratioL) ||
                            (-128 == pHVCResult->fdResult.fcResult[i].blinkResult.ratioR)){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Blink\t\tEstimation not possible");
                        }
                        else{
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Blink\t\tLeft:%d Right:%d",
                                        pHVCResult->fdResult.fcResult[i].blinkResult.ratioL, pHVCResult->fdResult.fcResult[i].blinkResult.ratioR);
                        }
                    }
                    if(pHVCResult->executedFunc & HVC_ACTIV_EXPRESSION_ESTIMATION){
                        /* Expression */
                        if(-128 == pHVCResult->fdResult.fcResult[i].expressionResult.score[0]){
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Expression\tEstimation not possible");
                        }
                        else{
                            if(pHVCResult->fdResult.fcResult[i].expressionResult.topExpression > EX_SADNESS){
                                pHVCResult->fdResult.fcResult[i].expressionResult.topExpression = 0;
                            }
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\n      Expression\tExpression:%s Score:%d, %d, %d, %d, %d Degree:%d",
                                        pExStr[pHVCResult->fdResult.fcResult[i].expressionResult.topExpression],
                                        pHVCResult->fdResult.fcResult[i].expressionResult.score[0],
                                        pHVCResult->fdResult.fcResult[i].expressionResult.score[1],
                                        pHVCResult->fdResult.fcResult[i].expressionResult.score[2],
                                        pHVCResult->fdResult.fcResult[i].expressionResult.score[3],
                                        pHVCResult->fdResult.fcResult[i].expressionResult.score[4],
                                        pHVCResult->fdResult.fcResult[i].expressionResult.degree);
                            char msgExp[16];
                            sprintf(msgExp, "Exp:%s", pExStr[pHVCResult->fdResult.fcResult[i].expressionResult.topExpression]);
                            cvui::text(frame, centerX + centerW / 2 + 10, centerY + 18, msgExp, 0.4, colorVal);
                        }    
                    }
                }
            }
              
            if(count < 0)
            {
                count = 0;
                cvui::counter(frame, 227, 190, &count, 1, "%03d");
            }
            else
            {
                cvui::counter(frame, 227, 190, &count, 1, "%03d");                
            }

            // Render a regular button.
            if (cvui::button(frame, 226, 212, " Register ")) {
                std::cout << "Regular button clicked!" << std::endl;

                if(flgReg != 1)
                {
                    std::cout << "Face Result != 1" << std::endl;
                }else{
                    std::cout << "Reg Face!!!!!" << std::endl;
                    cv::waitKey(100);            
                    int userID = count;
                    int dataID;
                    int dataNo;
                
                    /*********************************/
                    /* Get Registration Info         */
                    /*********************************/
                    ret = HVC_GetUserData(UART_SETTING_TIMEOUT, userID, &dataNo, &status);
                    if ( ret != 0 ) {
                        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_GetUserData) Error : %d\n", ret);
                        //break;
                    }
                    if ( status != 0 ) {
                        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetUserData Error : 0x%02X\n", status);
                        //break;
                    }
                    sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_GetUserData : 0x%04x", dataNo);
    
                    dataID = 0;
                    for ( i=0x01; i<0x400; i<<=1 ) {
                        if ( (dataNo & i) == 0 ) break;
                        dataID++;
                    }
                    printf("%d, %d\n", userID, dataID);
                    
                    if ( dataID >= 10 ) {
                        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nMaximum registration number reached.");
                        // break;
                    }
                    else
                    {
                        /*********************************/
                        /* Execute Registration          */
                        /*********************************/
                        timeOutTime = UART_REGIST_EXECUTE_TIMEOUT;
                        ret = HVC_Registration(timeOutTime, userID, dataID, &(pHVCResult->image), &status);
                        if ( ret != 0 ) {
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVCApi(HVC_Registration) Error : %d\n", ret);
//                            break;
                        }
                        if ( status != 0 ) {
                            sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nHVC_Registration Error : 0x%02X\n", status);
//                            break;
                        }
                        sprintf_s(&pStr[strlen(pStr)], LOGBUFFERSIZE-strlen(pStr), "\nRegistration complete.");
                    }
                }
            }

            // This function must be called *AFTER* all UI components. It does
            // all the behind the scenes magic to handle mouse clicks, etc.
            cvui::update();
            cv::imshow(WINDOW_NAME, frame);
            cv::waitKey(10);

            /*
            if ( kbhit() ) {
                ch = getchar();
                ch = toupper( ch );
            }
            */

        } while( ch != ' ' );
    } while(0);

    /******************/
    /* Log Output     */
    /******************/
    PrintLog(pStr);

    /********************************/
    /* Free result area             */
    /********************************/
    if( pHVCResult != NULL ){
        free(pHVCResult);
    }

    com_close();

    /* Free Logging Buffer */
    if ( pStr != NULL ) {
        free(pStr);
    }
    return (0);
}

