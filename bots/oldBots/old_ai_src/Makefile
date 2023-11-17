include config.mk

ROOT=..
LDFLAGS +=-lX11 -lm
CFLAGS += -fPIC
BIN=xpilot
PLATFORM=$(shell uname -i)

SRC=AI.c about.c blockbitmaps.c caudio.c checknames.c\
    client.c colors.c config.c configure.c datagram.c\
    dbuff.c debugaudio.c default.c error.c gfx2d.c gfx3d.c\
    guimap.c guiobjects.c join.c list.c math.c ncdaudio.c\
    net.c netclient.c paint.c paintdata.c painthud.c\
    paintmap.c paintobjects.c paintradar.c portability.c\
    query.c randommt.c record.c shipshape.c sim.c socklib.c\
    strcasecmp.c strdup.c strlcpy.c syslimit.c talk.c\
    talkmacros.c textinterface.c texture.c usleep.c welcome.c\
    widget.c xevent.c xeventhandlers.c xinit.c xpilot.c\
    xpilot_ai.c xpmemory.c xpmread.c

OBJ=${SRC:.c=.o}

all: options xpilot lib

options:
	@echo Xpilot-AI build options:
	@echo "CFLAGS 	= ${CFLAGS}"
	@echo "LDFLAGS	= ${LDFLAGS}"
	@echo "CC	= ${CC}"
	@echo "AR	= ${AR}"

${OBJ}: config.mk

.c.o:
	@echo CC $<
	@${CC} -c ${CFLAGS} $<

${BIN}: ${OBJ} main.o
	@echo CC -o $@
	@${CC} ${LDFLAGS} -o $@ ${OBJ} main.o

lib: ${OBJ}
	@echo Static library: libxpilot_ai.a
	@${AR} rcs libxpilot_ai.a ${OBJ}
	@echo Shared library: libxpilot_ai.so
	@${CC} ${LDFLAGS} -shared -o libxpilot_ai.so ${OBJ}

install: xpilot libxpilot_ai.so libxpilot_ai.a
	@echo installing executable to ${DESTDIR}${PREFIX}/bin
	@mkdir -p ${DESTIR}${PREFIX}/bin
	@cp -f ${BIN} ${DESTDIR}${PREFIX}/bin
	@chmod 755 ${DESTDIR}${PREFIX}/bin
	@echo installing libraries to ${DESTDIR}${PREFIX}/lib
	@mkdir -p ${DESTDIR}${PREFIX}/lib
	@cp -f libxpilot_ai.so libxpilot_ai.a ${DESTDIR}${PREFIX}/lib
	@echo installing header file to ${DESTDIR}${PREFIX}/include
	@cp -f xpilot_ai.h ${DESTDIR}${PREFIX}/include

uninstall:
	@echo Removing executable, library, and header files
	rm -f ${DESTIR}${PREFIX}/bin/${BIN}
	rm -f ${DESTDIR}${PREFIX}/lib/libxpilot_ai.so
	rm -f ${DESTDIR}${PREFIX}/lib/libxpilot_ai.a
	rm -f ${DESTDIR}${PREFIX}/include/xpilot_ai.h

tarball: clean
	@echo Building source tarball version ${VERSION}
	@rm -f ${ROOT}/xpilot-ai-*-src.tar.gz 
	@rm -rf ${ROOT}/xpilot-ai-${VERSION}
	@mkdir -p ${ROOT}/xpilot-ai-${VERSION}
	@cd ${ROOT}; cp -r src doc examples textures maps \
	INSTALL LICENSE README AUTHORS COPYING xpilot-ai-${VERSION}
	@cd ${ROOT}; tar czf xpilot-ai-${VERSION}-src.tar.gz \
	xpilot-ai-${VERSION}
	@rm -rf ${ROOT}/xpilot-ai-${VERSION}

binary: lib ${BIN} cleanobj
	@echo Building binary tarball version ${VERSION}-${PLATFORM}
	@rm -f 	${ROOT}/xpilot-ai-*-${PLATFORM}.tar.gz
	@rm -rf ${ROOT}/xpilot-ai-${VERSION}
	@mkdir -p ${ROOT}/xpilot-ai-${VERSION}
	@cd ${ROOT}; cp -r src doc examples textures maps \
	INSTALL LICENSE README AUTHORS COPYING xpilot-ai-${VERSION}/
	@cd ${ROOT}; tar czf xpilot-ai-${VERSION}-${PLATFORM}.tar.gz \
	xpilot-ai-${VERSION}
	@rm -rf ${ROOT}/xpilot-ai-${VERSION}

cleanobj:
	@echo Cleaning object files
	@rm -f *~
	@rm -f ${OBJ} main.o\

clean: cleanobj
	@echo Cleaning binaries
	@rm -f xpilot libxpilot_ai.* \
