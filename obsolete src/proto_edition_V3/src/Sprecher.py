
class Sprecher():


    @staticmethod
    def get_speakerCoordinates():

        [leftSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[0]) 
        [middleSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[1])
        [rightSpeaker] = freefield.pick_speakers(Globals.SPEAKER_COORDINATES[2])

        return leftSpeaker, middleSpeaker, rightSpeaker


 
