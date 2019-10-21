/* 
   Unix SMB/CIFS implementation.

   a partial implementation of DES designed for use in the 
   SMB authentication protocol

   Copyright (C) Andrew Tridgell 1998
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include "includes.h"
#include "libcli/auth/libcli_auth.h"

#include <gnutls/gnutls.h>
#include <gnutls/crypto.h>

static void str_to_key(const uint8_t *str,uint8_t *key)
{
	int i;

	key[0] = str[0]>>1;
	key[1] = ((str[0]&0x01)<<6) | (str[1]>>2);
	key[2] = ((str[1]&0x03)<<5) | (str[2]>>3);
	key[3] = ((str[2]&0x07)<<4) | (str[3]>>4);
	key[4] = ((str[3]&0x0F)<<3) | (str[4]>>5);
	key[5] = ((str[4]&0x1F)<<2) | (str[5]>>6);
	key[6] = ((str[5]&0x3F)<<1) | (str[6]>>7);
	key[7] = str[6]&0x7F;
	for (i=0;i<8;i++) {
		key[i] = (key[i]<<1);
	}
}

static int des_crypt56_gnutls(uint8_t out[8], const uint8_t in[8],
			      const uint8_t key_in[7], bool enc)
{
	static uint8_t iv8[8];
	gnutls_datum_t iv = { iv8, 8 };
	gnutls_datum_t key;
	gnutls_cipher_hd_t ctx;
	uint8_t key2[8];
	uint8_t outb[8];
	int ret;

	memset(out, 0, 8);

	str_to_key(key_in, key2);

	key.data = key2;
	key.size = 8;

	ret = gnutls_global_init();
	if (ret != 0) {
		return ret;
	}

	ret = gnutls_cipher_init(&ctx, GNUTLS_CIPHER_DES_CBC, &key, &iv);
	if (ret != 0) {
		return ret;
	}

	memcpy(outb, in, 8);
	if (enc) {
		ret = gnutls_cipher_encrypt(ctx, outb, 8);
	} else {
		ret = gnutls_cipher_decrypt(ctx, outb, 8);
	}

	if (ret == 0) {
		memcpy(out, outb, 8);
	}

	gnutls_cipher_deinit(ctx);

	return ret;
}

/*
  basic des crypt using a 56 bit (7 byte) key
*/
void des_crypt56(uint8_t out[8], const uint8_t in[8], const uint8_t key[7], int forw)
{
	(void)des_crypt56_gnutls(out, in, key, forw);
}

void E_P16(const uint8_t *p14,uint8_t *p16)
{
	const uint8_t sp8[8] = {0x4b, 0x47, 0x53, 0x21, 0x40, 0x23, 0x24, 0x25};
	des_crypt56(p16, sp8, p14, 1);
	des_crypt56(p16+8, sp8, p14+7, 1);
}

void E_P24(const uint8_t *p21, const uint8_t *c8, uint8_t *p24)
{
	des_crypt56(p24, c8, p21, 1);
	des_crypt56(p24+8, c8, p21+7, 1);
	des_crypt56(p24+16, c8, p21+14, 1);
}

void D_P16(const uint8_t *p14, const uint8_t *in, uint8_t *out)
{
	des_crypt56(out, in, p14, 0);
        des_crypt56(out+8, in+8, p14+7, 0);
}

void E_old_pw_hash( uint8_t *p14, const uint8_t *in, uint8_t *out)
{
        des_crypt56(out, in, p14, 1);
        des_crypt56(out+8, in+8, p14+7, 1);
}

/* des encryption with a 128 bit key */
void des_crypt128(uint8_t out[8], const uint8_t in[8], const uint8_t key[16])
{
	uint8_t buf[8];
	des_crypt56(buf, in, key, 1);
	des_crypt56(out, buf, key+9, 1);
}

/* des encryption with a 112 bit (14 byte) key */
void des_crypt112(uint8_t out[8], const uint8_t in[8], const uint8_t key[14], int forw)
{
	uint8_t buf[8];
	des_crypt56(buf, in, key, forw);
	des_crypt56(out, buf, key+7, forw);
}

/* des encryption of a 16 byte lump of data with a 112 bit key */
void des_crypt112_16(uint8_t out[16], const uint8_t in[16], const uint8_t key[14], int forw)
{
        des_crypt56(out, in, key, forw);
        des_crypt56(out + 8, in + 8, key+7, forw);
}

/* Decode a sam password hash into a password.  The password hash is the
   same method used to store passwords in the NT registry.  The DES key
   used is based on the RID of the user. */
void sam_rid_crypt(unsigned int rid, const uint8_t *in, uint8_t *out, int forw)
{
	uint8_t s[14];

	s[0] = s[4] = s[8] = s[12] = (uint8_t)(rid & 0xFF);
	s[1] = s[5] = s[9] = s[13] = (uint8_t)((rid >> 8) & 0xFF);
	s[2] = s[6] = s[10]        = (uint8_t)((rid >> 16) & 0xFF);
	s[3] = s[7] = s[11]        = (uint8_t)((rid >> 24) & 0xFF);

	des_crypt56(out, in, s, forw);
	des_crypt56(out+8, in+8, s+7, forw);
}
