/* $OpenLDAP: pkg/ldap/servers/slapd/back-passwd/back-passwd.h,v 1.7.2.3 2008/02/11 23:26:47 kurt Exp $ */
/* This work is part of OpenLDAP Software <http://www.openldap.org/>.
 *
 * Copyright 1998-2009 The OpenLDAP Foundation.
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

#ifndef _BACK_PASSWD_H
#define _BACK_PASSWD_H

#include "proto-passwd.h"

LDAP_BEGIN_DECL

extern ldap_pvt_thread_mutex_t passwd_mutex;

extern BI_destroy	passwd_back_destroy;

extern BI_db_config	passwd_back_db_config;

extern BI_op_search	passwd_back_search;

LDAP_END_DECL

#endif /* _BACK_PASSWD_H */
