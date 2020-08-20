#include <stdio.h>
#include <stdint.h>
#include "Client_API.h"
#include "EnumTypes.h"
#include "UART_Connector.h"

int main()
{
	uint32_t idx;
	
	// Step 1: Initialize the Camera 
	// Port 24 corresponds to -- /dev/ttyACM0
	// Be sure to add permissions on that port to be bound
	// sudo chmod a+rwx /dev/ttyACM0
	FLR_RESULT result;
	result = Initialize(24, 921600); // /dev/ttyACM0, 921600 baud
	// printf("Initialize: ");
	if (result)
	{
		printf("Failed to initialize, exiting.\n");
		Close();
		return 1;
	}
	// printf("0x%08X\n", result);
	// printf("SUCCESS\n\n");
	
	float cpu_temp = 0;
        result = bosonGetMyriadTemp(&cpu_temp);
        if (result)
        {
                printf("Failed MyraidTemp with status 0x%08X, exiting.\n",result);
                Close();
                return 1;
        }
	
	int16_t fpa_temp = 0;
	float sensor_temp = 0;
	result = bosonlookupFPATempDegCx10(&fpa_temp);
	if (result)
        {
                printf("Failed FPATemp with status 0x%08X, exiting.\n",result);
                Close();
                return 1;
        }
	sensor_temp = fpa_temp / 10.0;
	printf("proc_temp\t%.2f\nsensor_temp\t%.2f\n", cpu_temp, sensor_temp);

	Close();
	return 0;	
}
