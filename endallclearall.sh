#!/bin/bash

sudo kill -9 $(ps -x | grep python | grep -v grep | awk '{print $1}')
./clearall.sh

