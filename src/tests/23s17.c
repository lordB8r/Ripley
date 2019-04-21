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
    //writeByte(0, 0, 0x14, 2^i);
    //delay(1000);
    digitalWrite (BASE + i, 1);
    delay(100);
    digitalWrite (BASE + i, 0);
    delay(100);
  }
    delay(2000);
  }
  //pinMode         (BASE + 15, INPUT) ;
  //pullUpDnControl (BASE + 15, PUD_UP) ;
/*
  for (;;)
  {
    for (i = 0 ; i < 1024 ; ++i)
    {
      for (bit = 0 ; bit < 10 ; ++bit)
        digitalWrite (BASE + bit, i & (1 << bit)) ;
      delay (5) ;
      while (digitalRead (BASE + 15) == 0)
        delay (1) ;
    }
  }*/
  return 0 ;
}
