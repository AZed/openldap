/* $OpenLDAP: pkg/ldap/tests/progs/slapd-modrdn.c,v 1.7.2.8 2006/01/03 22:16:28 kurt Exp $ */
/* This work is part of OpenLDAP Software <http://www.openldap.org/>.
 *
 * Copyright 1999-2007 The OpenLDAP Foundation.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted only as authorized by the OpenLDAP
 * Public License.
 *
 * A copy of this license is available in file LICENSE in the
 * top-level directory of the distribution or, alternatively, at
 * <http://www.OpenLDAP.org/license.html>.
 */
/* ACKNOWLEDGEMENTS:
 * This work was initially developed by Howard Chu, based in part
 * on other OpenLDAP test tools, for inclusion in OpenLDAP Software.
 */

#include "portable.h"

#include <stdio.h>

#include <ac/stdlib.h>

#include <ac/ctype.h>
#include <ac/param.h>
#include <ac/socket.h>
#include <ac/string.h>
#include <ac/unistd.h>
#include <ac/wait.h>

#define LDAP_DEPRECATED 1
#include <ldap.h>
#include <lutil.h>

#define LOOPS	100
#define RETRIES	0

static void
do_modrdn( char *uri, char *host, int port, char *manager, char *passwd,
		char *entry, int maxloop, int maxretries, int delay,
		int friendly );

static void
usage( char *name )
{
        fprintf( stderr,
		"usage: %s "
		"-H <uri> | ([-h <host>] -p <port>) "
		"-D <manager> "
		"-w <passwd> "
		"-e <entry> "
		"[-l <loops>] "
		"[-r <maxretries>] "
		"[-t <delay>] "
		"[-F]\n",
			name );
	exit( EXIT_FAILURE );
}

int
main( int argc, char **argv )
{
	int		i;
	char		*uri = NULL;
	char		*host = "localhost";
	int		port = -1;
	char		*manager = NULL;
	char		*passwd = NULL;
	char		*entry = NULL;
	int		loops = LOOPS;
	int		retries = RETRIES;
	int		delay = 0;
	int		friendly = 0;

	while ( (i = getopt( argc, argv, "FH:h:p:D:w:e:l:r:t:" )) != EOF ) {
		switch( i ) {
		case 'F':
			friendly++;
			break;

		case 'H':		/* the server uri */
			uri = strdup( optarg );
			break;

		case 'h':		/* the servers host */
			host = strdup( optarg );
			break;

		case 'p':		/* the servers port */
			if ( lutil_atoi( &port, optarg ) != 0 ) {
				usage( argv[0] );
			}
			break;

		case 'D':		/* the servers manager */
			manager = strdup( optarg );
			break;

		case 'w':		/* the server managers password */
			passwd = strdup( optarg );
			break;

		case 'e':		/* entry to rename */
			entry = strdup( optarg );
			break;

		case 'l':		/* the number of loops */
			if ( lutil_atoi( &loops, optarg ) != 0 ) {
				usage( argv[0] );
			}
			break;

		case 'r':		/* the number of retries */
			if ( lutil_atoi( &retries, optarg ) != 0 ) {
				usage( argv[0] );
			}
			break;

		case 't':		/* delay in seconds */
			if ( lutil_atoi( &delay, optarg ) != 0 ) {
				usage( argv[0] );
			}
			break;

		default:
			usage( argv[0] );
			break;
		}
	}

	if (( entry == NULL ) || ( port == -1 && uri == NULL ))
		usage( argv[0] );

	if ( *entry == '\0' ) {

		fprintf( stderr, "%s: invalid EMPTY entry DN.\n",
				argv[0] );
		exit( EXIT_FAILURE );

	}

	do_modrdn( uri, host, port, manager, passwd, entry,
			loops, retries, delay, friendly );
	exit( EXIT_SUCCESS );
}


static void
do_modrdn( char *uri, char *host, int port, char *manager,
	char *passwd, char *entry, int maxloop, int maxretries, int delay,
	int friendly )
{
	LDAP	*ld = NULL;
	int  	i = 0, do_retry = maxretries;
	pid_t	pid;
	char *DNs[2];
	char *rdns[2];
	int         rc = LDAP_SUCCESS;


	pid = getpid();
	DNs[0] = entry;
	DNs[1] = strdup( entry );

	/* reverse the RDN, make new DN */
	{
		char *p1, *p2;

		p1 = strchr( entry, '=' ) + 1;
		p2 = strchr( p1, ',' );

		*p2 = '\0';
		rdns[1] = strdup( entry );
		*p2-- = ',';

		for (i = p1 - entry;p2 >= p1;)
			DNs[1][i++] = *p2--;
		
		DNs[1][i] = '\0';
		rdns[0] = strdup( DNs[1] );
		DNs[1][i] = ',';
	}

retry:;
	if ( uri ) {
		ldap_initialize( &ld, uri );
	} else {
		ld = ldap_init( host, port );
	}
	if ( ld == NULL ) {
		perror( "ldap_init" );
		exit( EXIT_FAILURE );
	}

	{
		int version = LDAP_VERSION3;
		(void) ldap_set_option( ld, LDAP_OPT_PROTOCOL_VERSION,
			&version ); 
	}

	if ( do_retry == maxretries ) {
		fprintf( stderr, "PID=%ld - Modrdn(%d): entry=\"%s\".\n",
			(long) pid, maxloop, entry );
	}

	rc = ldap_bind_s( ld, manager, passwd, LDAP_AUTH_SIMPLE );
	if ( rc != LDAP_SUCCESS ) {
		ldap_perror( ld, "ldap_bind" );
		switch ( rc ) {
		case LDAP_BUSY:
		case LDAP_UNAVAILABLE:
			if ( do_retry > 0 ) {
				do_retry--;
				if ( delay > 0) {
				    sleep( delay );
				}
				goto retry;
			}
		/* fallthru */
		default:
			break;
		}
		exit( EXIT_FAILURE );
	}

	for ( ; i < maxloop; i++ ) {
		rc = ldap_modrdn2_s( ld, DNs[0], rdns[0], 0 );
		if ( rc != LDAP_SUCCESS ) {
			ldap_perror( ld, "ldap_modrdn" );
			switch ( rc ) {
			case LDAP_NO_SUCH_OBJECT:
				/* NOTE: this likely means
				 * the second modrdn failed
				 * during the previous round... */
				if ( !friendly ) {
					goto done;
				}
				break;

			case LDAP_BUSY:
			case LDAP_UNAVAILABLE:
				if ( do_retry > 0 ) {
					do_retry--;
					goto retry;
				}
				/* fall thru */

			default:
				goto done;
			}
		}
		rc = ldap_modrdn2_s( ld, DNs[1], rdns[1], 1 );
		if ( rc != LDAP_SUCCESS ) {
			ldap_perror( ld, "ldap_modrdn" );
			switch ( rc ) {
			case LDAP_NO_SUCH_OBJECT:
				/* NOTE: this likely means
				 * the first modrdn failed
				 * during the previous round... */
				if ( !friendly ) {
					goto done;
				}
				break;

			case LDAP_BUSY:
			case LDAP_UNAVAILABLE:
				if ( do_retry > 0 ) {
					do_retry--;
					goto retry;
				}
				/* fall thru */

			default:
				goto done;
			}
		}
	}

done:;
	fprintf( stderr, " PID=%ld - Modrdn done (%d).\n", (long) pid, rc );

	ldap_unbind( ld );
}


