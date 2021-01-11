# ***************************************************************
# Written by Zach Rinehart
# Final version of the Storage Tester Program
# Last modified June 29, 2020
# ***************************************************************

# include necessary libraries
import os                   # file os ops
import shutil               # file transfers
import time                 # clock ops to measure transfer speed
import random               # for creation of files with random contents
import string               # ???
import sys                  # for sys.exit
import csv                  # to record the data

# random string program (from GeeksForGeeks.org)
def randomString(stringLength):

    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(stringLength))


# test file creation program
def createTestFile(testfname, filetype, filesize):

    # setup
    testfile = open(testfname, "w+")                    # create text file
    bytesize = filesize * 1048576                       # get byte size of specified file size


    # write file with semi-random data
    if(filetype == "random"):
        stringz = [randomString(10)]                        # list to hold random strings

        # create the strings
        for x in range(10):
            stringz.append(randomString(100))

        reps = int(bytesize / 100)                          # calculate number of write times for random strings

        print("Creating file. Please wait... ")             # let user know it's working
        print()                                             # extra spacing

        # write the file contents
        for x in range(reps):
            testfile.write(stringz[random.randrange(0, 9)])


    # write file with string pattern data
    elif filetype == "specified":
        datastring = str(input("Enter string pattern to test: "))   # prompt for string pattern
        wordsize = datastring.__sizeof__() - 49                     # corrected size of string pattern

        # error detection for string pattern
        if wordsize <= 0:
            sys.exit("ZDR: (1) Invalid selection")

        print("Creating file. Please wait... ")         # let user know it's working
        print()                                         # extra spacing

        datastring *= 10                                # an efficiency string with ten iterations of datastring

        reps = bytesize / wordsize                      # bytes of file / bytes of input pattern
        reps /= 10                                      # less work for the computer
        reps = int(reps)                                # convert reps to int for loop

        # write to the file
        for j in range(reps):
            testfile.write(datastring)

    # if not chosen 'specified' or 'random'
    else:
        sys.exit("ZDR: (2) Invalid selection")

    testfile.close()

    return testfile


# get the source test file
def getSource():

    # necessary global
    global testfile

    # get user source selection
    source = str(input("Create new test file (c) or use existing file (e)? (default e) "))

    # convert to lowercase
    source = source.lower()

    # repeat asking until valid input is received
    while source != 'c' and source != 'e' and source != 'q' and source != "":
        source = str(input("Invalid choice. Try again (press 'q' to quit): "))
        source = source.lower()

    # if user chooses existing file:
    if source == 'e' or source == "":
        # get name of test file
        testfname = str(input("What's the name of the test file? "))

        # default op
        if testfname == "":
            testfname = "tester.txt"

        # Try again while there's not a proper file input
        while not os.path.exists(testfname):
            testfname = input("Error: Not a file. Try again: ")

        # open and return test file
        testfile = open(testfname, "a")
        return testfile


    # if user chooses to create new file:
    elif source == 'c':
        # repeat decision
        repeat = "y"
        while repeat == "y":
            # get test file name
            testfname = str(input("Name the file (& end with .txt): "))

            # default (random) name
            if testfname == "":
                testfname = ("tester.txt")

            # remove any preexisting test file with this name
            testfile = open(testfname, "w+")
            testfpath = os.path.join(os.getcwd(), testfile.name)
            testfile.close()
            os.remove(testfpath)

            # create new test file
            filetype = str(input("Random file (r) or specified file (s)? (default r) "))
            filetype = filetype.lower()
            while filetype != 'r' and filetype != 's' and filetype != "":
                filetype = str(input("Invalid selection. Try again: "))
                filetype = filetype.lower()

            # convert to valid parameters
            if filetype == 'r' or filetype == "":
                filetype = "random"
            elif filetype == 's':
                filetype = "specified"

            # get specified file size
            filesize = str(input("Enter desired test file size in MB (default 500): "))
            while not filesize.isdigit() and filesize != "":
                filesize = str(input("Invalid selection. Enter an actual number: "))

            # default value
            if filesize == "":
                filesize = 500

            # make the actual test file
            testfile = createTestFile(testfname, filetype, int(filesize))
            print("This test file can be used in future program runs.")

            # repeat again?
            repeat = str(input("Create another test file? (y/n): "))
            repeat = repeat.lower()

        return testfile

    # if user wants to quit the program:
    elif source == "q":
        # quit the program
        sys.exit("Program terminated successfully")


