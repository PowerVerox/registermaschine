from instruction import *
from machine import *

#prompt = "> "

Machine().add_standard_instructions().print().run_code("""LOAD 41
IF != 42
GO TO 5
LOAD 420
END

LOAD 69
END

""").print()
