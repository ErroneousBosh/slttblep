// Copyright 2018 Erroneous Bosh <erroneousbosh@gmail.com>
//
// Usage of the works is permitted provided that this instrument is
// retained with the works, so that any entity that uses the works is
// notified of this instrument.
//
// DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.

// Sawtooth antialiased oscillator

#include "tables.h"

// global variables are bad
// but in embedded stuff with 2K of RAM we can't really go wrong

volatile unsigned char osc, oscp, frac, inp, dly; // oscillator blep
volatile unsigned long theta, phase;  // oscillator state and frequency offset

unsigned int adc; // current pot value
unsigned int ref = 31250; // theoretical sample rate, adjust to tune

void setup() {
  // configure timer for clock prescaler=1 PWM A on 11
  // and "phase correct" PWM
  TCCR2A &= 0x30;
  TCCR2A |= 0x81;
  TCCR2B &= 0xf0;
  TCCR2B |= 0x01;

  TIMSK0 &= 0xfe; // disable timer 0
  TIMSK2 |= 0x01; // enable timer 2 int
  
  // enable PWM pin
  DDRB |= 0x08;

  // enable aliasing gate pin
  DDRD &= 0xfb;
  PORTD |= 0x04;
}

void loop() {
  adc = 16 + analogRead(0)*4; // value from 16Hz to ~4100Hz
  theta = pow(2,32) * adc / ref;  // calculate phase shift per sample
}

ISR(TIMER2_OVF_vect) {
  // here's where the clever stuff happens
  // every 1/31250th of a second we calculate a new sample and output it to the PWM

  inp = dly;  // get the sample we saved from last time
  dly = 0;    // get ready to make a whole new sample

  phase += theta; // increment the phase accumulator
  osc = phase >> 24;  // upper 8 bits are our desired waveform

  if ((osc < oscp) && (PIND & 0x04)) {  // counter has wrapped, antialias enabled
    // "recip" is a lookup table containing the reciprocal of (1/x) scaled to 0-255
    frac = osc * pgm_read_byte_near(recip + (theta>>24)); // compute phase divided by phase step
    inp -= pgm_read_byte_near(blep+frac); // apply the bandlimited step correction to the current sample
    dly = pgm_read_byte_near(blep+(255-frac)); // and to the previous sample, which we'll output
    
  }

  dly += osc; // add the oscillator in, dly either has the blep correction or 0
  oscp = osc; // save the oscillator for next time so we can tell if it wraps

  OCR2A = inp;  // output the sample to PWM
}

