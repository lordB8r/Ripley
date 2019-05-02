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
# [ (b,p) for b in range(6) for p in range(16) ]
key_map = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
    (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15),
    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
    (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14), (2, 15),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
    (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15),
    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
    (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15),
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
    (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15)
    ]


MIDI_OFFSET = 21

class playtime:

    version = 0.7

    keys=[] # 1 pin per key

    ## SPI things

    def spi_init(self):
        self.mcps = []
        for dev in range(6):

            mcp = MCP23S17(bus=0x00, pin_cs=0x00, device_id=dev)
            mcp.open()
            mcp._spi.max_speed_hz = 47000000

            for pin in range(16):
                mcp.setDirection(pin, mcp.DIR_OUTPUT)

            self.mcps.append(mcp)
            mcp=None


    def spi_send(self):
        # solenoids on/off
        for key_no, key_val in enumerate(self.keys):
            # This line breaks on JPs machine
            chip_no, pin_no = key_map[key_no]
            # This line works on JPs machine
            # pin_no = key_no
            if key_val:
                print(' ', end='')
                if self.args.spi:
                    # press/energized
                    print( "pin: {}  chip: {}".format(pin_no, chip_no))
                    self.mcps[chip_no].digitalWrite(pin_no, MCP23S17.LEVEL_HIGH)
            else:
                if self.args.spi:
                    # release
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
        event_note = event[3]-MIDI_OFFSET

        if self.args.verbose>=1:
            print("{} dtime: {}  channel: {}  note: {} velocity: {}".format(*event))

        if self.args.strict:
            assert 0 <= event_note < self.args.keys

        if event[0] == 'note_on':
            self.keys[event_note] = 1
        else:
            self.keys[event_note] = 0


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

        if self.args.demo == 1:
            # walk down all the keys
            while True:
                for i in range(len(self.keys)):
                    self.keys[i] = 1
                    self.spi_send()
                    self.keys[i] = 0
                    time.sleep(.3)

        if self.args.demo == 2:
            while True:
                for bank in range(4):
                    print("bank {}:".format(bank), end=' ')
                    for solenoid in range(22):
                        i = bank+solenoid*4
                        print(i, end=' ')
                        self.keys[i] = 1
                        self.spi_send()
                        self.keys[i] = 0
                        time.sleep(.3)
                    print()

    # program things

    def pars_args(self):

        parser = argparse.ArgumentParser()

        parser.add_argument("--filename",
                help='midi file to play')

        parser.add_argument("--demo", type=int,
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


