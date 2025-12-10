#!/usr/bin/python3
"""FrontEnd Factory"""


from libraries.constants.constants import FrontEnd
from frontend.abstract_frontend import AbstractFrontEnd
from frontend.batocera.batocera_front_end import BatoceraFrontEnd
from frontend.launchbox.launchbox_front_end import LaunchboxFrontEnd


class FrontEndFactory:
    """FrontEnd Factory"""

    @staticmethod
    def create(front_end: FrontEnd) -> AbstractFrontEnd:
        """Create front end"""

        match(front_end):
            case FrontEnd.BATOCERA:
                return BatoceraFrontEnd()
            case FrontEnd.LAUNCHBOX:
                return LaunchboxFrontEnd()
            case _:
                raise Exception('Unimplemented FrontEnd!')
