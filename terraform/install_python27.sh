#!/bin/sh
env ASSUME_ALWAYS_YES=YES /usr/sbin/pkg bootstrap
/usr/sbin/pkg install -y python27
