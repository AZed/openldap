/* id2entry.c - routines to deal with the id2entry index */
/* $OpenLDAP: pkg/ldap/servers/slapd/back-ldbm/id2entry.c,v 1.18.2.5 2002/01/04 20:38:34 kurt Exp $ */
/*
 * Copyright 1998-2002 The OpenLDAP Foundation, All Rights Reserved.
 * COPYING RESTRICTIONS APPLY, see COPYRIGHT file
 */

#include "portable.h"

#include <stdio.h>

#include <ac/socket.h>

#include "slap.h"
#include "back-ldbm.h"

/*
 * This routine adds (or updates) an entry on disk.
 * The cache should already be updated. 
 */

int
id2entry_add( Backend *be, Entry *e )
{
	struct ldbminfo	*li = (struct ldbminfo *) be->be_private;
	DBCache	*db;
	Datum		key, data;
	int		len, rc, flags;

	ldbm_datum_init( key );
	ldbm_datum_init( data );

	Debug( LDAP_DEBUG_TRACE, "=> id2entry_add( %ld, \"%s\" )\n", e->e_id,
	    e->e_dn, 0 );

	if ( (db = ldbm_cache_open( be, "id2entry", LDBM_SUFFIX, LDBM_WRCREAT ))
	    == NULL ) {
		Debug( LDAP_DEBUG_ANY, "Could not open/create id2entry%s\n",
		    LDBM_SUFFIX, 0, 0 );
		return( -1 );
	}

	key.dptr = (char *) &e->e_id;
	key.dsize = sizeof(ID);

	ldap_pvt_thread_mutex_lock( &entry2str_mutex );
	data.dptr = entry2str( e, &len );
	data.dsize = len + 1;

	/* store it */
	flags = LDBM_REPLACE;
	rc = ldbm_cache_store( db, key, data, flags );

	ldap_pvt_thread_mutex_unlock( &entry2str_mutex );

	ldbm_cache_close( be, db );

	Debug( LDAP_DEBUG_TRACE, "<= id2entry_add %d\n", rc, 0, 0 );

	return( rc );
}

int
id2entry_delete( Backend *be, Entry *e )
{
	struct ldbminfo	*li = (struct ldbminfo *) be->be_private;
	DBCache	*db;
	Datum		key;
	int		rc;

	Debug(LDAP_DEBUG_TRACE, "=> id2entry_delete( %ld, \"%s\" )\n", e->e_id,
	    e->e_dn, 0 );

#ifdef notdef
#ifdef LDAP_RDWR_DEBUG
	/* check for writer lock */
	assert(ldap_pvt_thread_rdwr_writers(&e->e_rdwr) == 1);
#endif
#endif

	ldbm_datum_init( key );

	if ( (db = ldbm_cache_open( be, "id2entry", LDBM_SUFFIX, LDBM_WRCREAT ))
		== NULL ) {
		Debug( LDAP_DEBUG_ANY, "Could not open/create id2entry%s\n",
		    LDBM_SUFFIX, 0, 0 );
		return( -1 );
	}

	if ( cache_delete_entry( &li->li_cache, e ) != 0 ) {
		Debug(LDAP_DEBUG_ANY, "could not delete %ld (%s) from cache\n",
		    e->e_id, e->e_dn, 0 );
	}

	key.dptr = (char *) &e->e_id;
	key.dsize = sizeof(ID);

	rc = ldbm_cache_delete( db, key );

	ldbm_cache_close( be, db );

	Debug( LDAP_DEBUG_TRACE, "<= id2entry_delete %d\n", rc, 0, 0 );
	return( rc );
}

/* returns entry with reader/writer lock */
Entry *
id2entry_rw( Backend *be, ID id, int rw )
{
	struct ldbminfo	*li = (struct ldbminfo *) be->be_private;
	DBCache	*db;
	Datum		key, data;
	Entry		*e;

	ldbm_datum_init( key );
	ldbm_datum_init( data );

	Debug( LDAP_DEBUG_TRACE, "=> id2entry_%s( %ld )\n",
		rw ? "w" : "r", id, 0 );

	if ( (e = cache_find_entry_id( &li->li_cache, id, rw )) != NULL ) {
		Debug( LDAP_DEBUG_TRACE, "<= id2entry_%s( %ld ) 0x%lx (cache)\n",
			rw ? "w" : "r", id, (unsigned long) e );
		return( e );
	}

	if ( (db = ldbm_cache_open( be, "id2entry", LDBM_SUFFIX, LDBM_WRCREAT ))
		== NULL ) {
		Debug( LDAP_DEBUG_ANY, "Could not open id2entry%s\n",
		    LDBM_SUFFIX, 0, 0 );
		return( NULL );
	}

	key.dptr = (char *) &id;
	key.dsize = sizeof(ID);

	data = ldbm_cache_fetch( db, key );

	if ( data.dptr == NULL ) {
		Debug( LDAP_DEBUG_TRACE, "<= id2entry_%s( %ld ) not found\n",
			rw ? "w" : "r", id, 0 );
		ldbm_cache_close( be, db );
		return( NULL );
	}

	e = str2entry( data.dptr );
	ldbm_datum_free( db->dbc_db, data );
	ldbm_cache_close( be, db );

	if ( e == NULL ) {
		Debug( LDAP_DEBUG_TRACE, "<= id2entry_%s( %ld ) (failed)\n",
			rw ? "w" : "r", id, 0 );
		return( NULL );
	}

	e->e_id = id;

	if( cache_add_entry_rw( &li->li_cache, e, rw ) != 0 ) {
		entry_free( e );

		/* XXX this is a kludge.
		 * maybe the entry got added underneath us
		 * There are many underlying race condtions in the cache/disk code.
		 */
		if ( (e = cache_find_entry_id( &li->li_cache, id, rw )) != NULL ) {
			Debug( LDAP_DEBUG_TRACE, "<= id2entry_%s( %ld ) 0x%lx (cache)\n",
				rw ? "w" : "r", id, (unsigned long) e );
			return( e );
		}

		Debug( LDAP_DEBUG_TRACE, "<= id2entry_%s( %ld ) (cache add failed)\n",
			rw ? "w" : "r", id, 0 );
		return NULL;
	}

	Debug( LDAP_DEBUG_TRACE, "<= id2entry_%s( %ld ) 0x%lx (disk)\n",
		rw ? "w" : "r", id, (unsigned long) e );

	/* marks the entry as committed, so it will get added to the cache
	 * when the lock is released */
	cache_entry_commit( e );

	return( e );
}
