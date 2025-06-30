import time

class CommonHelpFunctions:

    @staticmethod #works
    def waitForXSeconds(deltaT : int) -> None:
        stopTime = time.time() + deltaT
        while True:
            if( time.time() >= stopTime ):
                break