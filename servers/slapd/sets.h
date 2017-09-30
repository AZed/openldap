/* $OpenLDAP: pkg/ldap/servers/slapd/sets.h,v 1.1.2.2 2002/01/04 20:38:31 kurt Exp $ */
/*
 * Copyright 2000-2002 The OpenLDAP Foundation, All Rights Reserved.
 * COPYING RESTRICTIONS APPLY, see COPYRIGHT file
 */

/* this routine needs to return the bervals instead of
 * plain strings, since syntax is not known.  It should
 * also return the syntax or some "comparison cookie"
 * that is used by set_filter.
 */
typedef char **(*SET_GATHER) (void *cookie, char *name, char *attr);

long set_size (char **set);
void set_dispose (char **set);

int set_filter (SET_GATHER gatherer, void *cookie, char *filter, char *user, char *this, char ***results);

