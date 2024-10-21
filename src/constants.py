# registermaschine - A simple register machine simulator
# Copyright (C) 2024  Tim Ernst, Vincent A. Hey

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


class Constants:
    # Variablen, die konstant bleiben sollen, zur Vermeidung von Magic Numbers
    REGISTER_COUNT = 8 # 1 Byte je Register, 8 Register insgesamt
    REGISTER_LIMIT = 256 # 0-255
