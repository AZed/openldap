/* $OpenLDAP$ */
/* This work is part of OpenLDAP Software <http://www.openldap.org/>.
 *
 * Copyright 1998-2009 The OpenLDAP Foundation.
 * Portions Copyright 1998-2003 Kurt D. Zeilenga.
 * Portions Copyright 2003 IBM Corporation.
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
 * This work was initially developed by Pierangelo Masarati for inclusion
 * in OpenLDAP Software.  Code portions borrowed from slapcat.c;
 * contributors are Kurt Zeilenga and Jong Hyuk Choi
 */

#include "portable.h"

#include <stdio.h>

#include "ac/stdlib.h"
#include "ac/ctype.h"
#include "ac/socket.h"
#include "ac/string.h"

#include "slapcommon.h"
#include "ldif.h"

static volatile sig_atomic_t gotsig;

static RETSIGTYPE
slapcat_sig( int sig )
{
	gotsig=1;
}

int
slapschema( int argc, char **argv )
{
	ID id;
	int rc = EXIT_SUCCESS;
	const char *progname = "slapschema";
	Connection conn = { 0 };
	OperationBuffer	opbuf;
	Operation *op = NULL;
	void *thrctx;

	slap_tool_init( progname, SLAPCAT, argc, argv );

#ifdef SIGPIPE
	(void) SIGNAL( SIGPIPE, slapcat_sig );
#endif
#ifdef SIGHUP
	(void) SIGNAL( SIGHUP, slapcat_sig );
#endif
	(void) SIGNAL( SIGINT, slapcat_sig );
	(void) SIGNAL( SIGTERM, slapcat_sig );

	if( !be->be_entry_open ||
		!be->be_entry_close ||
		!be->be_entry_first ||
		!be->be_entry_next ||
		!be->be_entry_get )
	{
		fprintf( stderr, "%s: database doesn't support necessary operations.\n",
			progname );
		exit( EXIT_FAILURE );
	}

	if( be->be_entry_open( be, 0 ) != 0 ) {
		fprintf( stderr, "%s: could not open database.\n",
			progname );
		exit( EXIT_FAILURE );
	}

	thrctx = ldap_pvt_thread_pool_context();
	connection_fake_init( &conn, &opbuf, thrctx );
	op = &opbuf.ob_op;
	op->o_tmpmemctx = NULL;
	op->o_bd = be;

	for ( id = be->be_entry_first( be );
		id != NOID;
		id = be->be_entry_next( be ) )
	{
		Entry* e;
		char textbuf[SLAP_TEXT_BUFLEN];
		size_t textlen = sizeof(textbuf);
		const char *text = NULL;

		if ( gotsig )
			break;

		e = be->be_entry_get( be, id );
		if ( e == NULL ) {
			printf("# no data for entry id=%08lx\n\n", (long) id );
			rc = EXIT_FAILURE;
			if( continuemode ) continue;
			break;
		}

		if( sub_ndn.bv_len && !dnIsSuffix( &e->e_nname, &sub_ndn ) ) {
			be_entry_release_r( op, e );
			continue;
		}

		if( filter != NULL ) {
			int rc = test_filter( NULL, e, filter );
			if( rc != LDAP_COMPARE_TRUE ) {
				be_entry_release_r( op, e );
				continue;
			}
		}

		if( verbose ) {
			printf( "# id=%08lx\n", (long) id );
		}

		rc = entry_schema_check( op, e, NULL, 0, 0, NULL,
			&text, textbuf, textlen );
		if ( rc != LDAP_SUCCESS ) {
			fprintf( ldiffp->fp, "# (%d) %s%s%s\n",
				rc, ldap_err2string( rc ),
				text ? ": " : "",
				text ? text : "" );
			fprintf( ldiffp->fp, "dn: %s\n\n", e->e_name.bv_val );
		}

		be_entry_release_r( op, e );
	}

	be->be_entry_close( be );

	if ( slap_tool_destroy() )
		rc = EXIT_FAILURE;

	return rc;
}
