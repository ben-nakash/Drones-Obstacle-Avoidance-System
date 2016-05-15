import sys

leftSensorData = middleSensorData = rightSensorData = new_file = None
line = ""
num_of_lines = 0
try:
    leftSensorData = open('Sensors Data\\leftSensorData.txt', 'r')
    middleSensorData = open('Sensors Data\\middleSensorData.txt', 'r')
    rightSensorData = open('Sensors Data\\rightSensorData.txt', 'r')
    new_file = open('Sensors Data\\SensorData.txt', 'w')

    for num_of_lines, l in enumerate(leftSensorData):
        pass
    leftSensorData.seek(0)

    # for line in leftSensorData:
    for row in range(num_of_lines):
        # line = ""
        # line += leftSensorData.readline().strip() + " "
        # line += middleSensorData.readline().strip() + " "
        # line += rightSensorData.readline() + " "
        # new_file.write(line)
        # print(line)
        line = leftSensorData.readline()
        new_file.write(line)
        line = middleSensorData.readline()
        new_file.write(line)
        line = rightSensorData.readline()
        new_file.write(line)

    leftSensorData.close()
    middleSensorData.close()
    rightSensorData.close()
    new_file.close()

except:
    print("Unexpected error:", sys.exc_info()[0])
    leftSensorData.close()
    middleSensorData.close()
    rightSensorData.close()
    new_file.close()
