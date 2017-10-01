/* ldapmodrdn.c - generic program to modify an entry's RDN using LDAP */
/* $OpenLDAP: pkg/ldap/clients/tools/ldapmodrdn.c,v 1.106.2.5 2006/01/03 22:16:01 kurt Exp $ */
/* This work is part of OpenLDAP Software <http://www.openldap.org/>.
 *
 * Copyright 1998-2007 The OpenLDAP Foundation.
 * Portions Copyright 1998-2003 Kurt D. Zeilenga.
 * Portions Copyright 1998-2001 Net Boolean Incorporated.
 * Portions Copyright 2001-2003 IBM Corporation.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted only as authorized by the OpenLDAP
 * Public License.
 *
 * A copy of this license is available in the file LICENSE in the
 * top-level directory of the distribution or, alternatively, at
 * <http://www.OpenLDAP.org/license.html>.
 */
/* Portions Copyright 1999, Juan C. Gomez, All rights reserved.
 * This software is not subject to any license of Silicon Graphics 
 * Inc. or Purdue University.
 *
 * Redistribution and use in source and binary forms are permitted
 * without restriction or fee of any kind as long as this notice
 * is preserved.
 */
/* Portions Copyright (c) 1992-1996 Regents of the University of Michigan.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms are permitted
 * provided that this notice is preserved and that due credit is given
 * to the University of Michigan at Ann Arbor.  The name of the
 * University may not be used to endorse or promote products derived
 * from this software without specific prior written permission.  This
 * software is provided ``as is'' without express or implied warranty.
 */
/* ACKNOWLEDGEMENTS:
 * This work was originally developed by the University of Michigan
 * (as part of U-MICH LDAP).  Additional significant contributors
 * include:
 *    Kurt D. Zeilenga
 *    Juan C Gomez
 */


#include "portable.h"

#include <stdio.h>

#include <ac/stdlib.h>

#include <ac/ctype.h>
#include <ac/string.h>
#include <ac/unistd.h>
#include <ac/time.h>

#include <ldap.h>
#include "lutil.h"
#include "lutil_ldap.h"
#include "ldap_defaults.h"

#include "common.h"


static char	*newSuperior = NULL;
static int   remove_old_RDN = 0;


static int domodrdn(
    LDAP	*ld,
    char	*dn,
    char	*rdn,
    char	*newSuperior,
    int		remove );	/* flag: remove old RDN */

void
usage( void )
{
	fprintf( stderr, _("Rename LDAP entries\n\n"));
	fprintf( stderr, _("usage: %s [options] [dn rdn]\n"), prog);
	fprintf( stderr, _("	dn rdn: If given, rdn will replace the RDN of the entry specified by DN\n"));
	fprintf( stderr, _("		If not given, the list of modifications is read from stdin or\n"));
	fprintf( stderr, _("		from the file specified by \"-f file\" (see man page).\n"));
	fprintf( stderr, _("Rename options:\n"));
	fprintf( stderr, _("  -r         remove old RDN\n"));
	fprintf( stderr, _("  -s newsup  new superior entry\n"));
	tool_common_usage();
	exit( EXIT_FAILURE );
}


const char options[] = "rs:"
	"cd:D:e:f:h:H:IkKMnO:p:P:QR:U:vVw:WxX:y:Y:Z";

int
handle_private_option( int i )
{
	switch ( i ) {
#if 0
		int crit;
		char *control, *cvalue;
	case 'E': /* modrdn extensions */
		if( protocol == LDAP_VERSION2 ) {
			fprintf( stderr, _("%s: -E incompatible with LDAPv%d\n"),
				prog, version );
			exit( EXIT_FAILURE );
		}

		/* should be extended to support comma separated list of
		 *	[!]key[=value] parameters, e.g.  -E !foo,bar=567
		 */

		crit = 0;
		cvalue = NULL;
		if( optarg[0] == '!' ) {
			crit = 1;
			optarg++;
		}

		control = strdup( optarg );
		if ( (cvalue = strchr( control, '=' )) != NULL ) {
			*cvalue++ = '\0';
		}
		fprintf( stderr, _("Invalid modrdn extension name: %s\n"), control );
		usage();
#endif

	case 'r':	/* remove old RDN */
	    remove_old_RDN++;
	    break;

	case 's':	/* newSuperior */
		if( protocol == LDAP_VERSION2 ) {
			fprintf( stderr, _("%s: -X incompatible with LDAPv%d\n"),
				prog, protocol );
			exit( EXIT_FAILURE );
		}
	    newSuperior = strdup( optarg );
	    protocol = LDAP_VERSION3;
	    break;

	default:
		return 0;
	}
	return 1;
}


