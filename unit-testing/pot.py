import gpiozero # uses BCM numbering by default

pot = gpiozero.MCP3008(channel=0)

while True:
  print(pot.value)