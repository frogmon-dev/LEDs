#!/bin/bash

sudo teamviewer passwd altpajswl

sudo teamviewer daemon restart

teamviewer info | grep "TeamViewer ID" > teamviewerID.txt

sudo reboot
