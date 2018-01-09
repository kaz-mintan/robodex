#INCLUDE_DIRECTORIES(  /usr/include/python2.7 )
#ADD_LIBRARY(main SHARED main.cpp )
#TARGET_LINK_LIBRARIES(okao boost_python python2.7 )

if (NOT MSVC)
  add_compile_options(-std=c++11 -Wno-write-strings -Wno-implicit-function-declaration)
endif()

find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} , /usr/include/python3.5 )
link_directories(./)

cmake_minimum_required(VERSION 2.8)
#add_executable(Main
#	main.cpp
#	HVCApi.c
#	uart.c
#)
ADD_LIBRARY(okao SHARED main.cpp HVCApi.c uart.c)
target_link_libraries( okao ${OpenCV_LIBS} boost_python3 )
#target_link_libraries( Main ${OpenCV_LIBS} boost_python python2.7 )