# The overall test
def storageTest():

    # separator string for console readability
    sephash = "################################################"

    # configure csv output log
    outputlog = open("OutputLog.csv", "w+")
    logwriter = csv.writer(outputlog)

    # initial separator
    print(sephash)

    # initial message
    print("Use no test file that exceeds RAM capacity.")
    time.sleep(2)

    # get test file
    testfile = getSource()

    # get storage destination
    destination = str(input("Where should the file write to? "))

    # error handling
    while not os.path.isdir(destination):
        destination = input("Error: Not a path to directory. Try again: ")

    # get number of loop times
    numloop = input("How many times for read/write tests? (default 5) ")

    # error handling
    while not numloop.isdigit() and numloop != "":
        numloop = input("Error: Not a number. Enter a real number: ")

    # default value
    if numloop == "":
        numloop = "5"

    # convert to int
    numloop = int(numloop)

    # initialize statistics arrays with dummy value
    writestats = ["Dummy"]
    readstats = ["Dummy"]

    # define globals
    global start            # start time
    global end              # end time
    global resultpath       # file path to result

    # read from /dev/[zero | random | urandom]
    if testfile.name == "/dev/zero" or testfile.name == "/dev/random" or testfile.name == "/dev/urandom":
        # get test file size from user
        insizestr = str(input("How many megabytes? (default 500) "))

        while not insizestr.isdigit() and insizestr != "":
            insizestr = input("Error: Not a number. Enter a real number: ")

        # separator
        print(sephash)

        # default value
        if insizestr == "":
            insizestr = "500"

        # calculate test file size
        insize = int(insizestr)
        insize *= (1024 * 1024)

        # configure output file path
        resultpath = os.path.join(destination, "output.txt")

        for i in range(numloop):
            # clear cache
            os.system('sudo -S sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"')

            # configure output file
            output = open(resultpath, "wb+")

            # open testfile in read mode
            testfile.close()
            testfile = open(testfile.name, "rb")

            # the actual write test and clock
            start = time.time()
            output.write(testfile.read(insize))
            os.system("sync")
            end = time.time()

            # calculations
            totalTime = end - start  # net time
            fileSize = os.stat(resultpath).st_size  # file size in bytes
            fileSize /= (1024 * 1024)  # file size in megabytes
            mps = fileSize / totalTime
            writestats.append(mps)

            # close output file
            output.close()

            # print current stats
            print("Write cycle " + str(i) + ": " + str(mps) + " MB/s")

        # remove dummy item in array
        writestats.remove("Dummy")

    # if standard file test:
    else:
        # separator
        print(sephash)

        # transfer test file to RAM
        print("Hold on while we write to RAM...")
        shutil.copy(testfile.name, "/dev/shm")
        ramtemp = os.path.join("/dev/shm", testfile.name)

        # configure output file path
        resultpath = os.path.join(destination, testfile.name)

        for i in range(numloop):
            # file transfer and clock
            os.system('sudo -S sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"')  # clear cache
            start = time.time()                                     # start time
            shutil.copy(ramtemp, destination)                       # file transfer
            os.system("sync")                                       # sync file transfer with cache just in case
            end = time.time()                                       # end time

            # calculations
            totalTime = end - start                 # net time
            fileSize = os.stat(resultpath).st_size  # file size in bytes
            fileSize /= (1024 * 1024)               # file size in megabytes
            mps = fileSize / totalTime              # megabytes per second

            # add data to array
            writestats.append(mps)

            # print current stats
            print("Write cycle " + str(i) + ": " + str(mps) + " MB/s")

        # remove dummy item in array
        writestats.remove("Dummy")

        # cleanup ram
        os.remove(ramtemp)

        # separator
        print(sephash)

    # transferred file size
    megabytesize = os.stat(resultpath).st_size / (1024 * 1024)

    # read test:
    for i in range(numloop):
        # open files for read test
        newtf = open(resultpath, "rb", buffering=0)     # open text file in tested storage location
        nullfile = open(os.devnull, "wb", buffering=0)  # setup /dev/null for write destination

        # clear cache
        os.system('sudo -S sh -c "sync && echo 3 > /proc/sys/vm/drop_caches"')      # clear cache

        # execution
        start = time.time()                 # start time
        nullfile.write(newtf.read())        # read test file contents to /dev/null
        os.system("sync")                   # sync cache with system
        end = time.time()                   # end time

        # calculations
        totaltime = end - start             # net time
        mps = megabytesize / totaltime      # megabytes per second

        # print current stats
        print("Read cycle " + str(i) + ": " + str(mps) + " MB/s")

        # add read speed to array
        readstats.append(mps)

        # close files
        newtf.close()
        nullfile.close()

    # remove dummy item in array
    readstats.remove("Dummy")

    # initial average speed values
    avgwspeed = 0
    avgrspeed = 0

    # iterate arrays and log data
    for i in range(numloop):
        avgwspeed += writestats[i]
        avgrspeed += readstats[i]
        logwriter.writerow([writestats[i], readstats[i]])

    # calculate average
    avgwspeed /= len(writestats)
    avgrspeed /= len(readstats)

    # print data
    print(sephash)
    print("Number of tests completed: " + str(numloop))
    print("Transferred file size: " + str(megabytesize) + " MB")
    print("Average write speed: " + str(avgwspeed) + " MB/s")
    print("Average read speed: " + str(avgrspeed) + " MB/s")
    print(sephash)

    # close files
    testfile.close()
    outputlog.close()

    # delete test file from eMMC
    os.remove(resultpath)


# Main program
def main():
    storageTest()

if __name__ == "__main__":
    main()