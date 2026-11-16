/*
 * breakbricks.h
 *
 *  Created on: Feb 12, 2024
 *      Author: Nirgal
 */

#ifndef RAMIO_H_
#define RAMIO_H_

#include <stdint.h>
#include "stm32g4_utils.h"
#include "stm32g4xx_hal.h"



#define SCREEN_HEIGHT	15
#define START_CO_X		152
#define START_CO_Y		112

typedef struct{
	uint8_t cell_x;
	uint8_t cell_y;
	uint8_t sub_x;
	uint8_t sub_y;
	float vel_x;
	float vel_y;
	bool grounded;
}player_t;

void RAMIO_init(void);

void RAMIO_process_main(void);


#endif /* TETRIS_H_ */
