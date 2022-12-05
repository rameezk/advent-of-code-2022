SUBDIRS = $(shell ls -d day*/)

run-all:
	for dir in $(SUBDIRS) ; do make -C $$dir run ; done

test-all:
	for dir in $(SUBDIRS) ; do make -C $$dir test ; done

