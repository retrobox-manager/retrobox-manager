#!/usr/bin/python3
"""FrontEnd Factory"""


from libraries.constants.constants import FrontEnd
from libraries.frontend.abstract_frontend import AbstractFrontEnd
from libraries.frontend.batocera.batocera_front_end import BatoceraFrontEnd
from libraries.frontend.launchbox.launchbox_front_end import LaunchboxFrontEnd


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
