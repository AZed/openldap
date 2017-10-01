# $OpenLDAP: pkg/ldap/contrib/slapd-modules/addpartial/Makefile,v 1.1.2.3 2008/09/04 17:17:30 quanah Exp $
OPENLDAP_SRC=../../..
CPPFLAGS+=-I${OPENLDAP_SRC}/include -I${OPENLDAP_SRC}/servers/slapd
CC=gcc

all: addpartial-overlay.so

addpartial-overlay.so: addpartial-overlay.c
	$(CC) -shared $(CPPFLAGS) $(LDFLAGS) -Wall -o $@ $?

clean:
	rm addpartial-overlay.so
