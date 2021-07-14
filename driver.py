import datetime

import PARAMETER
import preprocess

import spimi

if __name__ == '__main__':
    start = datetime.datetime.now()
    print("Start Time of spimi invert: ", start)
    print("\n==================== Start preprocessing ====================")
    preprocess.read_file(PARAMETER.JSON_FILE)

    print("\n==================== Start spimi invert ====================")
    spimi.start_spimi(PARAMETER.BOLCK_PATH, PARAMETER.MERGED_BOLCK_PATH)
    finish = datetime.datetime.now()
    print("\nFinish Time of spimi invert: ", finish)
    print("SPIMI invert takes: ", str(finish - start))
