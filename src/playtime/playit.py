# playit.py
# reads a midi file, fires the solenoids

import argparse
import time

from pprint import pprint

import MIDI

try:
    from RPiMCP23S17.MCP23S17 import MCP23S17
except RuntimeError as e:
    pprint(e)
    print("MCP23S17 failed to import. I hope you are OK with this.")

# map keys to chips and pins
key_map = [
        (0,0),
        (1,0),
        (2,0),
        (4,0),
        (5,0),
        (6,0),
        (7,0),
        (8,0),
        (9,0),
        (10,0),
        (11,0),
        (12,0),
        (13,0),
        (14,0),
        (15,0),
        (0,1),
        ]

class playtime:

    version = 0.3

    keys=[] # 1 pin per key

    ## SPI things

    def spi_init(self):
        self.mcps = []
        for x in range(1):

            mcp = MCP23S17(bus=0x00, pin_cs=0x00, device_id=0)
            mcp.open()
            mcp._spi.max_speed_hz = 7000

            for x in range(16):
                mcp.setDirection(x, mcp.DIR_OUTPUT)

            self.mcps.append(mcp)
            mcp=None


    def spi_send(self):
        # solenoids on/off
        for key_no, key_val in enumerate(self.keys):
            pin_no,chip_no = key_map[key_no]
            if key_val:
                print(' ', end='')
                if self.args.spi:
                    # press
                    print( "pin: {}  chip: {}".format(pin_no, chip_no))
                    self.mcps[chip_no].digitalWrite(pin_no, MCP23S17.LEVEL_HIGH)
            else:
                if self.args.spi:
                    # releawse
                    self.mcps[chip_no].digitalWrite(pin_no, MCP23S17.LEVEL_LOW)
                print('*', end='')
        print()


    ## MIDI things

    def score_get(self):

        with open(self.args.filename, 'rb') as fh:
            midi = bytes(fh.read())
            self.opus = MIDI.midi2opus(midi)

    ## play things


    def note(self, event):
        # note on/off
        if self.args.verbose>=1:
            print("{} dtime: {}  channel: {}  note: {} velocity: {}".format(*event))

        if self.args.strict:
            assert 0 <= event[3] <= 87

        if event[0] == 'note_on':
            self.keys[event[3]] = 1
        else:
            self.keys[event[3]] = 0


    def play(self):
        self.ticks = self.opus[0]
        tracks = self.opus[1:]

        if self.args.strict:
            assert len(tracks) == 1

        for event in tracks[0]:
            if self.args.verbose>=2:
                pprint(event)

            if event[0] in ['note_on', 'note_off']:
                self.note(event)
                self.spi_send()
                # I have no idea if this is the right time to sleep
                time.sleep( self.ticks/1000 )


    def demo(self):
        # walk down all the keys
        while True:
            for i in range(len(self.keys)):
                self.keys[i] = 1
                self.spi_send()
                self.keys[i] = 0
                time.sleep(1)

    # program things

    def pars_args(self):

        parser = argparse.ArgumentParser()

        parser.add_argument("--filename",
                help='midi file to play')

        parser.add_argument("--demo", action="store_true",
                help='sequence all the pins')

        parser.add_argument("--strict", action="store_true",
                help='error on invalid data')

        parser.add_argument("--spi", action="store_true",
                help="Send SPI commands.")

        parser.add_argument("--keys", type=int, default=88,
                help="Number of keys in a piano.")

        parser.add_argument("-v", "--verbose", type=int,
                default=0, )
        parser.add_argument("--version", action="store_true" )
        # parser.add_argument("--debug", action="store_true" )

        args = parser.parse_args()
        self.args = args

        return

    def main(self):

        self.pars_args()

        if self.args.version:
            print(self.version)
            return

        self.keys = [0] * self.args.keys

        if self.args.spi:
            self.spi_init()

        if self.args.demo:
            self.demo()

        if self.args.filename:
            self.score_get()
            self.play()

if __name__ == "__main__":
    pt = playtime()
    pt.main()


