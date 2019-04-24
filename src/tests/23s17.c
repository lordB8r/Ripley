/*
 * 23s17.c:
 *      WiringPi test with an MCP23S17 SPI GPIO expander chip
 *
 * Copyright (c) 2012-2013 Gordon Henderson. <projects@drogon.net>
 ***********************************************************************
 */

#include <stdio.h>
#include <wiringPi.h>
#include <mcp23s17.h>
#include <mcp23x0817.h>

#define BASE    123

int main (void)
{
  int i, bit ;

  wiringPiSetup () ;
  mcp23s17Setup (BASE, 0, 0) ;

  printf ("Raspberry Pi - MCP23S17 Test\n") ;

  for (i = 0 ; i < 15 ; ++i)
    pinMode (BASE + i, OUTPUT) ;
  i=1;
  for (;;) {
  for (i = 0 ; i < 15 ; ++i)
  {
    digitalWrite (BASE + i, 1);
    delay(100);
    digitalWrite (BASE + i, 0);
    delay(100);
  }
    delay(2000);
  }
  return 0 ;
}
