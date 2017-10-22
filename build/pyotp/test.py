#!/usr/bin/env python

from __future__ import print_function, unicode_literals, division, absolute_import

import base64
import datetime
import hashlib
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
import pyotp


class HOTPExampleValuesFromTheRFC(unittest.TestCase):
    def testMatchTheRFC(self):
        # 12345678901234567890 in Bas32
        # GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ
        hotp = pyotp.HOTP('GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ')
        self.assertEqual(hotp.at(0), '755224')
        self.assertEqual(hotp.at(1), '287082')
        self.assertEqual(hotp.at(2), '359152')
        self.assertEqual(hotp.at(3), '969429')
        self.assertEqual(hotp.at(4), '338314')
        self.assertEqual(hotp.at(5), '254676')
        self.assertEqual(hotp.at(6), '287922')
        self.assertEqual(hotp.at(7), '162583')
        self.assertEqual(hotp.at(8), '399871')
        self.assertEqual(hotp.at(9), '520489')

    def testVerifyAnOTPAndNowAllowReuse(self):
        hotp = pyotp.HOTP('GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ')
        self.assertTrue(hotp.verify('520489', 9))
        self.assertFalse(hotp.verify('520489', 10))
        self.assertFalse(hotp.verify('520489', 10))

    def testProvisioningURI(self):
        hotp = pyotp.HOTP('wrn3pqx5uqxqvnqr')

        self.assertEqual(
            hotp.provisioning_uri('mark@percival'),
            'otpauth://hotp/mark@percival?secret=wrn3pqx5uqxqvnqr&counter=0')

        self.assertEqual(
            hotp.provisioning_uri('mark@percival', initial_count=12),
            'otpauth://hotp/mark@percival?secret=wrn3pqx5uqxqvnqr&counter=12')

        self.assertEqual(
            hotp.provisioning_uri('mark@percival', issuer_name='FooCorp!'),
            'otpauth://hotp/FooCorp%21:mark@percival?secret=wrn3pqx5uqxqvnqr&counter=0&issuer=FooCorp%21')


class TOTPExampleValuesFromTheRFC(unittest.TestCase):
    RFC_VALUES = {
        (hashlib.sha1, b'12345678901234567890'): (
            (59, '94287082'),
            (1111111109, '07081804'),
            (1111111111, '14050471'),
            (1234567890, '89005924'),
            (2000000000, '69279037'),
            (20000000000, '65353130'),
        ),

        (hashlib.sha256, b'12345678901234567890123456789012'): (
            (59, 46119246),
            (1111111109, '68084774'),
            (1111111111, '67062674'),
            (1234567890, '91819424'),
            (2000000000, '90698825'),
            (20000000000, '77737706'),
        ),

        (hashlib.sha512, b'1234567890123456789012345678901234567890123456789012345678901234'): (
            (59, 90693936),
            (1111111109, '25091201'),
            (1111111111, '99943326'),
            (1234567890, '93441116'),
            (2000000000, '38618901'),
            (20000000000, '47863826'),
        ),
    }

    def testMatchTheRFC(self):
        for digest, secret in self.RFC_VALUES:
            totp = pyotp.TOTP(base64.b32encode(secret), 8, digest)
            for utime, code in self.RFC_VALUES[(digest, secret)]:
                value = totp.at(utime)
                msg = "%s != %s (%s, time=%d)"
                msg %= (value, code, digest().name, utime)
                self.assertEqual(value, str(code), msg)

    def testMatchTheRFCDigitLength(self):
        totp = pyotp.TOTP('GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ')
        self.assertEqual(totp.at(1111111111), '050471')
        self.assertEqual(totp.at(1234567890), '005924')
        self.assertEqual(totp.at(2000000000), '279037')

    def testMatchTheGoogleAuthenticatorOutput(self):
        totp = pyotp.TOTP('wrn3pqx5uqxqvnqr')
        with Timecop(1297553958):
            self.assertEqual(totp.now(), '102705')

    def testValidateATimeBasedOTP(self):
        totp = pyotp.TOTP('wrn3pqx5uqxqvnqr')
        with Timecop(1297553958):
            self.assertTrue(totp.verify('102705'))
            self.assertTrue(totp.verify('102705'))
        with Timecop(1297553958 + 30):
            self.assertFalse(totp.verify('102705'))

    def testValidateATimeBasedOTPWithDigitLength(self):
        totp = pyotp.TOTP('GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ')
        with Timecop(1111111111):
            self.assertTrue(totp.verify('050471'))
        with Timecop(1297553958 + 30):
            self.assertFalse(totp.verify('050471'))

    def testProvisioningURI(self):
        totp = pyotp.TOTP('wrn3pqx5uqxqvnqr')
        self.assertEqual(
            totp.provisioning_uri('mark@percival'),
            'otpauth://totp/mark@percival?secret=wrn3pqx5uqxqvnqr')

        self.assertEqual(
            totp.provisioning_uri('mark@percival', issuer_name='FooCorp!'),
            'otpauth://totp/FooCorp%21:mark@percival?secret=wrn3pqx5uqxqvnqr&issuer=FooCorp%21')

    def testRandomKeyGeneration(self):
        self.assertEqual(len(pyotp.random_base32()), 16)
        self.assertEqual(len(pyotp.random_base32(length=20)), 20)


class StringComparisonTest(unittest.TestCase):
    def testComparisons(self):
        self.assertTrue(pyotp.utils.strings_equal("", ""))
        self.assertTrue(pyotp.utils.strings_equal("a", "a"))
        self.assertTrue(pyotp.utils.strings_equal("a" * 1000, "a" * 1000))

        self.assertFalse(pyotp.utils.strings_equal("", "a"))
        self.assertFalse(pyotp.utils.strings_equal("a", ""))
        self.assertFalse(pyotp.utils.strings_equal("a" * 999 + "b", "a" * 1000))


class Timecop(object):
    """
    Half-assed clone of timecop.rb, just enough to pass our tests.
    """

    def __init__(self, freeze_timestamp):
        self.freeze_timestamp = freeze_timestamp

    def __enter__(self):
        self.real_datetime = datetime.datetime
        datetime.datetime = self.frozen_datetime()

    def __exit__(self, type, value, traceback):
        datetime.datetime = self.real_datetime

    def frozen_datetime(self):
        class FrozenDateTime(datetime.datetime):
            @classmethod
            def now(cls, **kwargs):
                return cls.fromtimestamp(timecop.freeze_timestamp)

        timecop = self
        return FrozenDateTime


if __name__ == '__main__':
    unittest.main()
