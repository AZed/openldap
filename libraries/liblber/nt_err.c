/* $OpenLDAP: pkg/ldap/libraries/liblber/nt_err.c,v 1.13.2.3 2007/01/02 21:43:48 kurt Exp $ */
/* This work is part of OpenLDAP Software <http://www.openldap.org/>.
 *
 * Copyright 1998-2008 The OpenLDAP Foundation.
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

#include "portable.h"

#ifdef HAVE_WINSOCK2
#include <winsock2.h>
#elif HAVE_WINSOCK
#include <winsock.h>
#endif /* HAVE_WINSOCK(2) */

#define LBER_RETSTR( x ) case x: return #x;

char *ber_pvt_wsa_err2string( int err )
{
	switch( err ) {
		LBER_RETSTR( WSAEINTR )
		LBER_RETSTR( WSAEBADF )
		LBER_RETSTR( WSAEACCES )
		LBER_RETSTR( WSAEFAULT )
		LBER_RETSTR( WSAEINVAL )
		LBER_RETSTR( WSAEMFILE )
		LBER_RETSTR( WSAEWOULDBLOCK )
		LBER_RETSTR( WSAEINPROGRESS )
		LBER_RETSTR( WSAEALREADY )
		LBER_RETSTR( WSAENOTSOCK )
		LBER_RETSTR( WSAEDESTADDRREQ )
		LBER_RETSTR( WSAEMSGSIZE )
		LBER_RETSTR( WSAEPROTOTYPE )
		LBER_RETSTR( WSAENOPROTOOPT )
		LBER_RETSTR( WSAEPROTONOSUPPORT )
		LBER_RETSTR( WSAESOCKTNOSUPPORT )
		LBER_RETSTR( WSAEOPNOTSUPP )
		LBER_RETSTR( WSAEPFNOSUPPORT )
		LBER_RETSTR( WSAEAFNOSUPPORT )
		LBER_RETSTR( WSAEADDRINUSE )
		LBER_RETSTR( WSAEADDRNOTAVAIL )
		LBER_RETSTR( WSAENETDOWN )
		LBER_RETSTR( WSAENETUNREACH )
		LBER_RETSTR( WSAENETRESET )
		LBER_RETSTR( WSAECONNABORTED )
		LBER_RETSTR( WSAECONNRESET )
		LBER_RETSTR( WSAENOBUFS )
		LBER_RETSTR( WSAEISCONN )
		LBER_RETSTR( WSAENOTCONN )
		LBER_RETSTR( WSAESHUTDOWN )
		LBER_RETSTR( WSAETOOMANYREFS )
		LBER_RETSTR( WSAETIMEDOUT )
		LBER_RETSTR( WSAECONNREFUSED )
		LBER_RETSTR( WSAELOOP )
		LBER_RETSTR( WSAENAMETOOLONG )
		LBER_RETSTR( WSAEHOSTDOWN )
		LBER_RETSTR( WSAEHOSTUNREACH )
		LBER_RETSTR( WSAENOTEMPTY )
		LBER_RETSTR( WSAEPROCLIM )
		LBER_RETSTR( WSAEUSERS )
		LBER_RETSTR( WSAEDQUOT )
		LBER_RETSTR( WSAESTALE )
		LBER_RETSTR( WSAEREMOTE )
		LBER_RETSTR( WSASYSNOTREADY )
		LBER_RETSTR( WSAVERNOTSUPPORTED )
		LBER_RETSTR( WSANOTINITIALISED )
		LBER_RETSTR( WSAEDISCON )

#ifdef HAVE_WINSOCK2
		LBER_RETSTR( WSAENOMORE )
		LBER_RETSTR( WSAECANCELLED )
		LBER_RETSTR( WSAEINVALIDPROCTABLE )
		LBER_RETSTR( WSAEINVALIDPROVIDER )
		LBER_RETSTR( WSASYSCALLFAILURE )
		LBER_RETSTR( WSASERVICE_NOT_FOUND )
		LBER_RETSTR( WSATYPE_NOT_FOUND )
		LBER_RETSTR( WSA_E_NO_MORE )
		LBER_RETSTR( WSA_E_CANCELLED )
		LBER_RETSTR( WSAEREFUSED )
#endif /* HAVE_WINSOCK2	*/

		LBER_RETSTR( WSAHOST_NOT_FOUND )
		LBER_RETSTR( WSATRY_AGAIN )
		LBER_RETSTR( WSANO_RECOVERY )
		LBER_RETSTR( WSANO_DATA )
	}
	return "unknown WSA error";
}
