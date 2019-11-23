import gpiozero # uses BCM numbering by default
from time import sleep

pot = gpiozero.MCP3008(channel=0)

while True:
  print(pot.value)
  sleep(0.25)