int
main(int argc, char **argv)
{
    char		*entrydn = NULL, *rdn = NULL, buf[ 4096 ];
    FILE		*fp;
    LDAP		*ld;
	int		rc, retval, havedn;

    tool_init();
    prog = lutil_progname( "ldapmodrdn", argc, argv );

	tool_args( argc, argv );

    havedn = 0;
    if (argc - optind == 2) {
	if (( rdn = strdup( argv[argc - 1] )) == NULL ) {
	    perror( "strdup" );
	    return( EXIT_FAILURE );
	}
        if (( entrydn = strdup( argv[argc - 2] )) == NULL ) {
	    perror( "strdup" );
	    return( EXIT_FAILURE );
        }
	++havedn;
    } else if ( argc - optind != 0 ) {
	fprintf( stderr, _("%s: invalid number of arguments (%d), only two allowed\n"), prog, argc-optind );
	usage();
    }

    if ( infile != NULL ) {
	if (( fp = fopen( infile, "r" )) == NULL ) {
	    perror( infile );
	    return( EXIT_FAILURE );
	}
    } else {
	fp = stdin;
    }

	ld = tool_conn_setup( 0, 0 );

	if ( pw_file || want_bindpw ) {
		if ( pw_file ) {
			rc = lutil_get_filed_password( pw_file, &passwd );
			if( rc ) return EXIT_FAILURE;
		} else {
			passwd.bv_val = getpassphrase( _("Enter LDAP Password: ") );
			passwd.bv_len = passwd.bv_val ? strlen( passwd.bv_val ) : 0;
		}
	}

	tool_bind( ld );

	if ( assertion || authzid || manageDSAit || noop ) {
		tool_server_controls( ld, NULL, 0 );
	}

    retval = rc = 0;
    if (havedn)
	retval = domodrdn( ld, entrydn, rdn, newSuperior, remove_old_RDN );
    else while ((rc == 0 || contoper) && fgets(buf, sizeof(buf), fp) != NULL) {
	if ( *buf != '\n' ) {	/* blank lines optional, skip */
	    buf[ strlen( buf ) - 1 ] = '\0';	/* remove nl */

	    if ( havedn ) {	/* have DN, get RDN */
		if (( rdn = strdup( buf )) == NULL ) {
                    perror( "strdup" );
                    return( EXIT_FAILURE );
		}
		rc = domodrdn(ld, entrydn, rdn, newSuperior, remove_old_RDN );
		if ( rc != 0 )
			retval = rc;
		havedn = 0;
	    } else if ( !havedn ) {	/* don't have DN yet */
	        if (( entrydn = strdup( buf )) == NULL ) {
		    perror( "strdup" );
		    return( EXIT_FAILURE );
	        }
		++havedn;
	    }
	}
    }

	tool_unbind( ld );
	tool_destroy();
    return( retval );
}

static int domodrdn(
    LDAP	*ld,
    char	*dn,
    char	*rdn,
    char	*newSuperior,
    int		remove ) /* flag: remove old RDN */
{
	int rc, code, id;
	char *matcheddn=NULL, *text=NULL, **refs=NULL;
	LDAPMessage *res;

    if ( verbose ) {
		printf( _("Renaming \"%s\"\n"), dn );
		printf( _("\tnew rdn=\"%s\" (%s old rdn)\n"),
			rdn, remove ? _("delete") : _("keep") );
		if( newSuperior != NULL ) {
			printf(_("\tnew parent=\"%s\"\n"), newSuperior);
		}
	}

	if( not ) return LDAP_SUCCESS;

	rc = ldap_rename( ld, dn, rdn, newSuperior, remove,
		NULL, NULL, &id );

	if ( rc != LDAP_SUCCESS ) {
		fprintf( stderr, "%s: ldap_rename: %s (%d)\n",
			prog, ldap_err2string( rc ), rc );
		return rc;
	}

	for ( ; ; ) {
		struct timeval	tv = { 0, 0 };

		if ( tool_check_abandon( ld, id ) ) {
			return LDAP_CANCELLED;
		}

		tv.tv_sec = 0;
		tv.tv_usec = 100000;

		rc = ldap_result( ld, LDAP_RES_ANY, LDAP_MSG_ALL, &tv, &res );
		if ( rc < 0 ) {
			ldap_perror( ld, "ldapmodrdn: ldap_result" );
			return rc;
		}

		if ( rc != 0 ) {
			break;
		}
	}

	rc = ldap_parse_result( ld, res, &code, &matcheddn, &text, &refs, NULL, 1 );

	if( rc != LDAP_SUCCESS ) {
		fprintf( stderr, "%s: ldap_parse_result: %s (%d)\n",
			prog, ldap_err2string( rc ), rc );
		return rc;
	}

	if( verbose || code != LDAP_SUCCESS ||
		(matcheddn && *matcheddn) || (text && *text) || (refs && *refs) )
	{
		printf( _("Rename Result: %s (%d)\n"),
			ldap_err2string( code ), code );

		if( text && *text ) {
			printf( _("Additional info: %s\n"), text );
		}

		if( matcheddn && *matcheddn ) {
			printf( _("Matched DN: %s\n"), matcheddn );
		}

		if( refs ) {
			int i;
			for( i=0; refs[i]; i++ ) {
				printf(_("Referral: %s\n"), refs[i] );
			}
		}
	}

	ber_memfree( text );
	ber_memfree( matcheddn );
	ber_memvfree( (void **) refs );

	return code;
}
