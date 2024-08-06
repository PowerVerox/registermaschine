from instruction import *
from machine import *

#prompt = "> "

#Machine().add_standard_instructions().run_code("""CLOAD 41
#IF != 42
#GO TO 5
#CLOAD 420
#END
#
#CLOAD 69
#END
#
#""").print()

Machine().add_standard_instructions().run_file('prog.ram').print()
