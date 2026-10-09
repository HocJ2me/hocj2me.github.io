/* Các hook bắt buộc khác của bản mô phỏng. */
#include <stdio.h>
#include <stdlib.h>
#include "FreeRTOS.h"
#include "task.h"

void vApplicationMallocFailedHook( void )
{
    printf( "!! Hết bộ nhớ heap (malloc failed)\n" );
    fflush( stdout );
    exit( 1 );
}

void vAssertCalled( const char * file, unsigned long line )
{
    printf( "!! configASSERT thất bại tại %s:%lu\n", file, line );
    fflush( stdout );
    exit( 2 );
}
