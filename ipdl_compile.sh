python compiler/ipdl.py \
	--sync-msg-list=compiler/sync-messages.ini \
	--msg-metadata=compiler/message-metadata.ini \
	--outheaders-dir=output/_ipdlheaders \
	--outcpp-dir=output/cpp \
	-I=ipdl/deps \
	ipdl/PPlugin.ipdl