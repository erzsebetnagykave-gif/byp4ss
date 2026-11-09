CXX = clang++
CXXFLAGS = -O2 -Wall -std=c++17 -fPIC
LDFLAGS = -shared
TARGET = libnetlink.so
SRC = NetlinkReader.cpp

all: $(TARGET)

$(TARGET): $(SRC) NetlinkReader.hpp
$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $(TARGET) $(SRC)

clean:
rm -f $(TARGET)

.PHONY: all clean
